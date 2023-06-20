# IMPORTING REQUIRED LIBRARIES
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import re
import string
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

extractor = URLExtract() # URL-EXTRACTOR

# GET STOPWORDS OF ENGLISH
f = open('stop_words_english.txt','r')
stop_words = f.read()

# FUNCTION TO REMOVE EMOJI'S
def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# FUNCTION TO PRE-PROCESS LIST OF WORDS(MESSAGES)
def words_preprocessing(words):
    
        # removing NUMERICAL CHARS from words
        words = [word for word in words if not any(char.isdigit() for char in word)]
    
        # removing EMOJIS from words
        words = [remove_emojis(word) for word in words]
    
        # REGEX PATTERN to match an EMAIL ADDRESS
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        # removing EMAILS contained words
        words = [word for word in words if not re.search(email_pattern,word)]
    
        # Create a TRANSLATION TABLE to remove PUNCTUATION
        translation_table = str.maketrans("", "", string.punctuation)

        # Remove SPACES,PUNCTUATIONS,CONSECUTIVE SPACES from each string in the list
        words = [re.sub(r"\s+", "", word.translate(translation_table)) for word in words]
        
        # removing EMPTY STRINGS
        words = [word for word in words if word.strip() != ""]
    
        return words

# FUNCTION TO GET BASIC STATS FROM CHAT
def fetch_stats(selected_user,df):
    
    # CHANGING DATAFRAME ACCORDING TO SELECTED USER
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    
    num_messages = df.shape[0] # NUMBER OF TOTAL MESSAGES IN CHAT
    
    words = []  # LIST TO STORE TOTAL NUMBER OF WORDS IN CHAT
    for message in df['message']:
        words.extend(message.split()) 
    
    # GETTING NUMBER OF MEDIA FILES SHARED IN CHAT    
    num_media_messages = df[df['message']=='<Media omitted>'].shape[0] 
    
    links = [] # LIST TO STORE NUMBER OF LINKS SHARED IN CHAT
    for message in df['message']:
        links.extend(extractor.find_urls(message))  # USING extractor.find_urls() TO FIND WHETHER A MESSAGE CONTAINS LINK OR NOT  
            
    return num_messages, len(words) ,num_media_messages, len(links)         
    
 # FUNCTION TO RETURN MOST BUSY/ACTIVE USERS IN GROUP   
def most_busy_users(df):
    
    # REMOVE GROUP NOTIFICATIONS
    df = df[df['user']!='group notification']
    
    n_unique = df['user'].nunique() # GETTING NUMBER OF UNIQUE USERS
    if  n_unique > 10:
        x = df['user'].value_counts().head(10)
    else:
        x = df['user'].value_counts().head(n_unique)    
    
    # x HAS USER'S VALUE_COUNTS
    x = x.to_frame().reset_index(drop=False) # x has 2 columns index,user
    
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index()
    
    return x, df # X IS USED TO PLOT BAR,,DF IS DISPLAYED

# FUNCTION TO RETURN WORDCLOUD
def create_wordcloud(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user']==selected_user]
        
    # REMOVE GROUP NOTIFICATIONS
    temp = df[df['user']!='group notification']
    # REMOVE MEDIA OMMITTED 
    temp = temp[temp['message'] != '<Media omitted>']    
    
    words = []  # CREATING A LIST TO STORE THE WORDS
    # REMOVING STOPWORDS FROM MESSAGES AND THEN APPENDING INTO LIST
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                
    words = words_preprocessing(words) # CALLING WORDS_PREPROCESSING FUNCTION
    
    # CALCULATING WORD FREQUENCIES
    word_frequencies = {}  # Dictionary to store word frequencies
    for word in words:
        word_frequencies[word] = word_frequencies.get(word, 0) + 1  # GET FUNCTION
    
    # GENERATING WORCLOUD BASED ON FREQUENCIES(with filtering threshold is 3)  
    df_wc = WordCloud(height=300,width=500,min_font_size=7,
                      colormap='Set2',repeat=False).generate_from_frequencies({word: freq for word,
                                                   freq in word_frequencies.items() if freq >= 1})
    
    return df_wc

# FUNCTION TO RETURN MOST COMMON WORDS
def most_common_words(selected_user,df):
    if selected_user !='Overall':
        df = df[df['user']==selected_user]
    
    # REMOVE GROUP NOTIFICATIONS
    temp = df[df['user']!='group notification']
    # REMOVE MEDIA OMMITTED 
    temp = temp[temp['message'] != '<Media omitted>']
    
    words = []  # CREATING A LIST TO STORE THE WORDS
    # REMOVING STOPWORDS FROM MESSAGES AND THEN APPENDING INTO LIST
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    words = words_preprocessing(words)  # CALLING WORDS_PREPROCESSING FUNCTION
    # CREATING A DATAFRAME OF MOST COMMONLY OCCURING 20 WORDS 
    most_common_df = pd.DataFrame(Counter(words).most_common(20)) # COUNTER().MOST_COMMON         
    
    return most_common_df

# FUNCTION TO RETURN EMOJI COUNTS
def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    
    emojis = [] # LIST TO STORE EMOJIS
    for message in df['message']:
        emoji_tokens = list(emoji.analyze(message))   # ANALYZING MESSAGE FOR EMOJIS
        emojis_list = [token[0] for token in emoji_tokens]  # FROM EMOJI TOKENS GETTING ONLY EMOJI SYMBOLS
        emojis.extend(emojis_list)  # EXTENDING THOSE EMOJIS IN LIST
    
    # len(Counter(emojis)) ==> NUMBER OF UNIQUE EMOJIS
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    # emoji_df CONTAINS EMOJI SYMBOL COLUMN AND THEIR COUNT COLUMN
    
    if len(Counter(emojis)) > 15:
        # LET'S,,THERE ARE MORE THAN 15 DIFFERENT EMOJIS
        top_n_emojis_df = emoji_df.nlargest(15,columns=1) 
    else: # len(Counter(emojis)) < 15 ==> then dispaly all emojis
        top_n_emojis_df = emoji_df       
    
    # LET'S GET THE TOP EMOJI'S PERCENTAGES
    top_n_emojis_df['Percentage'] = (top_n_emojis_df[1] / top_n_emojis_df[1].sum()) * 100

    return emoji_df ,top_n_emojis_df    

# FUNCTIONN TO RETURN MONTHLY TIMELINE
def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]

    # GROUPING THE DATAFRAME BASED ON YEAR AND THEN MONTH
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    
    month_year = []  # CREATING A LIST THAT STORES,MONTH AND YEAR OF A GROUP OF MESSAGES(sent in that month)
    for i in range(timeline.shape[0]):
        month_year.append(timeline.month[i]+'-'+str(timeline.year[i]))
        
    timeline['month_year'] = month_year # MAKING month_year COLUMN(x-axis in plot)
       
    return timeline    

