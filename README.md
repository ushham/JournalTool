# JournalTool
A user interface to manage journal entries, which are written in markdown or other markup text files. The tool also manages an accompanying JSON database.

It has been written for linux and macOS.

## Setup

**control.py** is where the user points at a specific directory, where the journal entries are then automatically saved into subfolders by year -> month.

The user defind template must be put in this directory and named *Template.md*.

**gui.py** is the script to run to access the run, which then allows the user to control the tool.

The code opens a user specified templete to then copy to the subfolder matching the date.

## Requirements

Python 3.9.5 with tkinter installed.

The required packages were chosen to ensure this would run on apple silicon.

