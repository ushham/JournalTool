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
                if score != '\n':
                    score = int(score)
                else:
                    score = float('NaN')

        #Create dictionary
        dic = {
            'Date': data_date.isoformat(),
            'File': file.replace(ct.folder, ''),
            'Title': tit.strip().capitalize(),
            'Status': [s.strip().capitalize() for s in stat.split(', ')],
            'Tags': [t.strip().capitalize() for t in tag.split('#') if t.strip() != ''],
            'Mood': [m.strip().capitalize() for m in mod.split(', ')],
            'Score': score
            }
        return dic

    def make_base(self):
        #open all files and read
        #title, date, status, tags
        files = self.listall()
        hold = []
        for f in files:
            if ct.temp not in f and ct.temp_folder not in f:
                data = open(f)
                line = self.parse_data(f, data)
                hold.append(line)

        #Write database
        with open(ct.folder + ct.data_b, 'w') as f:
            json.dump(hold, f)
        return 0

    def open_base(self):
        #checks if database exisits
        if not(os.path.exists(ct.folder + ct.data_b)):
            self.make_base()

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
            if (ct.temp not in f) and (ct.temp_folder not in f):
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

    def item_in_list(self, sublist, full_list, tag_input=True, exact=False):
        #given a sublist, check if any of these elements are in the list
        if tag_input:
            res_list = [i for i in sublist for j in full_list if (i in j) and ((i != '') or not(exact))]
        else:
            res_list = [i for i in sublist if i in full_list]
        check = len(res_list) > 0
        return check

    def filter_data(self, start=ct.first_date, end=dt.date.today(), tags=[], status=[]):
        #Given dates, sort dates and retrieve dates, path and title and pack as tuple
        #Make list of dates
        exact = True
        def conv_date(s):
            return dt.datetime.strptime(s, '%Y-%m-%d').date()
        data_base = self.open_base()
        dates = [dt.date.fromisoformat(f['Date']) for f in data_base]
        dates = [date for date in dates if (date >= start) and (date <= end)]

        if (tags == []) or (status == []):
            pulled_data = self.list_data(data_base)

        if (tags == []):
            tags = pulled_data[0]
            exact = False
        
        if (status == []):
            status = pulled_data[1]

        filt_list = [(conv_date(l['Date']), l['File'], l['Title'], l['Tags']) for l in data_base if 
        (conv_date(l['Date']) in dates) and 
        self.item_in_list(l['Tags'], tags, exact=exact) and 
        self.item_in_list(l['Status'], status, False)]

        return filt_list

    def data_from_tags(self, tags, status=[]):
        #given tags and maybe a status, return all (dates, path, title)
        def conv_date(s):
            return dt.datetime.strptime(s, '%Y-%m-%d').date()

        data_base = self.open_base()
        if status == []:
            status = self.list_data(data_base)[1]

        filt_list = [(conv_date(l['Date']), l['File'], l['Title'], l['Tags']) for l in data_base if
        (self.item_in_list(l['Tags'], tags, exact=True)) and
        (self.item_in_list(l['Status'], status, False))]
 
        return filt_list