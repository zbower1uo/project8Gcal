import timeblock

def larger_end(busytime1 , busytime2):
	bend = busytime1.get_end_time()
	b2end = busytime2.get_end_time()

def trim_blocks(busytimes,opent,close):
	trimmed_blocks = []
	days = split_date(opent, close)
	for bt in busytimes:
		eventDays = split_date(bt.get_start_time(),bt.get_end_time())

		trim = trim_day(block,day_slices,event_slices) #TODO trim events/create new
		trimmed_blocks += trim

	return trimmed_blocks


def split_date(opentime, closetime):
	oyear, omonth, oday = opentime.format("YYYY:MM:DD").split(":")
	cyear, cmonth, cday = closetime.format("YYYY:MM:DD").split(":")
	##returns a list of time range ex 8am - 10pmin iso woudl yeild 8-10
	##
	stimes = []
	#ending times of the open times
	openEnd = opentime.replace(year=cyear, month = cmonth, day = cday)

	for i in arrow.Arrow.range('day', opentime, openEnd):
		stimes.append(i)

	etimes = []
	cclose = closetime.replace(year = oyear, month=omonth, day=oday)
	for i in arrow.Arrow.range('day',cclose, closetime):
		etimes.append(i)
	length = len(stimes)
	splitdays = []
	for i in range(length):
		splitdays.append(stimes[i])
		splitdays.append(etimes[i])
	return splitdays



def get_times_to_parse(busytimes, begindate, enddate, begintime, endtime):

	beginHour, beginMinute = begintime.split(":")
	endHour , endMinute = endtime.split(":")

	lowTime = arrow.get(begindate).replace(hour=beginHour, minute=beginMinute)
	lowYear, lowMonth, LowDay = open_time.format("YYYY:MM:DD").split(":")

	endTime = arrow.get(enddate).replace(hour=endHour,minute=endMinute)

	parsedBusy = []

	length = len(busytimes)
	for i in range(0 , length):
		#no overlap
		if busytimes[i].get_end_time() < busytimes[i+1].get_start_time():
			parsedBusy.append(busytimes[i])
		#overlap
		else:
			largerEnd = max(busytimes[i].get_end_time(),busytimes[i+1].get_end_time())
			block = timeblock.TimeBlock(busytime[i].get_start_time(),busytime[i].get_end_time(), busytime[i].get_summary())
	parsedBusy.append(busytimes[i])

	#trim here
	#go through all the events
	currentDay = lowTime
	curretnDaystart = lowTime
	currentDayend = endTime.replace(year = lowYear, month = lowMonth , day = LowDay)

	freeTimes = []

	for b in trimmedTimes:
		#at the end of the day
		if currentDay == currentDayend:
			curretnDaystart = curretnDaystart.shift(days=+1)
			currentDayend = currentDayend.shift(days=+1)
		if currentDay.time = b.get_start_time():
			currentDay = b.get_end_time()

		#check to see if they are the same day
		if currentDay.format("DD") == b.get_start_time().format("DD"):
			freeTime = timblock.TimeBlock(currentDay, b.get_start_time())
			freeTimes.append(freeTime)
			
		else:
			fill_gaps(pointer,current_day_start,current_day_end,block,times)
			pointer = block.get_end_time()
			y,m,d = list(map(int,pointer.format("YYYY:MM:DD").split(":")))
			current_day_start = current_day_start.replace(year=y,month=m,day=d)
			current_day_end = current_day_end.replace(year=y,month=m,day=d)








	


