import arrow
import numpy
import math

class TimeBlock:
  def __init__(self ,start="00:00",end="00:00"):
    self.start = arrow.get(start)
    self.end = arrow.get(end)
    self.date = self.start.date()
    self.bittime = parse_datetime(start , end)
    self.date_str = str(self.date)

def create_time_block():
  '''
  Function to initialize an empty time block filled with 0's
  '''
  freeTime = numpy.full((96), 0 , dtype=int)              
  return freeTime


def parse_datetime(begin ,  end):
    '''
    Will parse a date given to be retured as an array of bitstrings ( 1 for busy 0 for free)
    ex input '2017-01-01 12:30:45' : will result in taking the HH:mm and parsing it based on a bit
    string with elements 0 - 23 representing 15min intervals and element 24 the date 1 reprsents busy
    0 free
    ex:
    0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0 2017-01-01
       0        1       2       3           4       5
    0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0 2017-01-01
       6        7       8        9       10      11
    0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0 2017-01-01
        12      13      14         15       16      17
    0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0  0 0 0 0 2017-01-01
        18      19      20     21          22       23
    '''
    pdatetime = arrow.get(begin).format('YYYY-MM-DD HH:mm')#parsed date
    edatetime = arrow.get(end).format('YYYY-MM-DD HH:mm')

    #begin min/hour
    phour = pdatetime[11:13]#12
    pmin = pdatetime[14:16]#30
    #end min/hour
    ehour = edatetime[11:13]#12
    emin = edatetime[14:16]#30

    starposH =(int(phour) * 4)#getting the element to start at
    startposM = (int(pmin) /15)
    startPosition = starposH + startposM

    endposH = (int(ehour) * 4)
    eposM = (int(emin) / 15)
    endPosition = ((endposH + eposM)-1)

    eventBitstring = create_time_block()
    eventBitstring [int(startPosition)]= 1
    eventBitstring [int(endPosition)] = 1

    length = endPosition - startPosition
    
    for i in range(int(length)):
        eventBitstring[int(startPosition) + i] = 1
 
    return eventBitstring

#add variable for either 1 or 0 depending on free/busy lookup
def bit_to_datetime(bitstring, date):
  """
  Bitstring: a bitstring to convert 
  
  date: The date the event occurs on

  Function takes a bitstring and changes it to dateTime obj
  the duration is then calculated and added to start time giving start/end

  ex 1111 0000 (with one block representing midnight and one 01:00)
  this will calculate 0 for hour and 45 duration, resulting in 00:45
  """
  stringlen = len(bitstring)
  index = 0 #index to store the start pos
  duration = 0
  for i in range(stringlen):
    if bitstring[i] == 1: #get starting position the start of the time
      index = i
      while( i < stringlen-1): #find out duration by adding all the ones
        if bitstring[i] == 1:
          duration +=1
        i+=1
      break
  #convert said results to start hour/min, then add the duration to find the end time
  timeHour = int(index / 4)
  timeMin = int((index % 4) * 15)

  if timeHour < 10 and timeMin < 15: 
    arrowStart = "{0} 0{1}:0{2}:00".format(date,timeHour,timeMin)
  elif timeHour < 10:
    arrowStart = "{0} 0{1}:{2}:00".format(date,timeHour,timeMin)
  else:
    arrowStart = "{0} {1}:{2}:00".format(date,timeHour,timeMin)

  timeBegin = arrow.get(arrowStart)
  timeEnd = timeBegin.shift(minutes=+ (duration *15))

  return timeBegin ,timeEnd
