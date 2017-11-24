import timeblock
from timeblock import TimeBlock
import logging
import arrow

def freetimes(busylist, begin, end):
  busyList = []
  for b in busylist:
    print(b)
  for event in busylist:
  	e = timeblock.TimeBlock(event._start, event._end, event._summary)
  	busyList.append(e)
  # List of available timeblocks
  freeTimes = create_free_time(begin, end)
  #print(freeTimes)
  freeBlocks = []
  print("inside loop")
  for e in busyList:
    print(e._startdate)


  for etime in busyList:
    for ft in freeTimes:
      if ft._startdate == etime._startdate or ft._enddate == etime._enddate: # if dates are the same
        if etime._starttime < ft._starttime and etime._endtime > ft._endtime:
          continue
        if etime._starttime >= ft._starttime or etime._endtime <= ft._endtime:
          freeBlocks.append(ft)
        else:
          timeblock1 , timeblock2 = ft.split_block(etime)
          if timeblock1._starttime >= timeblock1._endtime and timeblock2._starttime >= timeblock2._endtime:
            continue
          if timeblock2._starttime >= timeblock2._endtime:
            freeBlocks.append(timeblock1)
          if timeblock2._starttime >= timeblock2._endtime:
            freeBlocks.append(timeblock2)
          elif timeblock1._starttime < timeblock1._endtime and timeblock2._starttime < timeblock2._endtime:
            freeBlocks.append(timeblock1)
            freeBlocks.append(timeblock2)
      else:
        freeBlocks.append(ft)
  for f in freeTimes:
    print(f._startdate)
  return freeTimes


def create_free_time(begin , end):
  begin = arrow.get(begin)
  end = arrow.get(end)
  dayDifference =  end - begin
  
  dd = int((dayDifference).days)
  freeTimes = [] #create list for free times
  while dd >= 0:
    bhour = begin.replace(hour = 0 , minute = 0) #
    bend = begin.replace(hour = 23 , minute = 59 )
    freeTimes.append(timeblock.TimeBlock(bhour , bend , "FreeTime Block"))
    begin = begin.shift(days=+1)
    dd -=1
  return freeTimes
