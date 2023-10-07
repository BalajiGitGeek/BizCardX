from mysql.connector import connect
import streamlit as st

conn = connect(
    host = 'localhost',
    user = 'root',
    password='Balaji@1999'
)
mycursor = conn.cursor()
mycursor.execute('CREATE DATABASE IF NOT EXISTS bizcardx_db')
mycursor.execute('USE bizcardx_db')
mycursor.execute('CREATE TABLE IF NOT EXISTS details(name VARCHAR(35),position VARCHAR(35),email VARCHAR(35),address text,mobile VARCHAR(35),district text,state VARCHAR(35),pincode VARCHAR(20),website VARCHAR(35),company_name VARCHAR(35),image LONGBLOB)')

@st.cache_data
def store_data(card_data):
    mycursor.execute("INSERT INTO details VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(card_data['name'],card_data['designation'],card_data['mail'],card_data['address'],card_data['mobile'],card_data['district'],card_data['state'],card_data['pincode'],card_data['website'],card_data['company_name'],card_data['image']))
    conn.commit()
    return True

def get_name_list():
    name_list = []
    mycursor.execute("select name from details") 
    for each in mycursor.fetchall():
        name_list.append(each[0])
    return name_list

def get_specific_data(selected):
    mycursor.execute(f"SELECT * FROM details WHERE name = '{selected}' LIMIT 1")
    return mycursor.fetchall()

def delete_data(selected):
    mycursor.execute(f"DELETE FROM details WHERE name = '{selected}' LIMIT 1")
    conn.commit()
     
def update_values(selected,name,designation,company,district,mobile,mail,website,address,state,pin):
    mycursor.execute(f"UPDATE DETAILS SET name='{name}',position ='{designation}' ,email ='{mail}' ,address ='{address}' ,mobile ='{mobile}' ,district ='{district}' ,state ='{state}' ,pincode ='{pin}' ,website ='{website}' ,company_name ='{company}'  WHERE name='{selected}' limit 1")
    conn.commit()


