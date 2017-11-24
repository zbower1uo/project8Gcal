import timeblock
from timeblock import TimeBlock
import logging
import arrow

def freetimes(busylist, begin, end):
  '''
Current version for creating free times takes begin times and end times,
creates a list of free times then parses it and returns the parsed times
  '''
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
  for etime in busyList:
    for ft in freeTimes:
      #dates are equal
      if ft._startdate == etime._startdate or ft._enddate == etime._enddate: # if dates are the same
        if etime._starttime < ft._starttime and etime._endtime > ft._endtime:
          continue
        if etime._starttime >= ft._endtime or etime._endtime <= ft._starttime:
          if ft not in freeBlocks:
            freeBlocks.append(ft)
        else:
          timeblock1 , timeblock2 = ft.split_block(etime)
          if timeblock1._starttime >= timeblock1._endtime and timeblock2._starttime >= timeblock2._endtime:
            continue
          if timeblock2._starttime >= timeblock2._endtime:
            freeBlocks.append(timeblock1)
          if timeblock1._starttime >= timeblock1._endtime:
            freeBlocks.append(timeblock2)
          elif timeblock1._starttime < timeblock1._endtime and timeblock2._starttime < timeblock2._endtime:
            freeBlocks.append(timeblock1)
            freeBlocks.append(timeblock2)
      else:
        if ft in freeBlocks:
          continue
        else:
          freeBlocks.append(ft)

  return freeBlocks


def create_free_time(begin , end):
  '''
  Creates a block of free times, assumes the time given in application are free
  loops through the number of days and creates timeblock obj

  '''

  begin = arrow.get(begin)
  end = arrow.get(end)
  bhourr = begin.time()
  ehourr = end.time()
  dayDifference =  end - begin
  dd = int((dayDifference).days)
  freeTimes = [] #create list for free times
  while dd >= 0:
    bhour = begin.replace(hour = bhourr.hour , minute = bhourr.minute) #
    bend = begin.replace(hour = ehourr.hour , minute = ehourr.minute )
    freeTimes.append(timeblock.TimeBlock(bhour , bend , "FreeTime Block"))
    begin = begin.shift(days=+1)
    dd -=1
  return freeTimes
