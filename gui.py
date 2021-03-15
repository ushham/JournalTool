import FileManage as fm
# import DataManage as dm
# import control as ct
import tkinter as tk
import datetime as dt
from tkinter import ttk
from tkcalendar import Calendar, DateEntry


class gui:
    filer = fm.FileManage(0)
    def __init__(self, window):
        self.window = window

        self.initialise()

    def initialise(self):
        for i in range(3):
            window.columnconfigure(i, weight=1, minsize=10)

        for i in range(10):
            window.rowconfigure(i, weight=1, minsize=10)
        
        #Make journal for today
        frame = tk.Frame(master=window, relief=tk.RAISED)
        frame.grid(row=1, column=1, padx=10, pady=10)
        make_jrn = ttk.Button(master=frame, text="Make Entry", command=self.run)
        make_jrn.pack(padx=10, pady=10)

        #Custom date pick option
        frame = tk.Frame(master=window, relief=tk.RAISED)
        frame.grid(row=1, column=2, padx=10, pady=10)
        cust_jrn = ttk.Button(master=frame, text="Custom Date", command=self.cal_pop)
        cust_jrn.pack(padx=10, pady=10)

        #Open todays folder
        frame = tk.Frame(master=window, relief=tk.RAISED)
        frame.grid(row=1, column=3, padx=10, pady=10)
        cust_jrn = ttk.Button(master=frame, text="Open Folder", command=self.filer.open_loc)
        cust_jrn.pack(padx=10, pady=10)
    
    def run(self, date=dt.datetime.today()):
        #make popout with textbox
        def closeme():
            name = entry.get()
            newwin.destroy()
            print('here ' + name)
            self.filer.copytemplate(name, date)

        newwin = tk.Tk()
        newwin.title('Journal Name')
        entry = tk.Entry(newwin)
        entry.pack()

        but = tk.Button(newwin, text='ok', command=closeme)
        but.pack()
        

    def cal_pop(self):
        #pop up calculator to choose date
        def save_date():
            top.destroy()
            self.run(cal.selection_get())

        top = tk.Toplevel(self.window)
        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                    cursor="hand2")
        cal.datetime.today()

        cal.pack(fill="both", expand=True)

        sub = tk.Button(top, text="ok", command=save_date)
        sub.pack()

        return 0



window = tk.Tk()
window.title('')
x = gui(window)
window.mainloop()