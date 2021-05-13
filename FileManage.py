import json
import os
import datetime as dt
import subprocess
import shutil
import control as ct

class FileManage:

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

    def copytemplate(self, title, date=dt.date.today()):
        #Given date, copys template to location and saves with name and opens
        year, month, day, m_name = date.strftime('%Y'), date.strftime('%m'), date.strftime('%d'), date.strftime('%b')
        name = year[2:] + month + day
        if title != '':
            name = name + ' ' + title + ct.ext
            
            path = year + '/' + month + ' ' + m_name 
            if not os.path.exists(ct.folder + path):
                self.makefolder(date)

            if not os.path.exists(ct.folder + path + '/' + name):
                shutil.copy(ct.folder + ct.temp, ct.folder + path)
                os.rename(ct.folder + path + '/' + ct.temp, ct.folder + path + '/' + name)

                #Rename title in file
                text = self.readfile(path + '/' + name)
                
                lines = text.readlines()
            
                if lines[0] == '# \n':
                    lines[0] = '# ' + title + '\n'
                    w_file = open(ct.folder + path + '/' + name, 'w')
                    w_file.write(''.join(lines))
                    w_file.close()

                self.openfile(path + '/' + name)
            else:
                print('Journal: ' + name + ' already exists')
        return 0

    def open_loc(self, date=dt.datetime.today()):
        year, month, m_name = date.strftime('%Y'), date.strftime('%m'), date.strftime('%b')
        path = ct.folder + year + '/' + month + ' ' + m_name
        subprocess.run(['open', path], check=True)

    def readentry(self, text):
        #given full text from entry, strips out just journal text
        lines = text.readlines()
        count = 0
        hold_str = ''
        for line in lines:
            if count >= ct.journal_start:
                hold_str  = hold_str + line
            count += 1
        return hold_str
