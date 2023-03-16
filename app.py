import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import csv
import os
from datetime import date
from streamlit_custom_notification_box import custom_notification_box as scnb

def main():

    # set style parameters for button
    styles = {'material-icons':{'color': 'red'},
          'text-icon-link-close-container': {'box-shadow': '#3896de 0px 4px'},
          'notification-text': {'':''},
          'close-button':{'':''},
          'link':{'':''}}
    
    # set variables
    menu = ['Home', 'Register', 'Edit'] 
    roles = ['Data scientist','ML Engineer', 'Data Engineer', 'Data Analyst', 'AI developer', 
             'Software developer', 'IoT Engineer', 'IT Engineer']
    company_types = ('IT','Consulting', 'Non-IT', 'Unknown')
    contract_types= ('fixed', 'intern', 'remote', 'temporary' )
    languages = ('English', 'Dutch', 'French', 'Other')
    regions = ['Brussels','Flanders','Wallonia', 'not mentioned']
    provinces = ['Brussels', 'Flemish', 'Antwerp', 'Brabant', 'West Flanders', 'East Flanders', 
                 'Hainaut', 'Wallonia Brabant', 'Liège', 'Limburg', 'Luxembourg', 'Namur', 'not mentioned']
    sources = ['linkedin', 'indeed','ictjob', 'Stepstone','Talent','becode', 'company portal', 'email', 'other']
    results = ['Negative', 'Positive', 'waiting','Negative after interview']
    column = ['Role', 'Region', 'Province', 'Company_type', 'Status', 'Source']

    positive_feed_back_count = 0
    negative_feed_back_count = 0
    waiting_feed_back_count = 0
    interviews_count = 0
    daily_minimum = 3 # the minimum number of application you can make in a day


    # visualization functions
    def plot_pie_chart(df, column, title):
        
        counts =df[column].value_counts()
        fig1 = px.pie(counts, values=counts.values, names=counts.index, title=title)
        fig1.update_traces(textposition='inside',
                        textinfo='percent+label',
                        showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
            
            

    def plot_bar_chart(df, column_x, column_y, title):
        if column_y =="Applications":
            fig_3 = px.bar(df.groupby([column_x]).size(), width=600, height=400)

        else:
            fig_3 = px.bar(df.groupby([column_x, column_y]).size().unstack(level=1), width=600, height=400)
        fig_3.update_layout(title_text=title, title_x=0.5)
        st.plotly_chart(fig_3, theme="streamlit", use_container_width=True)
    

    def AlertBox(wht_msg):
        styles = {'material-icons':{'color': '#FF0000'},
                'text-icon-link-close-container': {'box-shadow': '#3896de 0px 4px'},
                'notification-text': {'':''},
                'close-button':{'':''},
                'link':{'':''}}

        scnb(icon='info', 
            textDisplay=wht_msg, 
            externalLink='', 
            url='#', 
            styles=styles, 
            key="foo")
    
    def is_minimum_reached(df):  # checks if the minimum daily application limit has been reached
        today_applications_count = df[df['Date'] == str(date.today())].shape[0]
        if today_applications_count < daily_minimum:
            st.sidebar.info(f'You do not meet daily minimum. You make only {today_applications_count}  applications today', icon="ℹ️")
        else:
            st.sidebar.info(f'It is nice day today. You make {today_applications_count} applications', icon="ℹ️")


        


    

    # basic file operations functions
    def read_file(file_name): 
        data = pd.read_csv(file_name, index_col=0)
        return data
    
    def save_file(df):
        df.to_csv('example.csv', index=True)
    
    def delete_job(df, index_number):
        df = df.drop(index=index_number)
        save_file(df)
        st.write('Job entry deleted')
    
    def check_index(df, index_number):
        if index_number not in df.index:
            return False
        else:
            return True

    
    # functions for styling the components
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    def remote_css(url):
        st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

    def icon(icon_name):
        st.sidebar.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
    local_css("style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
    icon("search")



    # Set the file name and path
    file_name = "example.csv"
    file_path = os.path.join(os.getcwd(), file_name)

    # Create a new CSV file
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Company_name', 'Company_type','Region', 'Province',
                             'Locality', 'Role', 'Job_title','Contract_type','Source', 
                             'Job_link', 'Language', 'Possibility', 'Sta', 'Feed',
                             'Job_requirements', 'Job_description'])                 
    


    choice = st.sidebar.selectbox('Menu', menu)
    if choice == 'Home':
        df = read_file(file_name)
        st.subheader('👨🏽‍💻 JOB APPLICATION SUMMARY')

        if df.shape[0] > 0: # only show summary if there is job entry
        
            if df['Status'].str.contains('Positive', case=False).any():
                positive_feed_back_count = df['Status'].value_counts()['Positive']
            if df['Status'].str.contains('Negative', case=False).any():
                negative_feed_back_count = df['Status'].value_counts()['Negative'] 
            if df['Status'].str.contains('interview', case=False).any():
                interviews_count = df['Status'].value_counts()['interview'] 
            if df['Status'].str.contains('waiting', case=False).any():
                waiting_feed_back_count = df['Status'].value_counts()['waiting'] 
            
            # dashboard summary
            col1, col2, col3, col4 = st.columns(4)  
            with col1:
                st.title(df.shape[0])
                st.write("TOTAL")
            with col2:
                feedback_counts =  positive_feed_back_count + negative_feed_back_count
                st.title(feedback_counts)
                st.write("FEEDBACKS")
            with col3:
                st.title(positive_feed_back_count)
                st.write("POSITIVE")
            with col4:
                st.title(interviews_count)
                st.write('INTERVIEWS')
            
            # visualizations
            col1, col2 = st.columns(2)
            with col1:
                st.sidebar.subheader('Pie chart')
                column1 = st.sidebar.selectbox("Select Column for pie chart", column, key='col1_key')
                title1 = "% Applications by " + column1
                plot_pie_chart(df, column1, title1)
                
            with col2:
                counts =df['Region'].value_counts()
                st.sidebar.subheader('Bar chart')
                column_x = st.sidebar.selectbox("Select Column for x", ['Region','Company_type', 'Contract_type', 'Role'], key=column)
                column_y = st.sidebar.radio("Select Column for y", ('Status', 'Applications'), horizontal=True)
                title2 = column_x + ' vs ' + column_y
                plot_bar_chart(df, column_x, column_y, title2)

            # Notify up coming interviews            
            with st.expander(" Upcoming interviews"):
                try:
                    filtered_df = df[df['Interview_date'] >= str(date.today())]
                    filtered_df = filtered_df[['Company_name', 'Interview_date']]
                    st.write(filtered_df)

                except:
                    st.write('error, no interview scheduled at all')

            
            # notify  if you don't hit the daily target
            is_minimum_reached(df)
           

  
        

    elif choice == 'Register':
        company_name = st.sidebar.text_input('Company Name *')
        d1= read_file(file_name)
        company_type = st.sidebar.radio('Company Type *', company_types, horizontal=True )
        region = st.sidebar.selectbox('Region *', regions)
        province =st.sidebar.selectbox('Province *', provinces)
        locality = st.sidebar.text_input('Locality *')
        role = st.sidebar.selectbox('Role *', roles)
        job_title = st.sidebar.text_input('Job title *', role)
        contract_type = st.sidebar.radio('Contract Type *', contract_types, horizontal=True)
        language = st.multiselect('Language requirements *', languages, ['English'])
        lan = ' '.join(language)
        source = st.selectbox('Source', sources)
        job_link = st.text_input('Job link',' ')
        job_requirements = st.text_area('Job Requirements', ' ')
        job_descripition = st.text_area('Job Description', ' ')
        possibility = st.slider('How well do you think you fit the job?', 0,100, 50)
        entry_date= st.date_input("Application date *", date.today())
        job_entry = {'Date': entry_date, 'Company_name': company_name, 'Company_type': company_type,
                      'Region':region, 'Province': province, 'Locality': locality, 
                      'Role': role,  'Job_title': job_title, 'Contract_type': contract_type,
                      'Source': source, 'Job_link': job_link,'Language': lan, 
                      'Possibility':possibility, 'Sta': 'applied', 'Feed': ' ', "Feedback_d": ' ', 
                      'Job_requirements': job_requirements, 'Job_description': job_descripition}
        
        
        
        if st.button('Save', key='save_btn'):
            if len(company_name) > 1:
                df = read_file(file_name)
                df = df.append(job_entry, ignore_index=True)
                st.write("Job saved")
                st.write(df.tail(1))
                save_file(df)
                           
            else:
                st.write('please enter Company name') 

          


    elif choice =='Edit':
        df = read_file(file_name)
        selected = st.sidebar.text_input("", "Search...")
        
        if df.shape[0] > 0:
    
            if st.sidebar.button("OK ", key='okbttn'):
                if df['Company_name'].str.contains(selected, case=False).any():
                    df = df[df['Company_name'].str.contains(selected, case=False)]
                    st.write(df.head())
                else:
                    AlertBox(f'You have not applied  to company with the keyword {selected} yet')
            

            id = st.sidebar.text_input('Application Id', key='id1')
            st.sidebar.subheader("Select method")
            edit = st.sidebar.selectbox('', ['add feedback', 'add interview date', 'delete application'])

            if edit == 'add feedback':

                result = st.sidebar.selectbox('Result', results)
                feedback = st.sidebar.text_area('Feedback details', ' ')
                feedback_date = st.sidebar.date_input(" Date *", date.today())
                update_bttn = st.sidebar.button('Update', key='upbttn')
                st.write(df.tail())

                if update_bttn:       
                    if (len(result)>0)&(len(feedback)>0)& (id.isnumeric()): # check if the fields has values
                        if (int(id)>=0):
                            if check_index(df, int(id)):
                                df.at[int(id), 'Feedback'] = feedback
                                df.at[int(id), 'Status'] = result
                                df.at[int(id), 'Feedback_date'] = feedback_date
                                st.write("Job entry updated")
                                st.write(df.loc[[int(id)]])
                                save_file(df)
                            else:
                                AlertBox('invalid value, enter correct index number')
                        else: 
                            AlertBox('index value must be integer')
                    else:
                        AlertBox("fill the fields with proper values")


            if edit == 'add interview date':
                interview_date = st.sidebar.date_input("Interview date", date.today())
                add_interview = st.sidebar.button('add',key = 'addbttn')
                if add_interview:
                    if id.isnumeric():
                        if (int(id)>=0):
                            if check_index(df, int(id)):
                                df.at[int(id), 'Interview_date'] = interview_date
                                st.write("Job entry updated")
                                st.write(df.loc[[int(id)]])
                                save_file(df)
                            else: AlertBox('invalid value, enter correct index number')
                        else: AlertBox('index value must be integer')
                    else: AlertBox('first enter value for index') 

            if edit == 'delete application':
                delete_bttn = st.sidebar.button('delete', key='delbttn')
                if delete_bttn:

                    if id.isnumeric():
                        if (int(id)>=0):
                            if check_index(df, int(id)):
                                 delete_job(df, int(id))
                            else:
                                AlertBox('invalid value, enter correct index number')
                        else:
                            AlertBox('index value must be integer')
                    else:
                        AlertBox('first enter value for index')
                    


           

if __name__ == '__main__':
    main()