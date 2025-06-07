import streamlit as st
from file_manager import add_uploader, get_data

class SideBar():
    def __init__(self):
        pass

    def render(self):
        with st.sidebar:
            file_uploader = st.file_uploader("Choose a '.csv' file or excel file.")

            df = get_data(file_uploader)
            if df is not None:
                # print(df.shape)
                return df

