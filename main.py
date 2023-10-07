import streamlit as st

st.set_page_config(layout= "wide",
                   initial_sidebar_state= "expanded")

import processing 
from streamlit_option_menu import option_menu
import sql


st.title("BizCardX: Extracting Business Card Data with OCR")

with st.sidebar:
    selected = option_menu(
        menu_title="BizCardX",
        options=["ABOUT PROJECT","STORING DATA","MODIFYING DATA"],
        default_index=0,
    )

if selected == 'STORING DATA':
    uploaded = st.file_uploader('Upload a image file',['jpg','jpeg','png'])

    if uploaded is not None:
        modified_data = {}
        c1,c2,c3 = st.columns([1,2,1])
        with c2:
            st.image(uploaded)

        with st.spinner("Extracting Info"):
            card_data = processing.extract_specific_data(uploaded)

            col_1,col_2 = st.columns([4,4])
            with col_1:
                
                modified_name = st.text_input('Name', card_data["name"])
                modified_designation = st.text_input('Designation', card_data["position"])
                modified_company = st.text_input('Company name', card_data["company_name"])
                modified_district = st.text_input('District', card_data["district"])
                modified_mobile = st.text_input('Mobile', ','.join(card_data["mobile"]))

            with col_2:
                modified_mail = st.text_input('Email', ','.join(card_data["email"]))
                modified_website = st.text_input('Website', ','.join(card_data["website"]))
                modified_address = st.text_input('Address', card_data["address"])
                modified_state = st.text_input('State', card_data["state"])
                modified_pin = st.text_input('Pincode', ','.join(card_data["pincode"]))

                modified_data["name"] = modified_name
                modified_data["designation"]= modified_designation
                modified_data["company_name"]=modified_company
                modified_data["district"]= modified_district
                modified_data["mobile"]= modified_mobile
                modified_data["mail"]= modified_mail
                modified_data["website"]= modified_website
                modified_data["address"]= modified_address
                modified_data["state"]= modified_state
                modified_data["pincode"]= modified_pin
                modified_data["image"]= card_data["image"][0]

            
            rc1,rc2,rc3 = st.columns([4,1,4])
            with rc2:    
                upload = st.button("UPLOAD")
                if upload:
                    db_info = sql.store_data(modified_data)
                    if db_info:
                        with rc3:
                            st.success('SUCCESSFULLY UPLOADED', icon="✅")

if selected == 'MODIFYING DATA':
    selected_name = st.selectbox("select the name to delete/modify",sql.get_name_list())
    sql_card_data = sql.get_specific_data(selected_name)
    col_1,col_2 = st.columns([4,4])
    with col_1:
        
        sql_modified_name = st.text_input('Name', sql_card_data[0][0])
        sql_modified_designation = st.text_input('Designation', sql_card_data[0][1])
        sql_modified_company = st.text_input('Company name', sql_card_data[0][9])
        sql_modified_district = st.text_input('District', sql_card_data[0][5])
        sql_modified_mobile = st.text_input('Mobile', sql_card_data[0][4])

    with col_2:
        sql_modified_mail = st.text_input('Email', sql_card_data[0][2])
        sql_modified_website = st.text_input('Website', sql_card_data[0][8])
        sql_modified_address = st.text_input('Address', sql_card_data[0][3])
        sql_modified_state = st.text_input('State', sql_card_data[0][6])
        sql_modified_pin = st.text_input('Pincode', sql_card_data[0][7])

    rc1,rc2 = st.columns([4,4])
    with rc1:
        modify = st.button('MODIFY')
    with rc2:
        delete = st.button('DELETE')
    
    if delete:
        sql.delete_data(selected_name)
        st.success('DELETED SUCCESSFULLY', icon="✅")

    if modify:
        sql.update_values(selected_name,sql_modified_name,sql_modified_designation,sql_modified_company,sql_modified_district,sql_modified_mobile,sql_modified_mail,sql_modified_website,sql_modified_address,sql_modified_state,sql_modified_pin)

if selected == 'ABOUT PROJECT':
    st.write("""
    The project delivers a Streamlit-based application designed to simplify the process of extracting information from business card images. 
1. Upload a image : Users can conveniently upload business card images, and the application employs easyOCR for automatic extraction.

2. Data Storage: The application seamlessly integrates with a database management system. Users have the capability to save both the uploaded business card images and the extracted information into the database.

3. User-Friendly Interface: Extracted information is presented in a well-organized manner within the interface. Streamlit's widgets facilitate ease of use, and a simple button click enables data storage in the database.

4. Data Modification : Implemented the ability for users to delete a specific business card entry from the database.

""")
