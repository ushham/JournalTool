import json
import os
import datetime as dt
import subprocess
import shutil
import control as ct

class FileManage:

    ext = '.md'

    def __init__(self, day):
        self.date = day

    def openfile(self, path):
        file_name = ct.folder + path
        subprocess.run(['open', file_name], check=True)
        return 0

    def readfile(self, path):
        file_name = ct.folder + path
        data = open(file_name)
        return data

    def makefolder(self, d):
        #Given date, makes subfolders for file
        year = d.strftime('%Y')
        month_num = d.strftime('%m')
        month_name = d.strftime('%b')
        #check year forder exists
        yr_fold = ct.folder + year
        if not os.path.exists(yr_fold):
            os.makedirs(yr_fold)
        
        #Check if month folder exists
        mth_fold = yr_fold + '/' + month_num + ' ' + month_name
        if not os.path.exists(mth_fold):
            os.makedirs(mth_fold)
        
        return 0

    def copytemplate(self, date):
        #Given date, copys template to location and saves with name and opens
        year, month, day, m_name = date.strftime('%Y'), date.strftime('%m'), date.strftime('%d'), date.strftime('%b')
        name = year[2:] + month + day
        title = input('Journal name: ')
        name = name + ' ' + title + self.ext
        
        path = ct.folder + year + '/' + month + ' ' + m_name 
        if not os.path.exists(path):
            self.makefolder(date)

        print(path)
        shutil.copy(ct.folder + ct.temp, path)
        os.rename(path + '/' + ct.temp, path + '/' + name)
        self.openfile(year + '/' + month + ' ' + m_name + '/' + name)
        return 0


x = FileManage(1)
d = dt.datetime.now()
x.copytemplate(d)
