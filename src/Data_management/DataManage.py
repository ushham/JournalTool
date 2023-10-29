import json
import os
import datetime as dt
import src.control.control as ct
from collections import Counter

class DataManage:
    title = '# '
    status = 'Status:'
    tags = 'Tags:'
    mood = 'Mood:'
    feel = 'Score:'
    location = 'Location:'

    lat = "Latitude:"
    lon = "Longitude:"
    city = "City:"
    country = "Country:"

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
        word_count = 0
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

            else:
                # Assumes line is a journal entry if no header is given
                word_count += len(line.split())
                
        #Format the location data
        #This removes the Obsidian backlinking formtting before the text strings are correctly formatted.
        locations = [ell.replace('[[', '').replace(']]', '') for ell in locs.split(', ')]
        locations = [loc.strip() for loc in locations]

        #Create dictionary
        dic = {
            'Date': data_date.isoformat(),
            'File': file.replace(ct.folder, ''),
            'Title': tit.strip().capitalize(),
            'Status': [s.strip().capitalize() for s in stat.split(', ')],
            'Tags': [t.strip().capitalize() for t in tag.split('#') if t.strip() != ''],
            'Mood': [m.strip().capitalize() for m in mod.split(', ')],
            'Score': score,
            'Location': locations,
            'Word_count': word_count
            }
        return dic

    def parsed_location_file(self, file):
        #Parse the location csv file
        file_path = ct.location_folder + file
        file_contents = open(file_path)
        lines = file_contents.readlines()

        for ln in lines:
            if self.lat in ln:
                temp_lat = ''.join(ln.replace(self.lat, "").split())
            elif self.lon in ln:
                temp_lon = ''.join(ln.replace(self.lon, "").split())
            elif self.city in ln:
                temp_city = ln.replace(self.city, "").replace("\n","")
            elif self.country in ln:
                temp_country = ln.replace(self.country, "").replace("\n","")

        return temp_lat, temp_lon, temp_city, temp_country

    def make_base(self):
        #open all files and read
        #title, date, status, tags
        files = self.listall()
        hold = []
        for f in files:
            if (ct.temp not in f) and (ct.temp_folder not in f) and (ct.time_cap_db not in f):
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

        #Previously checked files, excluding those without location information
        prev = [f['File'] for f in data if len(f["Location"]) > 0]

        #Removes files already in database
        completed = [f for f in files if f.replace(ct.folder, '') not in prev]
        for f in completed:
            if (ct.temp not in f) and (ct.temp_folder not in f) and (ct.time_cap_db not in f):
                newd = open(f)
                line = self.parse_data(f, newd)
                data.append(line)

        with open(ct.folder + ct.data_b, 'w') as f:
            json.dump(data, f)

        # self.unique_locs(data)
        self.produce_location_database(data)
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
    
    @staticmethod
    def location_visit_detatils(loc_occ, date_occ, loc):
        latest_date = list()
        for n, l in enumerate(loc_occ):
            if loc in l:
                latest_date.append(date_occ[n])

        loc_count = len(latest_date)
        ld = 0 if loc_count == 0 else max(latest_date)
        return loc_count, ld

    def produce_location_database(self, data=None):
        # Fucntion produced a csv that has all the location data
        if data is None:
            data = self.open_base()

        # Find all location .md files remove file extention
        loc_files = [f[:-3] for f in os.listdir(ct.location_folder)]

        all_loc_occurances = [d["Location"] for d in data]
        all_date_occurances = [d["Date"] for d in data]

        #Parse info from each file
        #Header of file
        location_file = list()

        for ell in loc_files:
            loc_data = self.parsed_location_file(ell + ".md")
            occurance, latest_visit = self.location_visit_detatils(all_loc_occurances, all_date_occurances, ell)

            entry = [ell, str(occurance), latest_visit, loc_data[0], loc_data[1], loc_data[2], loc_data[3]]
            location_file.append(entry) 

        # Sort the list to have "Latest_visit" as most recent
        location_file.sort(key=lambda lf: lf[2], reverse=False)
        location_file.insert(0, ['Location', 'Occurance', 'Latest_Visit', 'Lat', 'Long', 'City', 'Country'])
        
        #save the file
        with open(ct.folder + '/' + ct.loc_csv, 'w') as doc:
            for ln in location_file:
                doc.write(','.join(ln))
                doc.write('\n')
            doc.close()
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
            if open_time:
                path_to_write = '[-->](' + path + ')'
            else:
                path_to_write = ''

            return [datedue, datebegin, timedelta(datedue, datebegin), name, str(open_time), path_to_write]

        files = os.listdir(ct.time_cap_folder)
        files.sort()
        
        holder = [['Open Date', 'Date Written', 'Wait Period (Days)', 'Title', 'Time to Open','Path'], 
                    ['---', '---', '---', '---', '---','---']]
        for f in files:
            if os.path.splitext(f)[1] == ct.ext:
                holder.append(extract_data_from_name(f))

        path = ct.folder + '/' + ct.time_cap_db
        with open(path, 'w') as doc:
            for ln in holder:
                ln_str = '|' + '|'.join(ln) + '|'

                doc.write(ln_str)
                doc.write('\n')
        return 0


if __name__ == "__main__":
    data = DataManage()
    # database = data.make_base()
    print(data.parsed_location_file("Albany.md"))