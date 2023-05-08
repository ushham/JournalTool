import datetime as dt

folder = '/Users/ushhamilton/Documents/02_Journals/Journals/'
location_folder = '/Users/ushhamilton/Documents/02 Journals/Locations/'
time_cap_folder = ""

temp = 'Template.md'
data_b = 'JournalDatabase.json'
word_csv = 'DayWords.csv'
loc_csv = 'Locations.csv'

ext = '.md'
journal_start = 12
temp_folder = 'Temps/'


#first date of useable data
first_date = dt.date(2021, 3, 1)

#Plotting constants
min_plt, max_plt = 0, 10

##### Life in weeks constants ####

#Database
db_loc = 'life_database.csv'

col_dic = {
    'date_from' : 0,
    'date_to' : 1,
    'cat' : 2,
    'sub_cat' : 3,
    'colour' : 4
}

life_expectancy = 100   #<- Last year that is shown in the chart.
weeks_per_year = 52
days_per_week = 7
dob = '19/01/1992'      #<- Date of birth to be edited.

#plotting constants
radius = 150            #Size of circles on scatter graph

portrait_view = False   #When true, the years of life are on the y axis.
