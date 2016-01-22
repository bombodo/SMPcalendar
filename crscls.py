import datetime
import calendar
import pytz

class Course:
    
    def __init__(self, name, loc = ''):
        self.name = name.upper()
        self.location = loc
        self.notes = ''
        self.daysofop = []
        self.holidays = []
        
    #differentiate timeEnd and lastDay
    #lastDay for the calendar to know when to stop making events
    #timeEnd for the end time of the individual class instance
        self.fdstart = datetime.datetime.now()
        self.fdend = datetime.datetime.now()
        self.ldend = datetime.datetime.now()

        
    def addNotes(self, text):
        self.notes = self.notes + text

    def setstartTime(self, hrstrt, minstrt, secstrt, tzinf = 'US/Central'):
        self.fdstart = self.fdstart.replace(hour=hrstrt, minute=minstrt, second = secstrt, tzinfo = pytz.timezone(tzinf))
        
    def setendTime(self, hrend, minend, secstrt, tzinf = 'US/Central'):
        self.fdend = self.fdend.replace(hour=hrend, minute=minend, second = secstrt, tzinfo = pytz.timezone(tzinf))
        self.ldened = self.ldend.replace(hour=hrend+2, minute = minend, second = secstrt, tzinfo = pytz.timezone(tzinf))
                          
    def setstartDate(self, yr, mnth, dy, tzinf = 'US/Central'):
        self.fdstart = self.fdstart.replace(year = yr, month = mnth, day = dy, tzinfo = pytz.timezone(tzinf))
        self.fdend = self.fdend.replace(year = yr, month = mnth, day = dy, tzinfo = pytz.timezone(tzinf))

    def setendDate(self, yr, mnth, dy, tzinf = 'US/Central'):
        self.ldend = self.ldend.replace(year = yr, month = mnth, day = dy, tzinfo = pytz.timezone(tzinf))

    def addDays(self, days):
        for day in days:
            self.daysofop.append(day.upper())
            
        #make sure the first day of the event
        #is one of the days that it recurs on
        #else continue increasing the date
        while calendar.day_name[self.fdstart.weekday()][:2].upper() not in days:
            print(self.fdstart.weekday())
            self.fdstart = self.fdstart + datetime.timedelta(days =1)

    def addholiDays(self, days):
        for day in days:
            self.holidays.append(day.replace(tzinfo = pytz.timezone('US/Central')))
            
    def name(self):
        return self.name

    def startDay(self):
        return self.fdstart
    
    def endDay(self):
        return self.fdend
    
    def lastDay(self):
        return self.ldend

    def listDays(self):
        return self.daysofop

    def holiDays(self):
        return self.holidays
    
    def locate(self):
        return self.location
