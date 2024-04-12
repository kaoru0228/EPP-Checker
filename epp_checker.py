import streamlit as st
import pandas as pd

import csv
import base64


st.set_page_config(
    page_title="EPP Checker",
    page_icon="🐧",
    layout="centered",
    initial_sidebar_state='auto',
    menu_items={
        'About': "This is an application that identifies individuals who may be the biological fathers of children who may have EPP."
    }
)

showSidebarNavigation = False

st.title('EPP Checker')
st.write('**サイドバーからモードを選択してください．**')

st.snow()
# st.balloons()

# st.image('Images/adeliae_001.jpg')

img_path = 'Images/adeliae_001.jpg'
with open(img_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
