import timeblock
from timeblock import TimeBlock
import arrow

def freetimes(busylist, begin, end):
  """
  busylist: A list of busy obj (taken from flask)
  begin: Begin timerange to check for free slots
  end: End timerange to check for free slots

  This function takes a list of busy objects , begining time/date , end time/date
  and begins the process of making the free time calculations  
  """
  busyList = []
  for e in busylist:
    busyEvent = timeblock.TimeBlock(e.start , e.end)
    busyList.append(busyEvent)
    #no busy events so just give them all the free times
  
  freetimes = create_free_time(begin , end)

  for f in freetimes:
    f.bittime ^= f.bittime #initialze the free times to all 0's (at least until create free times is figured out)
  for f in freetimes:
    for b in busyList:
      if f.date == b.date:
        f.bittime = f.bittime | b.bittime #or the values together if they are on the same date
        #this creates a bittime with all the values on the same date 

  length = len(freetimes[0].bittime) # get len of array to translate bittime into human readable
  ft = []
  #TODO rework logic, just got it working for now
  for f in freetimes:
    alreadyFound = False #marker for found a free time, as a day can contain multiple free blocks
    date = f.date #date marker for free time
    duration = 0 #duarion of event in 15min intervals
    index =0 #start index of free event (used to calculate start hour/min and then add duration)
    temp = f.bittime #variable to hold bittime until indexing works 
    for i in range(length):
      if temp[i] == 0 and alreadyFound ==False:
        index = i
        alreadyFound = True
      elif temp[i] == 0:
        duration +=15 #15 as each 1 in the bitstring stands for 15 min
      if temp[i] ==1 or i == (length -1):
        if alreadyFound == True:
          #convert to timeblock object
          ft.append({"date": date.strftime('%Y-%m-%d') , "index" :index_to_hour_min(index)  , "duration":duration, "bittime":f.bittime})
          duration = 0
          alreadyFound = False

  return ft

def index_to_hour_min(index):
  """
  index : Index taken from bitstring to find value(starting time)
  Function converts an index in the 96 element array and converts it
  to a datetime, 
  """
  minuteValues = {"0":00,
                  "25": 15,
                  "5": 30,
                  "75": 45
                        }

  index = index / 4
  hour , minute = str(index).split(".")
  return str(hour) + ":" + str(minuteValues.get(minute))


def create_free_time(begin , end):
  '''
  begin: the beginning of the range (taken from flask input)
  end: the end of the range (taken from flask input)
  Creates a block of free times, assumes the time given in application are free
  loops through the number of days and creates timeblock obj ex ample:
  time from 09:00  - 17:00 from date ranges 11/1 - 11/5
  will return a list of timeblock objects
  from 11/1 with times 09:00 - 17:00 to 11/5
  '''

  begin = arrow.get(begin)
  end = arrow.get(end)
  bhourr = begin.time()
  ehourr = end.time()
  #setting up variables to use when creating the timeblock obj
  dayDifference =  end - begin

  dd = int((dayDifference).days)
  freeTimes = [] #create list for free times
  while dd >= 0:
    bhour = begin.replace(hour = bhourr.hour , minute = bhourr.minute) #
    bend = begin.replace(hour = ehourr.hour , minute = ehourr.minute )
    freeTimes.append(timeblock.TimeBlock(bhour , bend))
    begin = begin.shift(days=+1)
    dd -=1
  return freeTimes