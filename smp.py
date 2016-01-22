from datetime import datetime
from crscls import Course
import icalendar as ical
import pytz
import tempfile
import os

CalDir = 'C:\Python34\icalscript'
##semstrend = datetime(2016,5,2,22,0,0,tzinfo=pytz.timezone('US/Central'))


#required properties for compliance
cal = ical.Calendar()
cal.add('prodid', '-//Gnarly Lyle DE SMP Calendar//mxm.dk//')
cal.add('version', '2.0')

#takes in a pre-defined Course object
#returns an event and adds it to the specified calendar
def weeklyEvent(Course,CalDir):
    event = ical.Event()
    event.add('summary', Course.name)
    #pretty this up with the Course Class
    event.add('dtstart',Course.startDay())
    event.add('dtend', Course.endDay())
    event.add('dtstamp', Course.startDay())

    #for some reason, the ical python module
    #does not like it when i specify >1 days
    #in the same line for 'byday'
    for day in Course.listDays():
        freq = {
        'freq': 'weekly',
        'until': Course.lastDay(),
        'byday': day
        }
        event.add('rrule',freq)

    #adding in exception days / holidays
    #exdate has to have exact time as starttime, and same format (TZID)
    #maybe I should try use exrule (opposite of rrule)
    for day in Course.holiDays():
        event.add('exdate',day)
    event.add('location', Course.locate())
    cal.add_component(event)

    f = open(os.path.join(CalDir, 'Room.ics'),'wb')
    f.write(cal.to_ical())
    f.close()

if __name__ == '__main__':
    
    asdf = Course('Cse5381')
    asdf.setstartDate(2016,1,19)
    asdf.setendDate(2016,5,2)
    asdf.setstartTime(18,30,0)
    asdf.setendTime(21,30,0)
    asdf.addDays(['SU','MO'])
    #default timezone is Central Time
    asdf.addholiDays([datetime(2016,1,31,18,30,0),datetime(2016,2,1,18,30,0)])
    weeklyEvent(asdf, CalDir)
