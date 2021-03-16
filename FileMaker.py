import datetime as dt
import json
import os
import FileManage as fm

class FileMake:
    filer = fm.FileManage(0)


    def breaker(self, title, text):
        #Given text and a title, makes a dropdown for a markdown file
        output = (
            '<details>\n' +
            '<summary>' + title + '</summary>\n' +
            '<br>\n' +
            text + '\n' +
            '</details>\n'
        )
        return output

    def combinefile(self, name, dates):
        #Given dates and path and title (date, path, title), sort dates and make file
        dates_sort = sorted(dates, key = lambda tup: tup[0])
        hold_str = '# ' + name + '\n'
        for date in dates_sort:
            full_text = self.filer.readentry(self.filer.readfile(date[1]))
            
            grouped_txt = self.breaker(date[2], full_text)
            hold_str = hold_str + '\n' + grouped_txt
        
        return hold_str


x = FileMake()
data = [(dt.date(2021, 3, 10), "2021/03 Mar/210313 Reuben in the park with scones.md", 'tester1'), (dt.date(2021, 3, 1), "2021/03 Mar/210315 Work with a sunset walk.md", 'test2')]
y = x.combinefile('My First Combo', data)

t_file = open('testcomb.md', 'w')
t_file.write(y)
t_file.close()