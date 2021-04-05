import json
import os
import math
import datetime as dt
import control as ct
import DataManage as dm
import matplotlib.pyplot as plt


class Visualise:
    manage_data = dm.DataManage()

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
        for day in range((end_date-start_date).days):
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
        for day in range((end_date-start_date).days):
            date = start_date + dt.timedelta(day)

            #Score from the database
            scores = [entry['Score'] for entry in data if dt.date.fromisoformat(entry['Date']) == date]
            
            ave = average(scores)

            if len(scores)==0:
                scores.append(float('NaN'))

            for scr in scores:
                score_data.append((date, scr, ave))

        avescr = self.wk_rolling(score_data)

        plt.plot(*zip(*avescr), color='grey')
        plt.scatter(*zip(*score_data))
        plt.ylim(ct.min_plt, ct.max_plt)
        plt.gcf().autofmt_xdate()
        plt.show()
        return score_data
