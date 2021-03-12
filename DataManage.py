import json
import os
import datetime as dt
import control as ct

class DataManage:
    title = '# '
    status = 'Status: '
    tags = 'Tags: '
    mood = 'Mood: '
    feel = 'Score: '

    def __init__(self, day):
        self.date = day

    def listall(self):
        #List all files in subfolders
        locs = os.walk(ct.folder)
        f_loc = []
        for x in locs:
            for f in os.listdir(x[0]):
                if f.endswith(ct.ext):
                    add = x[0] + '/' + f
                    add = add.replace('//', '/')
                    f_loc.append(add)
        return f_loc
    
    def parse_data(self, file, data):
        #Extract date, assuming first 6 letters are the date and we are in the 21st centuary
        data_date = file.split('/')[-1][:6]
        data_date = dt.datetime.strptime(str(20) + data_date, '%Y%m%d')

        lines = data.readlines()
        count = 0
        for line in lines:
            count += 1
            #Extract journal status
            if (self.title in line) & (count == 1):
                tit = line.replace(self.title, '').strip('\n')
            elif self.status in line:
                stat = line.replace(self.status, '').strip('\n')
            
            #Extract journal tags
            elif self.tags in line:
                tag = line.replace(self.tags, '').strip('\n')

            elif self.mood in line:
                mod = line.replace(self.mood, '').strip('\n')
            
            elif self.feel in line:
                score = line.replace(self.feel, '').strip('\n')

        return [data_date, tit, stat.split(', '), tag.split(', '), mod.split(', '), int(score)]

    def make_base(self):
        #open all files and read
        #title, date, status, tags
        files = self.listall()
        hold = []
        for f in files:
            if ct.temp not in f:
                data = open(f)
                line = self.parse_data(f, data)
                hold.append(line)
        return hold

x = DataManage(1)
y = x.make_base()
print(y)