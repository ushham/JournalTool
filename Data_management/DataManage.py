import json
import os
import csv
import datetime as dt
import control.control as ct
from collections import Counter

class DataManage:
    title = '# '
    status = 'Status:'
    tags = 'Tags:'
    mood = 'Mood:'
    feel = 'Score:'
    location = 'Location:'

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

            elif self.location in line:
                locs = line.replace(self.location, '')

        #Create dictionary
        dic = {
            'Date': data_date.isoformat(),
            'File': file.replace(ct.folder, ''),
            'Title': tit.strip().capitalize(),
            'Status': [s.strip().capitalize() for s in stat.split(', ')],
            'Tags': [t.strip().capitalize() for t in tag.split('#') if t.strip() != ''],
            'Mood': [m.strip().capitalize() for m in mod.split(', ')],
            'Score': score,
            'Location': {'Name': [ell.strip().capitalize() for ell in locs.split(', ')]}
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
            f.close()
        
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

        self.unique_locs(data)
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

    def word_count(self):
        data = self.open_base()

        #List of words
        words = Counter([d for dt in data for d in dt['Mood'] if d != ''])
        
        ls = words.items()

        path = ct.folder + '/' + ct.word_csv
        with open(path, 'w') as doc:
            doc.write('Word' + ',' + 'Occurance' + '\n')
            for ln in ls:
                doc.write(ln[0] + ',' + str(ln[1]))
                doc.write('\n')
        
        return 0

    def unique_locs(self, data = None):
        def index(location, locs):
            #function to return the index of a given location in the database
            n = 0
            check = False
            while not(check):
                check = True if locs[n][0] == location else False
                idx = n if check == True else 0
                n += 1
            
            return check, idx

        if data == None:
            data = self.open_base()

        #list locations with occurance
        locs = [ell for els in data for ell in els['Location']['Name'] if ell != '']
        visit_date = [[ell, els['Date']] for els in data for ell in els['Location']['Name'] if ell != '']
        
        locs = list(Counter(locs).items())
    
        #Find the latest stay at each location
        latest_visit = []
        for i in locs:
            location = i[0]
            late_date = max([dl[1] for dl in visit_date if dl[0] == location])
            latest_visit.append((location, late_date))

        #Open csv database
        path = ct.folder + '/' + ct.loc_csv
        with open(path, 'r') as doc:
            loc_db = doc.readlines()

        data_hold = [loc_db[0].replace('\n', '')]

        #Update occurance of items and latest visit
        for ln in loc_db[1:]:
            lns = ln.replace('\n', '').split(',')
            location = lns[0]
            check_1, idx_1 = index(location, locs)
            check_2, idx_2 = index(location, latest_visit)
            if check_1 and check_2:
                lns[1] = str(locs[idx_1][1])
                lns[2] = str(latest_visit[idx_2][1])
                new_line = ','.join(lns)
    
                data_hold.append(new_line)
                locs.pop(idx_1)

        #If new items are not in list, add to csv
        for ell in locs:
            new_line = ell[0] + ',' + str(ell[1]) + ',,,,,'
            data_hold.append(new_line)
       
        #Write the data to a new csv
        with open(path, 'w') as doc:
            for ln in data_hold:
                doc.write(ln)
                doc.write('\n')
            doc.close()
        return 0 

    def update_locs(self):
        data = self.open_base()

        #csv of location data
        f = open(ct.folder + '/' + ct.loc_csv)
        reader = csv.reader(f)
        loc_info = list(reader)
        loc_title = [i[0] for i in loc_info]

        for d in data:
            loc = d['Location']['Name']
            if loc[0] != '':
                idxs = [loc_title.index(name) for name in loc]

                new_line = {
                    'Name': loc,
                    'Latitude': [loc_info[i][2] for i in idxs],
                    'Longitude': [loc_info[i][3] for i in idxs],
                    'City': [loc_info[i][4] for i in idxs],
                    'Country': [loc_info[i][5] for i in idxs]
                }
                d['Location'] = new_line
        
        with open(ct.folder + ct.data_b, 'w') as fn:
            json.dump(data, fn)
            
        return 0

    def time_capsule_list(self):
        def time_to_open(date):
            today = dt.datetime.today()
            date_formatted = dt.datetime.strptime(date, '%y%m%d')

            return today >= date_formatted

        def timedelta(d1, d2):
            date1 = dt.datetime.strptime(d1, '%y%m%d')
            date2 = dt.datetime.strptime(d2, '%y%m%d')

            return str((date1 - date2).days)

        def extract_data_from_name(name):
            path = ct.time_cap_folder + '/' + name

            data = name.split(' - ')
            datedue, datebegin = data[0].split(' ')
            name = data[1].replace(ct.ext, '')

            open_time = time_to_open(datedue)
            path_to_write = path if open_time else ''

            return [datedue, datebegin, timedelta(datedue, datebegin), name, str(open_time), path_to_write]

        files = os.listdir(ct.time_cap_folder)
        files.sort()
        
        holder = [['Open Date', 'Date Written', 'Wait Period (Days)', 'Title', 'Time to Open','Path']]
        for f in files:
            if os.path.splitext(f)[1] == ct.ext:
                holder.append(extract_data_from_name(f))

        path = ct.folder + '/' + ct.time_cap_db
        with open(path, 'w') as doc:
            for ln in holder:
                ln_str = ','.join(ln)
                doc.write(ln_str)
                doc.write('\n')
        return 0

