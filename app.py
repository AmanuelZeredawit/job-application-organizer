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

    menu = ['Home', 'scrap']
    roles = ['Data scientist','ML Engineer', 'Data Engineer', 'Data Analyst', 'AI developer', 'Software developer', 'IoT Engineer', 'IT Engineer']
    company_types = ('IT','Consulting', 'Non-IT')
    contract_types= ('fixed', 'intern', 'remote', 'temporary' )
    languages = ('English', 'Dutch', 'French', 'Other')
    regions = ['Brussels','Flanders','Wallonia']
    provinces = ['Brussels', 'Flemish', 'Antwerp', 'Brabant', 'West Flanders', 'East Flanders', 'Hainaut', 'Liège', 'Limburg', 'Luxembourg', 'Namur']
    sources = ['linkedin', 'ictjob', 'Stepstone','Talent','other']
    possibilities = ['medium', 'high', 'low']



    today = date.today()

    def read_file(file_name):
        data = pd.read_csv(file_name)
        return data
    
    def is_already_applied():
        pass


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
        #st.write("Home page")
        company_name = st.sidebar.text_input('Company Name *')
        d1= read_file(file_name)
        if d1['Company_name'].str.contains(company_name).any():
            
            #st.write('I think you have already applied to this position')
            custom_notification_box(icon='info', textDisplay='We are almost done with your registration...', externalLink='more info', url='#', styles=styles, key="foo")
            #st.write(d1[d1['company_name'].str.contains(company_name)].head())
        company_type = st.sidebar.radio('Company Type *', company_types, horizontal=True )
        region = st.sidebar.selectbox('Region', regions)
        province =st.sidebar.selectbox('Province', provinces)
        locality = st.sidebar.text_input('Locality')
        role = st.sidebar.selectbox('Role *', roles)
        job_title = st.sidebar.text_input('Job title *', role)
        contract_type = st.sidebar.radio('Contract Type *', contract_types, horizontal=True)
        language = st.multiselect('Language requirements *', languages)
        lan = ' '.join(language)
        source = st.selectbox('Source', sources)
        job_link = st.text_input('Job link','')
        job_requirements = st.text_area('Job Requirements', '')
        job_descripition = st.text_area('Job Description', '')
        possibility = st.selectbox('How well you think fit the job?', possibilities)
        job_entry = {'Date': today, 'Company_name': company_name, 'Company_type': company_type,
                      'Region':region, 'Province': province, 'Locality': locality, 
                      'Role': role,  'Job_title': job_title, 'Contract_type': contract_type,
                      'Source': source, 'Job_link': job_link,'Language': lan, 
                      'Possibility':possibility, 'Status': 'applied', 'Feedback': '',
                      'Job_requirements': job_requirements, 'Job_description': job_descripition}
        
        
        
        if st.button('Save', key='save_btn'):
            #df = pd.DataFrame(job_entry, index=[0])
            with open(file_path, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Date', 'Company_name', 'Company_type','Region', 'Province',
                             'Locality', 'Role', 'Job_title','Contract_type','Source', 
                             'Job_link', 'Language', 'Possibility', 'Status', 'Feedback',
                             'Job_requirements', 'Job_description'])
                if os.path.getsize(file_path) == 0:
                    writer.writeheader()  # Write the header row if the file is empty
                writer.writerow(job_entry)
            print("Dictionary added to the CSV file.")
            df = read_file(file_name)
            st.write(df.tail())        


    elif choice =='scrap':
        st.write("scrapping page")


if __name__ == '__main__':
    main()