import json
import os
import math
import datetime as dt
import control as ct
import DataManage as dm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.collections import PolyCollection

class Visualise:
    manage_data = dm.DataManage()
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_labs = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def wk_rolling(self, data, start_date=ct.first_date, end_date=dt.date.today(), rolling=7):
        def idx_tuple(l, index, value):
            #returns index of value in a list of tuples l, given the index of the search position index.
            for pos,t in enumerate(l):
                if t[index] == value:
                    return pos
        
        def ave_non_nan(lst):
            #given list of numbers and NaNs, find the average not including NaNs
            count, lst_sum = 0, 0
            for l in lst:
                if not(math.isnan(l)):
                    lst_sum += l
                    count += 1
            
            out = lst_sum / count if count > 0 else float('NaN')
            return out

        ave_score = []
        #Create list of average scores for each day (used if there are multiple scores / day)
        for day in range((end_date-start_date).days + 1):
            date = start_date + dt.timedelta(day)

            ave_score.append((date, data[idx_tuple(data, 0, date)][-1]))

        #Find rolling average of list of averages, which were calculated above
        roll_ave = []
        for day in ave_score:
            aves = [num[-1] for num in ave_score if (num[0] <= day[0]) & (num[0] > day[0]-dt.timedelta(rolling))]
            roll_ave.append((day[0], ave_non_nan(aves)))

        return roll_ave   
            
    def show_score(self, start_date=ct.first_date, end_date=dt.date.today()):
        # Opens database and extracts scores between given dates, then displays the data
        def average(lst):
            if len(lst) == 0:
                out = float('NaN')
            else:
                out = sum(lst) / len(lst)
            return out

        #Open database
        data = self.manage_data.open_base()

        #filter data to extract scores
        score_data = []
        for day in range((end_date-start_date).days + 1):
            date = start_date + dt.timedelta(day)

            #Score from the database
            scores = [entry['Score'] for entry in data if dt.date.fromisoformat(entry['Date']) == date]
            
            ave = average(scores)

            if len(scores)==0:
                scores.append(float('NaN'))

            for scr in scores:
                score_data.append((date, scr, ave))

        avescr = self.wk_rolling(score_data)

        plt.figure('Happyness Score')

        plt.plot(*zip(*avescr), color='grey')
        plt.scatter(*zip(*score_data))
        plt.ylim(ct.min_plt, ct.max_plt)
        plt.gcf().autofmt_xdate()
        plt.show()
        return 0

    def graph_use(self, data, status, time_array, start_date=dt.date(2017, 9, 1), end_date=dt.date.today(), rolling = 4):
        #finds the number of entries made over each month, and compares that to the number of days in each month
        #Filter data to count the number of records in each month period
        if status == '':
            status = 'All'
        count_hold = []

        for date in time_array:
            c = sum((dt.date.fromisoformat(item['Date']) >= date[0]) & 
            (dt.date.fromisoformat(item['Date']) <= date[1]) & ((status in item['Status']) or (status == 'All')) 
            for item in data)

            count_hold.append((date[0], c / date[2] * 100))
        
        roll_ave = []
        for d in count_hold:
            aves = [num[1] for num in count_hold if (num[0] <= d[0]) & (num[0] > d[0]-dt.timedelta(rolling * 30))]
            roll_ave.append((d[0], sum(aves) / len(aves)))

        plt.figure('Journal Writing %')
        plt.plot(*zip(*roll_ave), color='grey')
        plt.bar(*zip(*count_hold), width=10)
        plt.gcf().autofmt_xdate()
        plt.title(status)
        plt.show()
        return 0
        
    def stat_maker(self, status, start_date=dt.date(2017, 9, 1), end_date=dt.date.today()):
        #Open database
        data = self.manage_data.open_base()

        #Find totals

        #find monthly figures
        #make an array with the start date of each month, and the number of days in that month
        def month_list(start_date, end_date):
            date_hold = [[start_date, None, None]]
            current_date = start_date
            prev_date = start_date

            #make a list of all the starting dates in each month
            while current_date < end_date:
                if current_date.month != prev_date.month:
                    date_hold.append([current_date, None, None])
                
                prev_date = current_date
                current_date += dt.timedelta(1)

            #make list of number of days in each period
            for i in range(len(date_hold[:-1])):
                date_hold[i][1] = date_hold[i+1][0] - dt.timedelta(1)
                date_hold[i][2] = (date_hold[i+1][0] - date_hold[i][0]).days
            date_hold[-1][1] = end_date
            date_hold[-1][2] = (end_date - date_hold[-1][0]).days + 1

            return date_hold

        #Make graph of total number of journals
        self.graph_use(data, status, month_list(start_date, end_date))

        return 0

    def all_journals(self):
        #Produces a timeline of when journals were made for each year
        #Open database
        data = self.manage_data.open_base()
        
        #Find all dates in database
        dates = [dt.datetime.strptime(d['Date'], '%Y-%m-%d') for d in data]
        dates.sort()
     
        #Format data into (date, date + 1, year as str)
        min_year, max_year, date_len = min(dates).year, max(dates).year, len(dates)

        date_hold = []
        delta = 0.4 #Width of bars
        idx = 0

        #Run through all dates
        while idx < date_len:
            prev_date = dates[idx]
            year = prev_date.year
            i = 1

            #For each date, check how long each streak is (number of consecutive days of journalling)
            while (dates[min(date_len-1, idx + i)] == prev_date + dt.timedelta(days=i)) & (year == dates[min(date_len-1, idx + i)].year) & (idx + i < date_len-1):
                i += 1
            
            next_date = dates[idx + i - 1] if i > 1 else (prev_date + dt.timedelta(days=1))
            p_d, n_d = prev_date.timetuple().tm_yday, next_date.timetuple().tm_yday
            
            #Make bar (Bottom Left, TL, TR, BR, BL) with the year (first year at the bottom)
            v = [
                (p_d, year - min_year - delta),
                (p_d, year - min_year + delta),
                (n_d, year - min_year + delta),
                (n_d, year - min_year - delta),
                (p_d, year - min_year - delta)
            ]
            date_hold.append(v)
            idx += i

        # Plot stuff
        bars = PolyCollection(date_hold)
        fig, ax = plt.subplots(num='Year by Year Comparison')
      
        ax.add_collection(bars)
        ax.autoscale()

        month_locs = [1 if i == 0 else sum(self.month_days[:i])+1 for i in range(len(self.month_days))]
        ax.set_xticks(month_locs)
        ax.set_xticklabels(self.month_labs)

        ax.set_yticks([i for i in range(max_year - min_year + 1)])
        ax.set_yticklabels([str(y) for y in range(min_year, max_year + 1)])
        plt.show()
        return 0
