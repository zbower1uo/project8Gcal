import arrow
import timeblock
from timeblock import TimeBlock

def getbusy(service, flaskcalendarids, begindate, enddate):
  """
  service : A Google service object
  flaskcalendarids: a list of calendar ids
  begindate: The date to begin checking for events
  enddate: The date to end check for events(inclusive)

  This function returns a list of TimeBlock objects each of which represents a busytime
  event going on , for example if the calendarid foo has an event on 01/01/2017 at 09:00
  - 17:00 
  The function would return a TimeBlock object with date 01/01/2017 and a start of 09:00 and
  end of 17:00
  
  """
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
      t = TimeBlock(start,end)
      theEvents.append(t)

  return theEvents


        


