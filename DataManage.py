import json
import os
import datetime as dt

class DataManage:
    folder = '/Users/ushhamilton/Documents/02 Journals/Journals/'
    filetype = '.md'
    status = 'Status: '
    tags = 'Tags: '

    def __init__(self, day):
        self.date = day

    def listall(self):
        #List all files in subfolders
        locs = os.walk(self.folder)
        f_loc = []
        for x in locs:
            for f in os.listdir(x[0]):
                if f.endswith(self.filetype):
                    add = x[0] + '/' + f
                    add = add.replace('//', '/')
                    f_loc.append(add)
        return f_loc
    
    def parse_data(self, file, data):
        #Extract date, assuming first 6 letters are the date and we are in the 21st centuary
        data_date = file.split('/')[-1][:6]
        data_date = dt.datetime.strptime(str(20) + data_date, '%Y%m%d')

        lines = data.readlines()
        for line in lines:
            #Extract journal status
            if self.status in line:
                stat = line.replace(self.status, '').strip('\n')
            
            #Extract journal tags
            elif self.tags in line:
                tag = line.replace(self.tags, '').strip('\n')

        return [data_date, stat, tag]

    def make_base(self):
        #open all files and read
        #title, date, status, tags
        files = self.listall()
        print(files)
        for f in files[1:]:
            print(f)
            data = open(f)
            line = self.parse_data(f, data)
        return line

x = DataManage(1)
y = x.make_base()
print(y)