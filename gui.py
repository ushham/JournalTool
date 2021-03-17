import FileManage as fm
import DataManage as dm
# import control as ct
import tkinter as tk
import datetime as dt
from tkinter import ttk
from tkcalendar import Calendar, DateEntry


class gui:
    filer = fm.FileManage(0)
    datar = dm.DataManage()
    def __init__(self, window):
        self.window = window

        self.initialise()

    def initialise(self):
        #create full gui
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
        #make popout with textbox to get title of journal
        def closeme(event=None):
            name = entry.get()
            newwin.destroy()
            self.filer.copytemplate(name, date)

        newwin = tk.Tk()
        newwin.title('Journal Name')
        entry = tk.Entry(newwin)
        entry.pack()

        newwin.bind('<Return>', closeme)

        but = tk.Button(newwin, text='ok')
        but.bind('<Button-1>', closeme)
        but.pack()
        return 0    

    def cal_pop(self):
        #pop up calculator to choose date
        def save_date():
            top.destroy()
            self.run(cal.selection_get())

        top = tk.Toplevel(self.window)
        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                    cursor="hand2")
        cal.date.today()

        cal.pack(fill="both", expand=True)

        sub = tk.Button(top, text="ok", command=save_date)
        sub.pack()

        return 0

    def tags_pop(self):
        #Create popout to list all tags to choose from
        def save_tags():
            res = [(t, var.get()) for t, var in output.items()]
            tag_win.destroy()
            print(res)
        
        tag_win = tk.Toplevel()
        tag_win.title('Tag Choices')

        tags, status = self.datar.list_data(self.datar.open_base())
        tg = [r[0] + ' [' + r[1] + ']' for r in tags]

        output = {}

        #Make Checkboxes
        for t in tg:
            var = tk.IntVar()
            l = tk.Checkbutton(tag_win, text=t, variable=var, onvalue=1, offvalue=0)
            output[t] = var
            l.pack(anchor='w')
        btn = tk.Button(tag_win, text='ok', command=save_tags)
        btn.pack()
        return 0



window = tk.Tk()
window.title('')
x = gui(window)
x.tags_pop()
window.mainloop()
