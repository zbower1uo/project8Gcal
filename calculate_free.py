import timeblock
from timeblock import TimeBlock
import logging
import arrow

def freetimes(busylist, begin, end):
  busyList = []
  for event in busylist:
  	e = timeblock.TimeBlock(event._start, event._end, event._summary)
  	busyList.append(e)
  # List of available timeblocks
  freeTimes = create_free_time(begin, end)
  #print(freeTimes)
  freeBlocks = []
  for ft in freeTimes:
    if len(busyList) > 0:
      for ev in busyList:
        if ft._startdate == ev._startdate or ft._enddate == ev._enddate:
              if ev._starttime >= ft._starttime and ev._endtime <= ft._endtime:
                timeblock1 , timeblock2 = ft.split_block(ev)
                freeBlocks.append(timeblock1)
                freeBlocks.append(timeblock2)
        else:
          if ft not in freeBlocks:
            freeBlocks.append(ft)
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
