import streamlit as st
import os
import pandas as pd
import traceback

def add_uploader():
    file_uploader = st.file_uploader("Choose a '.csv' or excel file: ")

def get_data(file_uploader):
    try:
        if file_uploader is not None:
            filename = file_uploader.name
            file_extension = os.path.splitext(filename)[1]
        
            df = pd.read_excel(file_uploader) if file_extension == ".xlsx" else pd.read_csv(file_uploader)
            return df
        else:
            print("Could not read file!")
    except Exception:
        print(traceback.format_exc())