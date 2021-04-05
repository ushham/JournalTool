import datetime as dt
import json
import os
import FileManage as fm
import DataManage as dm
import control as ct

class FileMake:
    filer = fm.FileManage()
    datar = dm.DataManage()
    days_per_month = 30
    days_per_week = 7


    def breaker(self, title, text):
        #Given text and a title, makes a dropdown for a markdown file
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

    def makeyear(self, my_date=dt.date.today()):
        def conv_date(s):
            return dt.datetime.strptime(s, '%Y-%m-%d').date()

        data_base = self.datar.open_base()
        my_month, my_day = my_date.month, my_date.day


        dates = [(conv_date(d['Date']), d['File'], d['Title']) for d in data_base if 
        (conv_date(d['Date']).month == my_month) and 
        (conv_date(d['Date']).day == my_day)]

        self.combinefile('My Year', dates, rev=True)
        return 0

    def makeperiod(self, period, name='Custom', my_date=dt.date.today()):
        def conv_date(s):
            return dt.datetime.strptime(s, '%Y-%m-%d').date()

        if period == None:
            period = self.days_per_week
        data_base = self.datar.open_base()

        dates = [(conv_date(d['Date']), d['File'], d['Title']) for d in data_base if 
        (conv_date(d['Date']) > my_date - dt.timedelta(days = period)) and
        (conv_date(d['Date']) <= my_date)]


        self.combinefile('My ' + name, dates, rev=True)
        return 0
