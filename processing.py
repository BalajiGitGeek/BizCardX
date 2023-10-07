import easyocr
import numpy as np
import streamlit as st
import re
from PIL import Image

@st.cache_data
def load_model():
    reader = easyocr.Reader(['en'])
    return reader

reader = load_model()

def extract_data(uploaded):
    extracted_data = {
        'card_data' : [],
        'image_data' : []
    }
    image = Image.open(uploaded)
    gray_image = image.convert("L")
    extracted_list = reader.readtext(np.array(gray_image))
    for each in extracted_list:
        extracted_data['card_data'].append(each[1])
    image_binary_data = uploaded.read()
    extracted_data['image_data'].append(image_binary_data)
    return extracted_data

@st.cache_data
def extract_specific_data(uploaded):
    data = extract_data(uploaded)
    lst = data["card_data"]
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    pin_pattern = r'\b\d{6,7}\b'
    phone_pattern = r'\b\+?\d+\-\d+-\d+\b'
    districtArr = ['chennai','erode','hydrabad','tirupur','salem']

    card_data = {
        'name':lst[0],
        'position':lst[1],
        'email' : [],
        'address': '',
        'mobile' : [],
        'district' : '',
        'state' : '',
        'pincode' : [],
        'website' : [],
        'company_name':lst[-1],
        'image':data['image_data']
    }
    
    

    for item in lst:
        
        email_matches = re.findall(email_pattern, item)
        card_data['email'].extend(email_matches)

        phone_matches = re.findall(phone_pattern, item)
        card_data['mobile'].extend(phone_matches)

        pin_matches = re.findall(pin_pattern, item)
        card_data['pincode'].extend(pin_matches)
        
        if 'www' in item.lower():
            card_data['website'].append(item)

        elif 'TamilNadu' in item:
            card_data['state'] = 'TamilNadu'
            
        elif 'st' in item.lower():
            card_data['address'] = card_data['address']+item.split(',')[0]
        
        for each_district in districtArr:
            if each_district in item.lower():
                card_data['district'] = card_data['district']+item

    return card_data