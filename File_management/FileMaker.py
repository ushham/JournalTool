import datetime as dt
import json
import os
import File_management.FileManage as fm
import Data_management.DataManage as dm
import control.control as ct

class FileMake:
    filer = fm.FileManage()
    datar = dm.DataManage()
    days_per_month = 30
    days_per_week = 7


    def breaker(self, title, text):
        #Given text and a title, makes a dropdown for a markdown file
        text = text.replace('\n', '<br>')
        output = (
            '<details>\n' +
            '<summary>' + title + '</summary>\n' +
            '<br>\n' +
            text.strip() + '\n' +
            '</details>\n'
        )
        return output

    def combinefile(self, name, dates, rev=False):
        #Given dates and path and title (date, path, title), sort dates and make file
        dates_sort = sorted(dates, key = lambda tup: tup[0], reverse=rev)
        hold_str = '# ' + name + '\n'
        for date_it in dates_sort:
            full_text = self.filer.readentry(self.filer.readfile(date_it[1]))

            grouped_txt = self.breaker(date_it[0].strftime('%Y-%m-%d') + ' ' + date_it[2], full_text)
            hold_str = hold_str + '\n' + grouped_txt

        #make file
        path = ct.temp_folder + name + ct.ext
        new_file = open(ct.folder + path, 'w')
        new_file.write(hold_str)
        new_file.close()

        self.filer.openfile(path)
        
        return 0

    def makeyear(self, stat, my_date=dt.date.today()):
        def conv_date(s):
            return dt.datetime.strptime(s, '%Y-%m-%d').date()

        data_base = self.datar.open_base()
        my_month, my_day = my_date.month, my_date.day

        dates = [(conv_date(d['Date']), d['File'], d['Title']) for d in data_base if 
        (conv_date(d['Date']).month == my_month) and 
        (conv_date(d['Date']).day == my_day) and
        ((stat in d['Status']) or stat == 'All')]

        self.combinefile('My Year', dates, rev=True)
        return 0

    def makeperiod(self, period, stat, name='Custom', my_date=dt.date.today()):
        def conv_date(s):
            return dt.datetime.strptime(s, '%Y-%m-%d').date()

        if period == None:
            period = self.days_per_week
        data_base = self.datar.open_base()

        dates = [(conv_date(d['Date']), d['File'], d['Title']) for d in data_base if 
        (conv_date(d['Date']) > my_date - dt.timedelta(days = period)) and
        (conv_date(d['Date']) <= my_date) and
        ((stat in d['Status']) or stat == 'All')]


        self.combinefile('My ' + name, dates, rev=True)
        return 0

    def make_time_capsule(self, date, title, path=ct.time_cap_folder):
        #Time capsule is named as 'yymmdd-future yymmdd title'
        year, month, day = date.strftime('%Y'), date.strftime('%m'), date.strftime('%d')
        today = dt.date.today()
        y, m, d = today.strftime('%Y'), today.strftime('%m'), today.strftime('%d')

        title = year[2:] + month + day + ' ' + y[2:] + m + d + ' - '+ title

        path = path + '/' + title + ct.ext

        self.filer.copytemplate(title, date, path)
        return 0


