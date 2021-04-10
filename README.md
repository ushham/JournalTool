# JournalTool
A user interface to manage journal entries, which are written in markdown or other markup text files. The tool also manages an accompanying JSON database.

It has been written for linux and macOS.
control.py is the sheet requires the user to point the code at a specific folder, where the journal entries are then saved into subfolders by year -> month.

The code opens a templete markdown file to then copy to the subfolder matching the date.

Required (Written to ensure this would run on apple silicon):
* Python 3
* Matplotlib
* tkcalendar
* tkscrolledframe

