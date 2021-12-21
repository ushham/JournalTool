import os
import datetime as dt
import subprocess
import shutil
import control.control as ct

class FileManage:

    def openfile(self, path, parent_folder=True):
        '''Opens a file given the path.

        If argument parent_folder isnt passed, it assumes the path is in the journal folder.
        This function requires manual setting up to work with your own application preferences.

        Parameters
        ----------
        path : str, optional
            file path

        parent_folder : str,
            If false it assumes the path variable is the absolute path and not the journal folder path
        '''
        if parent_folder:
            #Uses obsidian here as it is within the journal vault that I have set up, using the URL feature.
            # To find vault go to: ~/Users/user/Library/Application Support/obsidian/obsidian.json
            vault = "0a4e5e27e9772700"
            bash_string = "open 'obsidian://open?vault=" + vault + "&file=" + path + "'"

        else:
            #If not in journal obsidian vault I want the file to open in the Typewriter app
            file_name = path
            application = "Typewriter"
            bash_string = "open -a " + application + " " + "'" + file_name + "'"

        os.system(bash_string)
    
        return 0

    def readfile(self, path, parent_folder=True):
        if parent_folder:
            file_name = ct.folder + path
        else:
            file_name = path
        
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

    def copytemplate(self, title, date=dt.date.today(), path=''):
        #Given date, copys template to location and saves with name and opens
        year, month, day, m_name = date.strftime('%Y'), date.strftime('%m'), date.strftime('%d'), date.strftime('%b')
        name = year[2:] + month + day
        
        name = name + ' ' + title + ct.ext
        journal_path = year + '/' + month + ' ' + m_name

        if path == '':
            path = ct.folder + journal_path
            if not os.path.exists(path):
                self.makefolder(date)

            path = path + '/' + name

        if not os.path.exists(path):
            shutil.copy(ct.folder + ct.temp, path)

            #Rename title in file
            text = self.readfile(path, False)
            
            lines = text.readlines()
        
            if lines[0] == '# \n':
                lines[0] = '# ' + title + '\n'
                w_file = open(path, 'w')
                w_file.write(''.join(lines))
                w_file.close()

            self.openfile(journal_path + '/' + name)
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
