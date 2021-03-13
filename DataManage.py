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

        #Create dictionary
        dic = {
            'Date': data_date.isoformat(),
            'File': file.replace(ct.folder, ''),
            'Title': tit.capitalize(),
            'Status': [s.capitalize() for s in stat.split(', ')],
            'Tags': [t.capitalize() for t in tag.split(', ')],
            'Mood': [m.capitalize() for m in mod.split(', ')],
            'Score': int(score)
            }
        return dic

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

        #Write database
        with open(ct.folder + ct.data_b, 'w') as f:
            json.dump(hold, f)
        return 0

    def open_base(self):
        with open(ct.folder + ct.data_b, 'r') as f:
            data = f.read()
        
        data = json.loads(data)
        return data

    def list_data(self, data):
        data_base = data

        #Find all status
        status = [s['Status'] for s in data_base]
        status = [item for sublist in status for item in sublist]
        status = list(set(status))

        #Find all Tags
        tags = [t['Tags'] for t in data_base]
        tags = [item for sublist in tags for item in sublist]
        tags = list(set(tags))
        return status, tags

    def filter_data(self, start='', end=''):
        data_base = self.open_base()
        return 0




x = DataManage(1)
print(x.list_data(x.open_base()))

