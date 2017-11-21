import arrow
from dateutil import tz

'''
functions to calculate free times, as a separate file 
to help with testing etc
'''


def list_calendars(service):
    """
    Given a google 'service' object, return a list of
    calendars.  Each calendar is represented by a dict.
    The returned list is sorted to have
    the primary calendar first, and selected (that is, displayed in
    Google Calendars web app) calendars before unselected calendars.
    """
    print("Entering cft.list_calendars")  
    calendar_list = service.calendarList().list().execute()["items"]
    result = [ ]
    for cal in calendar_list:
        kind = cal["kind"]
        id = cal["id"]
        if "description" in cal: 
            desc = cal["description"]
        else:
            desc = "(no description)"
        summary = cal["summary"]
        # Optional binary attributes with False as default
        selected = ("selected" in cal) and cal["selected"]
        primary = ("primary" in cal) and cal["primary"]
        
        result.append(
            {"kind": kind,
             "id": id,
             "summary": summary,
             "selected": selected,
             "primary": primary,
             })

    return sorted(result, key=cal_sort_key)

def cal_sort_key(cal):
	if cal["selected"]:
		selected_key = " "
	else: 
		selected_key = "X"
	if cal["primary"]:
		primary_key = " "
	else:
		primary_key = "X"
	return (primary_key, selected_key, cal["summary"])

def cleanup_end_time(event, day_end ):

	cleanEndtime = day_end.split(":")
	endTime = arrow.get(event['dateTime_end'])
	endTime = endTime.replace(hour=int(cleanEndtime[0], minute=int(endTime[1])))
	return endTime.isoformat()

def plus_one_day(iso):

	atime = arrow.get(iso)
	return atime.replace(days=+1).isoformat()


def list_events(service , calendarIds, beginDate, endDate , beginTime, endTime, ignoreEvent ):
	nextDay = plus_one_day(endDate)
	result = []

	for cid in calendarId:
		event = service.events().list(
			calendarId=calendarIds,
			timeMin = beginDate,
			timeMax = nextDay,
			singleEvents = True,
			orderBy = 'startTime').execute()
		events = event.get('items',[])

		for e in events:
			start = e['start'].get('dateTime', e['start'].get(['date']))
			end = e['end'].get('dateTime', e['end'].get('date'))
			eventId = e['id']

			dtStart = arrow.get(start)
			dtEnd = arrow.get(end)
			summary = e['summary']
			allDay = False

			if 'transparency' in e:
				continue
			if ignoreEvent != None and eventId in ignoreEvent:
				continue
			
			#check for all day events and mark as such
			if str(dtEnd.time()) == '00:00:00' and str(dtStart.time()) == '00:00:00':
				dtStart = dtStart.replace(tzinfo='local')
				dtEnd = dtEnd.replace(minutes=-1,tzinfo='local')
				allDay = True
			elif str(dtStart.time()) <= beginTime and str(dtEnd.time()) >= endTime:
				allDay = True
			elif str(dtEnd.time()) <= beginTime or str(dtStart.time()) >= endTime:
				continue


			result.append({
				"eventid" : eventId,
				"summary": summary,
				"start" : dtStart.isoformat(),
				"end" : dtEnd.isoformat(),
				"allday" : allDay
				})
	return sorted(result, key = event_sort_key)

def event_sort_key(event):
	return event['start']

def get_busy(events, endTime):
	if len(events) < 2:
		if len(events) != 0:
			events[0]['block'] = 'busy'
		return events
	checkEvents = []

	for i in range(len(events)):
		startpre = arrow.get(events[i-1]["start"])
		endpre = arrow.get(events[i-1]["end"])
		start = arrow.get(events[i]["start"])
		end = arrow.get(events[i]["end"])
		if startpre <= start and endpre >= end:
			continue
		checkEvents.append(events[i])



	if len(checkEvents) < 2:
		if len(checkEvents) != 0:
			events[0]['block'] = 'busy'
		return checkEvents

	busyBlock = []

	for i in range(len(checkEvents)-1):
		checkEvents[i]['block'] = 'busy'
		end = arrow.get(checkEvents[i]["end"])
		start = arrow.get(checkEvents[i+1]["start"])
		if end >= start:
			checkEvents[i+1]['start'] = checkEvents[i]['start']
		else:
			if(str(end.time())) > endTime:
				checkEvents[-1]['end'] = cleanup_end_time(checkEvents[i], endTime)
			busyBlock.append(checkEvents[i])	

	if str(arrow.get(checkEvents[-1]['end']).time()) > endTime:
		checkEvents[-1]['end'] = cleanup_end_time(checkEvents[-1], endTime)
	checkEvents[-1]['block'] = 'busy'
	busyBlock.append(checkEvents[-1])

	return busyBlock

def calculate_free_blocks(busyBlock, beginDate, endDate, beginTime, endTime ):
	freeBegin = arrow.get(beginDate)
	freeEnd = arrow.get(endDate)
	days = (freeEnd-freeBegin).days

	dayBegin = beginTime.split(":")
	dayEnd = endTime.split(":")

	dayBegindate = freeBegin.replace(hour=int(dayBegin[0]), minute=int(dayBegin[1]))
	dayEnddate = freeBegin.replace(hour=int(dayEnd[0]), minute=int(dayEnd[1]))

	freeTimes = []
	for i in range(days):
		freeTimes.append({

			"fstart" : dayBegindate.isoformat(),
			"fend" : dayEnddate.isoformat(),
			"block" : 'free'

			}) 
		dayBegindate = dayBegindate.replace(days=+1)
		dayEnddate = dayEnddate.replace(days=+1)
	
	for i, busyBlock in enumerate(busyBlock):
		for j , freeTimes in enumerate(freeTimes):
			if busyBlock["allday"] and busyBlock["start"] <= freeTimes["fstart"]:
				del freeTimes[j]
				break
			elif busyBlock["end"] <= freeTimes["fstart"]:
				continue

			if busyBlock["end"] <= freeTimes["fend"]:
				time1 = {
					"fstart" : freeTimes["fstart"],
					"fend" : busyBlock["start"],
					"block" : "free",
					}
				time2 = {
					"fstart" : busyBlock["end"],
					"fend" : freeTimes["fend"],
					"block" : "free"
					}
				del freeTimes[j]

				if time1["fstart"] < time1["fend"]:
					freeTimes.append(time1)
				if time2["fstart"] < time2["fend"]:
					freeTimes.append(time2)
				break

		freeTimes.sort(key = event_sort_key)
	return freeTimes
