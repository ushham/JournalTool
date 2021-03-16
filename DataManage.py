import json
import os
import datetime as dt
import control as ct

class DataManage:
    title = '# '
    status = 'Status:'
    tags = 'Tags:'
    mood = 'Mood:'
    feel = 'Score:'

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
        data_date = dt.datetime.strptime(str(20) + data_date, '%Y%m%d').date()

        lines = data.readlines()
        count = 0
        for line in lines:
            count += 1
            #Extract journal status
            if (self.title in line) & (count == 1):
                tit = line.replace(self.title, '')
            elif self.status in line:
                stat = line.replace(self.status, '')
            #Extract journal tags
            elif self.tags in line:
                tag = line.replace(self.tags, '')

            elif self.mood in line:
                mod = line.replace(self.mood, '')
            
            elif self.feel in line:
                score = line.replace(self.feel, '')

        #Create dictionary
        
        dic = {
            'Date': data_date.isoformat(),
            'File': file.replace(ct.folder, ''),
            'Title': tit.capitalize().strip(),
            'Status': [s.capitalize().strip() for s in stat.split(', ')],
            'Tags': [t.capitalize().strip() for t in tag.split(', ')],
            'Mood': [m.capitalize().strip() for m in mod.split(', ')],
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
        #Opens and reads json database
        with open(ct.folder + ct.data_b, 'r') as f:
            data = f.read()
        
        data = json.loads(data)
        return data

    def updt_base(self):
        #Updates exisiting database
        #Used to update day to day rarther than full update
        data = self.open_base()
        files = self.listall()
        prev = [f['File'] for f in data]

        #Removes files already in database
        completed = [f for f in files if f.replace(ct.folder, '') not in prev]
    
        for f in completed:
            if ct.temp not in f:
                newd = open(f)
                line = self.parse_data(f, newd)
                data.append(line)

        with open(ct.folder + ct.data_b, 'w') as f:
            json.dump(data, f)
        return 0

    def list_data(self, data):
        #Given json database makes a list of unique entries of tag and status
        data_base = data

        #Find all status
        status = [s['Status'] for s in data_base]
        status = [item for sublist in status for item in sublist]
        status = list(set(status))

        #Find all Tags
        tags = [(t['Tags'], t['Status']) for t in data_base]
        tagged = [(t, tup[1][0]) for tup in tags for t in tup[0]]
        tagged = list(set(tagged))
        return tagged, status

    def filter_data(self, start=dt.date(2021, 3, 1), end=dt.date.today()):
        data_base = self.open_base()
        dates = [dt.datetime.fromisoformat(f['Date']) for f in data_base]
        dates = [date for date in dates if (date >= start) and (date <= end)]
        return dates

#Convert everything to date rather than datetime
x = DataManage(1)
x.make_base()



