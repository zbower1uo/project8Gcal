import timeblock
import logging
import arrow

def freetimes(busylist, begin, end):
  """
  Takes a list of busy times and checks to see if they are within the proper time range
  Args:
    busy_list: a list of busy dictionary events within a datetime range (with overlapping in/out of dates)
    begin: start datetime of daterange
    end: end datetime of daterange
  Returns:
    free_list: list with free blocks in datetime range
  """
  busyList = []

  for event in busylist:
  	e = timeblock.TimeBlock(event._start, event._end, event._summary)
  	busyList.append(e)
  # List of available timeblocks
  freeTimes = to_datetime(begin, end)
  free_list = freeTimes

  print("inside loop")

  for etime in busyList:
    calcFree = []
    for ft in free_list:
      if ft._startdate == etime._startdate or ft._enddate == etime._enddate: # if dates are the same
        if etime._starttime < ft._starttime and etime._endtime > ft._endtime: # etime has a wider time range than ft
            continue # go to the next ft, do not add to calcFree
        if etime._starttime >= ft._endtime or etime._endtime <= ft._starttime:
          calcFree.append(ft) # no overlap
        else: 
          tb1, tb2 = ft.split(etime)
          if tb1._starttime >= tb1._endtime and tb2._starttime >= tb2._endtime:
            continue
          if tb2._starttime >= tb2._endtime:
            calcFree.append(tb1)
          if tb1._starttime >= tb1._endtime:
            calcFree.append(tb2)
          elif tb1._starttime < tb1._endtime and tb2._starttime < tb2._endtime:
            calcFree.append(tb1)
            calcFree.append(tb2)
      else:
        calcFree.append(ft) # if no overlap

    
    free_list = calcFree
    for f in free_list:
      print(f._starttime)
      print(f._endtime)
      print(f._startdate)
  return free_list

def to_datetime(begin, end):
  avail_list = []
  day_list = []
  counter = 0

  # Convert to arrow objects
  begin = arrow.get(begin)
  end = arrow.get(end)
  # Convert to strings for subsequent conversion
  begin_time = str(begin.time())
  begin_hour = int(begin_time[:2])
  begin_minute = int(begin_time[3:5])

  end_time = str(end.time())
  end_hour = int(end_time[:2])
  end_minute = int(end_time[3:5])

  # Find how many days there are between begin and end
  for day in arrow.Arrow.span_range('day', begin, end):
    day_list.append(day)
  for day in day_list:
    counter += 1
    start = day[0].replace(hour=begin_hour, minute=begin_minute)
    end = day[1].replace(hour=end_hour, minute=end_minute)
    avail_tb = timeblock.TimeBlock(start,end, "Block : " + str(counter))
    avail_list.append(avail_tb)

  return avail_list
