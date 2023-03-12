import streamlit as st
import pandas as pd
from datetime import date
import csv
import os
from streamlit_custom_notification_box import custom_notification_box

def main():

    styles = {'material-icons':{'color': 'red'},
          'text-icon-link-close-container': {'box-shadow': '#3896de 0px 4px'},
          'notification-text': {'':''},
          'close-button':{'':''},
          'link':{'':''}}

    menu = ['Home', 'Update']
    roles = ['Data scientist','ML Engineer', 'Data Engineer', 'Data Analyst', 'AI developer', 
             'Software developer', 'IoT Engineer', 'IT Engineer']
    company_types = ('IT','Consulting', 'Non-IT')
    contract_types= ('fixed', 'intern', 'remote', 'temporary' )
    languages = ('English', 'Dutch', 'French', 'Other')
    regions = ['Brussels','Flanders','Wallonia']
    provinces = ['Brussels', 'Flemish', 'Antwerp', 'Brabant', 'West Flanders', 'East Flanders', 
                 'Hainaut', 'Liège', 'Limburg', 'Luxembourg', 'Namur']
    sources = ['linkedin', 'indeed','ictjob', 'Stepstone','Talent','other']
    possibilities = ['medium', 'high', 'low']
    results = ['Negative', 'Positive', 'waiting','Negative after interview']
    


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
                             'Job_link', 'Language', 'Possibility', 'Status', 'Feedback',
                             'Job_requirements', 'Job_description'])                 
    else:
        print(f"File {file_name} already exists.")


    choice = st.sidebar.selectbox('Menu', menu)
    if choice == 'Home':
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
        possibility = st.slider('How well you think fit the job?', 0,100, 50)
        entry_date= st.date_input("Application date *", date.today())
        job_entry = {'Date': entry_date, 'Company_name': company_name, 'Company_type': company_type,
                      'Region':region, 'Province': province, 'Locality': locality, 
                      'Role': role,  'Job_title': job_title, 'Contract_type': contract_type,
                      'Source': source, 'Job_link': job_link,'Language': lan, 
                      'Possibility':possibility, 'Status': 'applied', 'Feedback': ' ', "Feedback_date": ' ', 
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


    elif choice =='Update':
        selected = st.sidebar.text_input("", "Search...")
        if st.sidebar.button("OK ", key='okbttn'):
            df = read_file(file_name)
            if df['Company_name'].str.contains(selected).any():
                #st.write('already there')
                df = df[df['Company_name'].str.contains(selected)]
                st.write(df.head())
            else:
                st.write(f'You have not applied  to company with the keyword {selected} yet') 

        i = st.sidebar.text_input('Index')
        result = st.sidebar.selectbox('Result', results)
        feedback = st.sidebar.text_area('Feedback details', ' ')
        feedback_date = st.sidebar.date_input(" Date *", date.today())
        update_bttn = st.sidebar.button('Update', key='upbttn')
        delete_bttn = st.sidebar.button('delete', key='delbttn')

        if update_bttn:       
            if (len(result)>0)&(len(feedback)>0)& (i.isnumeric()): # check if the fields has values
                if (int(i)>=0):
                    df1 = read_file(file_name)
                    if check_index(df1, int(i)):
                        df1.at[int(i), 'Feedback *'] = feedback
                        df1.at[int(i), 'Status *'] = result
                        df1.at[int(i), 'Feedback_date *'] = feedback_date
                        st.write(df1.tail(10))
                        st.write("Job entry updated")
                        st.write(df1.loc[[int(i)]])
                        save_file(df1)
                    else:
                         st.write('invalid value, enter correct index number')
                else: 
                    st.write('index value must be integer')
            else:
                st.write("fill the fields with proper values")

        if delete_bttn:
            if i.isnumeric():
                if (int(i)>=0):
                    df1 = read_file(file_name)

                    if check_index(df1, int(i)):
                        delete_job(df1, int(i))
                    else:
                        st.write('invalid value, enter correct index number')
                else:
                    st.write('index value must be integer')
            else:
                st.write('first enter value for index')


    

        
            

if __name__ == '__main__':
    main()