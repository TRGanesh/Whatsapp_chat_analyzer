# IMPORTING REQUIRED LIBRARIES
import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

def main():
    # SETTING PAGE CONFIGURATION
    st.set_page_config(page_title='Whatsapp Chat Analyzer',layout='wide')

    # SETTING STREAMLIT STYLE
    streamlit_style = """   <style>
                            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');
                            
                            html,body,[class*='css']{
                                font-family:'serif';
                            }
                            </style>
                    """
    st.markdown(streamlit_style,unsafe_allow_html=True)

    # FONT STYLING FOR HEADERS
    def title(string):
            st.markdown(f"<h1 style='color:#e8322e';font-size:40px>{string}</h1>",unsafe_allow_html=True)
    def header(string):
            st.markdown(f"<h2 style='color:#FF00FF';font-size:40px>{string}</h2>",unsafe_allow_html=True)
    def subheader(string):
            st.markdown(f"<h3 style='color:#e5f55b';font-size:40px>{string}</h3>",unsafe_allow_html=True)
    def plot_subheader(string):
            st.markdown(f"<h3 style='color:#41FB3A';font-size:40px>{string}</h3>",unsafe_allow_html=True) 
    def inference_subheader(string):
            st.markdown(f"<h4 style='color:#9933ff';font-size:40px>{string}</h4>",unsafe_allow_html=True)
    def plot_subheader2(string):
            st.markdown(f"<h4 style='color:#ffff80';font-size:40px>{string}</h4>",unsafe_allow_html=True)                               

    st.sidebar.title('Whatsapp Chat Analyzer')

    uploaded_file = st.sidebar.file_uploader('Choose file') # FILE_UPLOADER
    if uploaded_file is not None:
        
        bytes_data = uploaded_file.getvalue()  # READING THE FILE 
        # FROM ABOVE CODE, WE CAN READ FILE IN STREAM FORMAT
        
        data = bytes_data.decode('utf-8') # CONVERTING TO STRING
        
        df = preprocessor.preprocess(data) # GETTING DATAFRAME FROM THAT RAW TEXT DATA 

        st.dataframe(df)    
        
        # FETCHING UNIQUE USERS-->(TO DISPLAY IN SELECT BOX)
        user_list = df['user'].unique().tolist()
        # user_list.remove('group notification') # no group notification in new_processing
        user_list.sort()
        user_list.insert(0,'Overall')
        
        # SELECT BOX IN SIDE BAR
        selected_user = st.sidebar.selectbox('Show analysis with respect to',user_list)
        
        if st.sidebar.button('Show Analysis'):
            
            header('Top Statistics')
            
            # GETTING STATS FROM HELPER FUNCTIONS
            num_messages, words , num_media_messages, num_links = helper.fetch_stats(selected_user,df)
            
            # CREATING A CONTAINER TO DISPLAY THOSE STATS
            container = st.container()
            
            col1,col2,col3,col4 = container.columns(4)
    
            with col1:
                subheader('Total messages')
                st.title(num_messages)
            with col2:
                subheader('Total words')    
                st.title(words)
            with col3:
                subheader('Media Shared')    
                st.title(num_media_messages)    
            with col4:
                subheader('Links Shared')    
                st.title(num_links)   
                
            st.write('- - -')
                
            # MONTHLY TIMELINE
            header('Monthly timeline')
            monthly_timeline = helper.monthly_timeline(selected_user, df) # GETTING DATAFRAME
            
            # PLOTLY EXPRESS AREA PLOT 
            fig = px.area(data_frame=monthly_timeline,x=monthly_timeline['month_year'], y=monthly_timeline['message'], color_discrete_sequence=['#00FFFF'],template='plotly_dark')
                          
            # UPDATING LAYOUT              
            fig.update_layout({'paper_bgcolor':'rgb(87,85,86)'}, # FOR PAPER BG COLOR
                              plot_bgcolor='#404040', # FOR PLOT BG COLOR
                              
                              xaxis=dict(showgrid=False,zeroline=False), # MAKING GRID OFF FOR X AXIS
                              yaxis=dict(showgrid=False,zeroline=False), # MAKING GRID OFF FOR Y AXIS
                              
                              xaxis_title='Date', # CHANGING X-AXIS LABEL NAME
                              yaxis_title='Message count', # CHANGING Y-AXIS LABEL NAME
                              xaxis_title_font=dict(size=15), # CHANGING SIZE OF X-AXIS LABEL NAME
                              yaxis_title_font=dict(size=15), # CHANGING SIZE OF Y-AXIS LABEL NAME
                              xaxis_tickfont=dict(size=15), # CHANGING SIZE OF X-TICKS
                              yaxis_tickfont=dict(size=15) # CHANGING SIZE OF Y-TICKS
                              )
            # LAYOUT FOR HOVER BOX
            fig.update_layout(hoverlabel=dict(
                        bgcolor='black',
                        font_size=15,
                        font_family='Rockwell',
                        font_color='#00FFFF'
                    ))
            st.plotly_chart(fig,use_container_width=True)
            
            st.write('- - -')
            
            # DAILY TIMELINE
            header('Daily timeline')
            daily_timeline = helper.daily_timeline(selected_user, df) # GETTING DATAFRAME
            
            # PLOTLY EXPRESS AREA PLOT 
            fig = px.area(data_frame=daily_timeline,x=daily_timeline['only_date'], y=daily_timeline['message'], color_discrete_sequence=['#00FF00'],template='plotly_dark')
                          
            # UPDATING LAYOUT                    
            fig.update_layout({'paper_bgcolor':'rgb(87,85,86)'}, # FOR PAPER BG COLOR
                              plot_bgcolor='#404040', # FOR PLOT BG COLOR
                              
                              xaxis=dict(showgrid=False,zeroline=False), # MAKING GRID OFF FOR X AXIS
                              yaxis=dict(showgrid=False,zeroline=False),# MAKING GRID OFF FOR Y AXIS
                              
                              xaxis_title='Date', # CHANGING X-AXIS LABEL NAME
                              yaxis_title='Message count', # CHANGING Y-AXIS LABEL NAME
                              xaxis_title_font=dict(size=15), # CHANGING SIZE OF X-AXIS LABEL NAME
                              yaxis_title_font=dict(size=15), # CHANGING SIZE OF Y-AXIS LABEL NAME
                              xaxis_tickfont=dict(size=15), # CHANGING SIZE OF X-TICKS
                              yaxis_tickfont=dict(size=15) # CHANGING SIZE OF Y-TICKS
                              )
            # LAYOUT FOR HOVER BOX
            fig.update_layout(hoverlabel=dict(
                        bgcolor='black',
                        font_size=15,
                        font_family='Rockwell',
                        font_color='#00FF00'
                    ))
            st.plotly_chart(fig,use_container_width=True)
            
            st.write('- - -')
            
            # ACTIVITY MAP
            header('Activity Map')
            col1,col2 = st.columns(2) # 1 COL FOR DAYS,OTHER FOR MONTHS
            
            with col1:
                subheader('Most Active day')
                days_count_df = helper.week_activity_map(selected_user, df)
                # RENAME COLUMNS(index -> Day)
                days_count_df = days_count_df.rename(columns={'index':'Day',
                                              'day_name':'day_name'})
                
                # PLOTLY EXPRESS BAR PLOT
                fig = px.bar(data_frame=days_count_df,x=days_count_df['Day'],y=days_count_df['day_name'])
                
                # UPDATING THE FIG
                fig.update_traces(marker_color='#FFD700')
                fig.update_layout({'paper_bgcolor':'rgb(87,85,86)'}, # FOR PAPER BG COLOR
                              plot_bgcolor='#404040', # FOR PLOT BG COLOR
                              
                              xaxis=dict(showgrid=False,zeroline=False), # MAKING GRID OFF FOR X AXIS
                              yaxis=dict(showgrid=False,zeroline=False),# MAKING GRID OFF FOR Y AXIS
                              
                              xaxis_title='Day', # CHANGING X-AXIS LABEL NAME
                              yaxis_title='Message count', # CHANGING Y-AXIS LABEL NAME
                              xaxis_title_font=dict(size=15), # CHANGING SIZE OF X-AXIS LABEL NAME
                              yaxis_title_font=dict(size=15), # CHANGING SIZE OF Y-AXIS LABEL NAME
                              xaxis_tickfont=dict(size=15), # CHANGING SIZE OF X-TICKS
                              yaxis_tickfont=dict(size=15) # CHANGING SIZE OF Y-TICKS
                              )
                # LAYOUT FOR HOVER BOX
                fig.update_layout(hoverlabel=dict(
                        bgcolor='black',
                        font_size=15,
                        font_family='Rockwell',
                        font_color='#FFD700'
                    ))
            
                st.plotly_chart(fig,use_container_width=True)
                
            with col2:
                subheader('Most Active month')
                months_count_df = helper.month_activity_map(selected_user, df)
                # RENAME COLUMNS(index -> Month)
                months_count_df = months_count_df.rename(columns={'index':'Month',
                                              'day_name':'month'})
                
                # PLOTLY EXPRESS BAR PLOT
                fig = px.bar(data_frame=months_count_df,x=months_count_df['Month'],y=months_count_df['month'])
                
                # UPDATING THE FIG
                fig.update_traces(marker_color='#FF7F50')
                fig.update_layout({'paper_bgcolor':'rgb(87,85,86)'}, # FOR PAPER BG COLOR
                              plot_bgcolor='#404040', # FOR PLOT BG COLOR
                              
                              xaxis=dict(showgrid=False,zeroline=False), # MAKING GRID OFF FOR X AXIS
                              yaxis=dict(showgrid=False,zeroline=False),# MAKING GRID OFF FOR Y AXIS
                              
                              xaxis_title='Month', # CHANGING X-AXIS LABEL NAME
                              yaxis_title='Message count', # CHANGING Y-AXIS LABEL NAME
                              xaxis_title_font=dict(size=15), # CHANGING SIZE OF X-AXIS LABEL NAME
                              yaxis_title_font=dict(size=15), # CHANGING SIZE OF Y-AXIS LABEL NAME
                              xaxis_tickfont=dict(size=15), # CHANGING SIZE OF X-TICKS
                              yaxis_tickfont=dict(size=15) # CHANGING SIZE OF Y-TICKS
                              )
                # LAYOUT FOR HOVER BOX
                fig.update_layout(hoverlabel=dict(
                        bgcolor='black',
                        font_size=15,
                        font_family='Rockwell',
                        font_color='#FF7F50'
                    ))
                
                st.plotly_chart(fig,use_container_width=True)
            
            
            # ACTIVITY HEAT MAP        
            header('Heatmap')
            activity_pt = helper.activity_heatmap(selected_user, df)
            
            plt.style.use('dark_background')  # SETTING BACKGROUND TO DARK
            
            fig,ax = plt.subplots()
            ax = sns.heatmap(activity_pt,cmap='cubehelix')
            ax.tick_params(axis='x', labelsize=8) # CHANGING SIZE OF X TICKS
            ax.tick_params(axis='y', labelsize=8) # CHANGING SIZE OF X TICKS
            
            cbar = ax.collections[0].colorbar # COLLECTING CBAR VALUES
            cbar.ax.tick_params(labelsize=8) # CHANGING THEIR SIZE
            
            plt.xlabel('Time',fontsize=10) # LABELLING X
            plt.ylabel('Day',fontsize=10) # LABELLING Y
           
            st.pyplot(fig)
            
            st.write('- - -')
                
            # ACTIVE USERS(ONLY WHEN THE SELECTED USER IS OVERALL)
            if selected_user=='Overall':
                header('Most Active users')
                x, new_df = helper.most_busy_users(df)
                # RENAMING COLUMNS
                x = x.rename(columns={'index':'User',
                                              'day_name':'user'})
                
                col1,col2 = st.columns((2,1))  # 1 COL TO DISPLAY BAR PLOT,OTHER FOR DATAFRAME
                
                with col1:
                    # BARPLOT
                    fig = px.bar(data_frame=x,x=x['User'],y=x['user'])
                    
                    # UPDATING FIG
                    fig.update_traces(marker_color='#FA234C')
                    fig.update_layout({'paper_bgcolor':'rgb(87,85,86)'}, # FOR PAPER BG COLOR
                              plot_bgcolor='#404040', # FOR PLOT BG COLOR
                              
                              xaxis=dict(showgrid=False,zeroline=False), # MAKING GRID OFF FOR X AXIS
                              yaxis=dict(showgrid=False,zeroline=False),# MAKING GRID OFF FOR Y AXIS
                              
                              xaxis_title='Month', # CHANGING X-AXIS LABEL NAME
                              yaxis_title='Message count', # CHANGING Y-AXIS LABEL NAME
                              xaxis_title_font=dict(size=15), # CHANGING SIZE OF X-AXIS LABEL NAME
                              yaxis_title_font=dict(size=15), # CHANGING SIZE OF Y-AXIS LABEL NAME
                              xaxis_tickfont=dict(size=15), # CHANGING SIZE OF X-TICKS
                              yaxis_tickfont=dict(size=15) # CHANGING SIZE OF Y-TICKS
                              )
                    # LAYOUT FOR HOVER BOX
                    fig.update_layout(hoverlabel=dict(
                        bgcolor='black',
                        font_size=15,
                        font_family='Rockwell',
                        font_color='#FA234C'
                    ))
                    
                    st.plotly_chart(fig,use_container_width=True)
                
                with col2:
                    new_df.index = range(1, len(new_df) + 1) # CHANGING INDEX RANGE OF DATAFRAME
                    st.dataframe(new_df,use_container_width=True)
                    
            st.write('- - -')        
                    
            # WORDCLOUD
            header('WordCloud')
            df_wc = helper.create_wordcloud(selected_user, df)
            
            fig,ax = plt.subplots(dpi=150)
            plt.axis('off')  # GETTING RID OF AXIS
            ax.imshow(df_wc)        
            st.pyplot(fig)
            
            st.write('- - -')
            
            # MOST COMMON WORDS
        
            header('Most Common words')
            most_common_df = helper.most_common_words(selected_user,df) 
            # RENAMING COLUMN
            most_common_df = most_common_df.rename(columns={0:'word',1:'count'})   
        
            #st.dataframe(most_common_df)
            # BAR PLOT
            fig = px.bar(data_frame=most_common_df,y=most_common_df['word'],
                         x=most_common_df['count'],height=500)
            # UPDATING FIG        
            fig.update_traces(marker_color='#790BF8')
            fig.update_layout({'paper_bgcolor':'rgb(87,85,86)'}, # FOR PAPER BG COLOR
                              plot_bgcolor='#404040', # FOR PLOT BG COLOR
                              
                              xaxis=dict(showgrid=False,zeroline=False), # MAKING GRID OFF FOR X AXIS
                              yaxis=dict(showgrid=False,zeroline=False),# MAKING GRID OFF FOR Y AXIS
                              
                              xaxis_title='word count', # CHANGING X-AXIS LABEL NAME
                              yaxis_title='word', # CHANGING Y-AXIS LABEL NAME
                              xaxis_title_font=dict(size=15), # CHANGING SIZE OF X-AXIS LABEL NAME
                              yaxis_title_font=dict(size=15), # CHANGING SIZE OF Y-AXIS LABEL NAME
                              xaxis_tickfont=dict(size=15), # CHANGING SIZE OF X-TICKS
                              yaxis_tickfont=dict(size=15) # CHANGING SIZE OF Y-TICKS
                              )
            # LAYOUT FOR HOVER BOX
            fig.update_layout(hoverlabel=dict(
                        bgcolor='black',
                        font_size=15,
                        font_family='Rockwell',
                        font_color='#790BF8'
                    ))
                    
            st.plotly_chart(fig,use_container_width=True)
            
            st.write('- - -')          
            
            # EMOJI ANALYSIS
            
            emoji_df, top_n_emojis_df = helper.emoji_helper(selected_user, df)   
            
            st.write(' ')
            header('Emoji Analysis')
            
            col1,col2 = st.columns((1,3)) # 1 COL TO SHOW DATAFRAME,OTHER FOR PIE CHART
            
            with col1:
                st.write(' ')
                st.write('  ')
                st.write('  ')
                st.write('  ')
                # RENAMING THE COLUMNS OF EMOJI_DF
                emoji_df = emoji_df.rename(columns={0: 'Emoji', 1: 'Count'})
                # DISAPLAYING THE DF
                st.dataframe(emoji_df,use_container_width=True) 
                
            with col2:
                
                # PIE CHART
                fig = go.Figure(data=[go.Pie(labels=top_n_emojis_df[0],values=top_n_emojis_df[1], hole=0.4,marker=dict(colors=px.colors.sequential.Rainbow_r))])
                # UPDATING FIG
                fig.update_traces(textfont_size=15)
                fig.update_traces(marker=dict(line=dict(color='#FFFFFF',width=0)))
                # Customize the layout
                fig.update_layout(
                    autosize=True,
                    showlegend=False,
                    height=600,  
                    width=600,
                    hoverlabel=dict(
                        bgcolor='black',
                        font_size=15,
                        font_family='Rockwell',
                        font_color='white'
                    )
                )
                st.plotly_chart(fig,use_container_width=True)

                
if __name__ == '__main__':
    main()
                
                
