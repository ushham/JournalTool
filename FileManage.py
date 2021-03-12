import json
import os
import datetime as dt
import subprocess

class FileManage:

    folder = '/Users/ushhamilton/Documents/02 Journals/Journals/'
    def __init__(self, day):
        self.date = day

    def openfile(self, sub, file):
        file_name = self.folder + sub + file
        subprocess.run(['open', file_name], check=True)
        return 0

    def readfile(self, sub, file):
        file_name = self.folder + sub + file
        data = open(file_name)
        return data


x = FileManage(1)
y = x.readfile('2021/03 Mar/', '210311 Testing the system.md')
print(y.read())
