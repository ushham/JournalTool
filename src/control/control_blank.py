import datetime as dt

folder = ''
location_folder = ''

time_cap_folder = ''

temp = 'Template.md'
data_b = 'JournalDatabase.json'
time_cap_db = 'TimeCapsules.md'
word_csv = 'DayWords.csv'
loc_csv = 'Locations.csv'

ext = '.md'
journal_start = 12
temp_folder = 'Temps/'


#first date of useable data
first_date = dt.date(2023, 6, 4)

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

life_expectancy = 80   #<- Last year that is shown in the chart.
standard_weeks_year = 52
weeks_per_year = 52.17857143  #365.25 / 7
days_per_week = 7
dob = ''      #<- Date of birth to be edited.

event = 'Life Event'    #<- The title in the database given to life events

#plotting constants
radius = 150            #Size of circles on scatter graph

portrait_view = False   #When true, the years of life are on the y axis.
