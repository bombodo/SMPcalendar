
from icalendar import Calendar, Event, vCalAddress, vText, Timezone, TimezoneStandard, TimezoneDaylight
from datetime import datetime,timedelta
import pytz
import os

f = open('TV Operations Schedule Calendar.ics','r')
print(f)
fcal = Calendar.from_ical(f.read())
gcal = Calendar()
gcal.add('prodid', '-//My calendar product//mxm.dk//')
gcal.add('version','2.0')
gcal.add('calscale','GREGORIAN')
gcal.add('method','PUBLISH')
gcal.add('X-WR-CALNAME','C179')
gcal.add('X-WR-TIMEZONE','America/Chicago')
tz = Timezone()
#might need to accomodate for DSaveTime
dlt = TimezoneDaylight()
dlt.add('TZOFFSETFROM',timedelta(hours=-6))
dlt.add('RRULE',{'FREQ':'YEARLY','BYMONTH':'3','BYDAY':'2SU'})
dlt['DTSTART']=datetime(2007,03,11,2,0,0)
dlt.add('TZNAME','CDT')
dlt.add('TZOFFSETTO',timedelta(hours=-5))
stnd = TimezoneStandard()
stnd.add('TZOFFSETFROM',timedelta(hours=-5))
stnd.add('RRULE',{'FREQ':'YEARLY','BYMONTH':'11','BYDAY':'1SU'})
stnd['DTSTART']=datetime(2007,11,4,2,0,0)
stnd.add('TZNAME','CST')
stnd.add('TZOFFSETTO',timedelta(hours=-6))
tz.add('TZID','America/Chicago')
tz.add_component(dlt)
tz.add_component(stnd)
gcal.add_component(tz)


room = {
##'J205':'
##'J203'
##'J113'
##'J101'
'C161':'CH157encoder161',
'C184':'CH157encoder184',
'C179':'CH157encoder179',
'C183':'CH157encoder183'
}
#checks all scheduled events
for ev3nt in fcal.walk('vevent'):
    #this is really sloppy not trying to figure out what causes Keyerror
    try:
        gcalevent = Event()
        summ = ev3nt['summary']
        gcalevent.add('summary',summ[7:])
        if (summ[0:4] in room) and ('Vacant' not in summ):
            try:
                gcalevent['location']=vText(room[summ[0:4]])
            except:
                gcalevent['location'] = vText(summ[0:4])
##            print gcalevent.get('location')
            bgntime = ev3nt['dtstart'].dt - timedelta(minutes =1)
            stamp = ev3nt['dtstamp'].dt - timedelta(minutes = 1)
            endtime = ev3nt['dtend'].dt + timedelta(minutes = 4)
            try:
                #one event EETS 8315 worked without replacing tzinfo
                gcalevent.add('dtstart',bgntime.replace(tzinfo = pytz.timezone('America/Chicago')))
                gcalevent.add('dtend',endtime.replace(tzinfo = pytz.timezone('America/Chicago')))
                gcalevent.add('dtstamp',stamp.replace(tzinfo = pytz.timezone('America/Chicago')))
##                attendee = vCalAddress('MAILTO:dehelp@lyle.smu.edu')
##                attendee.params['cn'] = vText('Lyle')
##                attendee.params['ROLE'] = vText('REQ-PARTICIPANT')
##                gcalevent.add('attendee', attendee, encode=0)
                try:
                    rules = ev3nt['rrule']
                    gcalevent.add('rrule',rules)
                except:
                    print('skipped rrules')
            except Exception as e:
                print(e)
            gcal.add_component(gcalevent)
    except KeyError as e:
        print(e)


g = open('Testing.ics','wb')
g.write(gcal.to_ical())
#close the new calendar
g.close()
#close the original
f.close()

##if __name__ == '__main__':
    