# FUNCTIONN TO RETURN MONTHLY TIMELINE
def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    
    # GROUPING THE DATAFRAME BASED ON DATE
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    
    return daily_timeline

# FUNCTIONN TO RETURN WEEKLY ACTIVITY MAP
def week_activity_map(selected_user,df):
      if selected_user!='Overall':
        df = df[df['user']==selected_user]
      
      # DAY_ORDER ==> TO SORT THE INDEX/ROWS(with KEY) 
      day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
      
      # GETTING VALUE_COUNTS OF EACH DAY(as a dataframe)
      days_count_df = df['day_name'].value_counts().to_frame().reset_index(drop=False) 
      
      # days_count_df HAS 2 COLUMNS day_name,count
      # SORTING BASED ON KEY 
      days_count_df = days_count_df.sort_values(by='day_name', key=lambda x: x.map({day: i for i, day in enumerate(day_order)})) 
        
      return days_count_df
  
# FUNCTIONN TO RETURN MONTHLY ACTIVITY MAP  
def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    
    # DAY_ORDER ==> TO SORT THE INDEX/ROWS(with KEY) 
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    # GETTING VALUE_COUNTS OF EACH DAY(as a dataframe)
    months_count_df = df['month'].value_counts().to_frame().reset_index(drop=False)  
    
    # months_count_df HAS 2 COLUMNS index(having real month names),month(having count),,
    # SORTING BASED ON KEY 
    months_count_df = months_count_df.sort_values(by='month', key=lambda x: x.map({day: i for i, day in enumerate(month_order)}))   
    
    return months_count_df

# FUNCTION TO SORT COLUMNS NAME (00-1,1-2,2-3...)
def sort_columns(column):
    hour1, hour2 = map(int, column.split('-'))
    return (hour1, hour2)

# FUNCTION TO RETURN PIVOT TABLE(with that GENERATING HEATMAP)
def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
        
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # PIVOT TABLE OF DAYS,TIME PERIOD AND COUNT OF MESSAGES ON A PARTICULAR (DAY,TIME PERIOD)
    activity_pt = df.pivot_table(index='day_name',columns='period',
                                 values='message',aggfunc='count').fillna(0)
    
    # SORTING COLUMN NAMES OF activity_pt as (00-1,1-2,2-3...)
    activity_pt = activity_pt.reindex(sorted(activity_pt.columns,key=sort_columns),axis=1)
    # SORTING INDEX(DAYS NAMES)
    activity_pt = activity_pt.sort_index(key=lambda x: x.map({day: i for i, day in enumerate(day_order)}))
    return activity_pt

# VADER SENTIMENT    
def vader(message):
    obj = SentimentIntensityAnalyzer()
    scores = obj.polarity_scores(message)
    return scores['compound']
# TEXTBLOB SENTIMENT
#def textblob(message):
#    # Create a TextBlob object
#    blob = TextBlob(message)

#    # Perform sentiment analysis
#    sentiment = blob.sentiment.polarity
#    return sentiment
# FINAL SENTIMENT
def classify_sentiment(row):
    # Define thresholds and rules for sentiment classification
    positive_threshold = 0.2
    negative_threshold = -0.1
    
    combined_score = row['vader_compound']
    
    if combined_score >= positive_threshold:
        return 'Positive'
    elif combined_score <= negative_threshold:
        return 'Negative'
    else:
        return 'Neutral'
    
# FUCNTION TO RETURN SENTIMENT SCORED DF PER USER
def get_sentiment(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]      
        
    df['vader_compound'] = df['message'].apply(vader)    
    #df['textblob_score'] = df['message'].apply(textblob)
    
    df['sentiment'] = df.apply(classify_sentiment, axis=1)
    
    unstack_df = df.groupby(['user','sentiment']).count()['message'].to_frame().unstack()
    unstack_df.columns = unstack_df.columns.to_flat_index().map('|'.join)
    
    unstack_df.fillna(0,inplace=True)
    
    return unstack_df

    
           
        
        
