# IMPORTING REQUIRED LIBRARIES
from datetime import datetime # FOR HANDLING DATE_TIME DATA
import re # FOR GETTING PATTERNS FROM RAW TEXT
import pandas as pd 

# Function to convert time from 12 hours format into 24 hours format
def convert_to_24h(time_string):
    
    # Remove leading/trailing whitespace and unwanted characters
    cleaned_time = time_string.strip().replace('\u202f', '')
    # Parse input time in 12-hour format
    parsed_time = datetime.strptime(cleaned_time, '%I:%M%p')
    # Format time in 24-hour format
    converted_time = parsed_time.strftime('%H:%M')
    
    return converted_time

# THIS FUNCTION RETURNS DATAFRAME FROM TEXT FILE
def preprocess(data):
    
    # DATA ==> RAW CHAT TEXT FILE,,,HAS LINES ,, EACH LINE HAVING DATE_TIME AND MESSAGE
    
    # REGEX PATTERN TO FIND DATE_TIME IN RAW TEXT FILE
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2})(\s*(AM|PM))?\s*-\s*(.*?):\s*(.*)'
    
    splitted_data = re.findall(pattern,data,flags=re.IGNORECASE)
    
    date_time = [tup[0] for tup in splitted_data]
    am_pm = [tup[1] for tup in splitted_data]
    user = [tup[3] for tup in splitted_data]
    message = [tup[4] for tup in splitted_data]

    df = pd.DataFrame({'date_time':date_time,
             'am_pm':am_pm,
             'user':user,
             'message':message})
    
    df['date_time'] = df['date_time'] + ' ' + df['am_pm']
    df.drop(columns='am_pm',inplace=True)
    
    df[['date','time']] = df['date_time'].str.split(',',expand=True)
    
    df['date_time'] = pd.to_datetime(df['date_time'])
    
    if any(df['time'].str.contains('AM')):
        df['time'] = df['time'].str.replace(' ','').apply(convert_to_24h)
        
    df['year'] = df['date_time'].dt.year
    df['month_num'] = df['date_time'].dt.month
    df['month'] = df['date_time'].dt.month_name()
    df['day'] = df['date_time'].dt.day
    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute
    df['only_date'] = df['date_time'].dt.date
    df['day_name'] = df['date_time'].dt.day_name()   
    
    period = []

    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' +str(hour+1))
        else:
            period.append(str(hour) + '-' + str(hour+1))
            
    df['period'] = period         
    
    df.loc[df['user'] == '.', 'user'] = 'you'  
    
    return df