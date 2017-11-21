import arrow
import timeblock
from timeblock import TimeBlock


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

def getbusy(service, flaskcalendarids, begindate, enddate):
  calendarids = flaskcalendarids
  theEvents = []
  #formatting the date and time into an iso format, using nows to add the timezone
  
  for cid in calendarids: 
    events = service.events().list( calendarId = cid ,
                    singleEvents = True,
                    timeMin = begindate, #request time date based on user input
                    timeMax = enddate,
                    orderBy="startTime"
        ).execute()
    for e in events['items']:
      if ("transparency" in e and e["transparency"] == "transparent"):
        continue
      else:
        summary = e["summary"]
      if "date" in e["start"]:
        start = "All day " + e["start"]["date"]
      elif "dateTime" in e["start"]:
        start = e["start"]["dateTime"]
        end = e["end"]["dateTime"]
      else:
        raise Exception("unknown time format/something went wrong")
      t = TimeBlock(start,end,summary)
      theEvents.append(t)

  return theEvents


def order_busy(tosort):
    
    for time in tosort:
        busyStart = arrow.get(time["start"]).format('YYYY-MM-DD HH:mm')
        busyEnd = arrow.get(time["end"]).format('YYYY-MM-DD HH:mm')


