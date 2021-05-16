import FileManage as fm
import DataManage as dm
import FileMaker as fmk
import DataVisualisation as dv
import tkinter as tk
import datetime as dt
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from tkscrolledframe import ScrolledFrame

class gui:
    filer = fm.FileManage()
    datar = dm.DataManage()
    faker = fmk.FileMake()
    viser = dv.Visualise()

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('')

        self.initialise()

    def initialise(self):
        #create full gui
        for i in range(3):
            self.window.columnconfigure(i, weight=1, minsize=10)

        for i in range(10):
            self.window.rowconfigure(i, weight=1, minsize=10)

        #Find tags and statuses
        self.tags, self.status = self.datar.list_data(self.datar.open_base())
        stat_list = ['All']
        stat_list.extend(self.status)
        stat_list.remove('')

        #Custom date pick option
        frame = tk.Frame(master=self.window, relief=tk.RAISED)
        frame.grid(row=1, column=1, padx=10, pady=10)
        cust_jrn = ttk.Button(master=frame, text=" Journal ", command=self.cal_pop)
        cust_jrn.pack(padx=10, pady=10)

        #Open todays folder
        frame = tk.Frame(master=self.window, relief=tk.RAISED)
        frame.grid(row=1, column=2, padx=10, pady=10)
        cust_jrn = ttk.Button(master=frame, text="Folder Loc", command=self.filer.open_loc)
        cust_jrn.pack(padx=10, pady=10)

        #Journal Stats
        frame = tk.Frame(master=self.window, relief=tk.RAISED)
        frame.grid(row=1, column=3, padx=10, pady=10)
        cust_jrn = ttk.Button(master=frame, text=" Stats ", command=self.mk_stats)
        cust_jrn.pack(padx=10, pady=10)

        #dropdown
        self.drop_var = tk.StringVar(self.window)
        self.drop_var.set(self.status[0])
        self.dropdown = tk.OptionMenu(self.window, self.drop_var, *stat_list)
        self.dropdown.grid(row=2, column=1, padx=10, pady=10)

        #Tags popout
        frame = tk.Frame(master=self.window, relief=tk.RAISED)
        frame.grid(row=2, column=2, padx=10, pady=10)
        cust_jrn = ttk.Button(master=frame, text=" Pick Tags ", command=self.tags_pop)
        cust_jrn.pack(padx=10, pady=10)

        #Make Database
        self.datar.make_base()
        self.datar.word_count()
        frame = tk.Frame(master=self.window, relief=tk.RAISED)
        frame.grid(row=2, column=3, padx=10, pady=10)
        cust_jrn = ttk.Button(master=frame, text=" Update ", command=self.mk_db)
        cust_jrn.pack(padx=10, pady=10)

        #year popout
        frame = tk.Frame(master=self.window, relief=tk.RAISED)
        frame.grid(row=3, column=1, padx=10, pady=10)
        cust_jrn = ttk.Button(master=frame, text=" My Year ", command=self.my_year)
        cust_jrn.pack(padx=10, pady=10)

        #custom popout
        frame = tk.Frame(master=self.window, relief=tk.RAISED)
        frame.grid(row=3, column=2, padx=10, pady=10)
        cust_jrn = ttk.Button(master=frame, text=" My Period ", command=self.my_period)
        cust_jrn.pack(padx=10, pady=10)  

        #graph of scores
        frame = tk.Frame(master=self.window, relief=tk.RAISED)
        frame.grid(row=3, column=3, padx=10, pady=10)
        cust_jrn = ttk.Button(master=frame, text="  Graph  ", command=self.viser.show_score)
        cust_jrn.pack(padx=10, pady=10) 

        self.window.mainloop()
    
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
            res = [r[0] for r in res if r[1] == 1]
            tag_win.destroy()

            data = self.datar.data_from_tags(res)
            name = ', '.join(res)
            self.faker.combinefile('My Tags: ' + name, data)

        def sort_tuple(tup):  
            # sorts the first element of tuples alphebetically 
            tup.sort(key = lambda x: x[0])  
            return tup  
        
        #Find current Status choice
        stat_choose = self.drop_var.get()
        
        #Filter Tag list to only include correct status
        if stat_choose == 'All':
            stat_tags = self.tags
        else:
            stat_tags = [t for t in self.tags if stat_choose in t[1]]

        #Sort List alphabetically
        stat_tags = sort_tuple(stat_tags)

        tag_win = tk.Toplevel()
        tag_win.title('Tag Choices')

        #Scrollbar
        sf = ScrolledFrame(tag_win, width=200, height=500)
        sf.pack(side='bottom', expand=100, fill='x')

        sf.bind_arrow_keys(tag_win)
        sf.bind_scroll_wheel(tag_win)

        inner_frame = sf.display_widget(tk.Frame)

        tg = [[r[0] , ' [' + r[1] + ']'] for r in stat_tags]

        output = {}

        #Make Checkboxes
        for t in tg:
            var = tk.IntVar()
            l = tk.Checkbutton(inner_frame, text=t[0] + t[1], variable=var, onvalue=1, offvalue=0)
            output[t[0]] = var
            l.pack(anchor='w')
        btn = tk.Button(inner_frame, text='ok', command=save_tags)
        btn.pack()
        return 0

    def my_year(self):
        def print_year():
            #Find current Status choice
            stat_choose = self.drop_var.get()
            if stat_choose == '':
                stat_choose = 'All'

            top.destroy()
            self.faker.makeyear(stat_choose, my_date=cal.selection_get())

        top = tk.Toplevel(self.window)
        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                    cursor="hand2")
        cal.date.today()

        cal.pack(fill="both", expand=True)

        sub = tk.Button(top, text="ok", command=print_year)
        sub.pack()

        return 0

    def my_period(self):
        def print_period(event=None):
            #Find current Status choice
            stat_choose = self.drop_var.get()
            if stat_choose == '':
                stat_choose = 'All'
                
            days = fill.get()
            top.destroy()
            val = int(days) if days != '' else None
            self.faker.makeperiod(period=val, stat=stat_choose, my_date=cal.selection_get())

        top = tk.Toplevel(self.window)
        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                    cursor="hand2")
        cal.date.today()

        top.bind('<Return>', print_period)
        cal.pack(fill="both", expand=True)

        fill = tk.Entry(top)
        
        sub = tk.Button(top, text="ok")
        sub.bind('<Button-1>', print_period)
        fill.pack()
        sub.pack()

        return 0

    def mk_db(self):
        #Refresh database and refresh gui
        self.datar.updt_base()
        self.window.destroy()
        self.__init__()

    def mk_stats(self):
        self.viser.stat_maker(self.drop_var.get())
        self.viser.all_journals()
        return 0

if __name__ == "__main__":
    gui()
