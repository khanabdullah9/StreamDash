import streamlit as st
from file_manager import get_data
import analysis

if __name__ == "__main__":
    df = None
    with st.sidebar:
        file_uploader = st.file_uploader("Choose a '.csv' file or excel file.")

        data = get_data(file_uploader)
        if data is not None:
            # print(df.shape)
            df = analysis.feature_engineering(data)
        month_range = analysis.get_month_range(df)
        year_range = analysis.get_year_range(df)

        if month_range is not None:
            st.selectbox(
                "Month:",
                month_range
            )

        if year_range is not None:
            st.selectbox(
                "Year:",
                year_range
            )
    
    if df is not None:
        month_wise_expense = analysis.get_month_wise_expense(df)
        #st.table(month_wise_expense)

        month_insights = analysis.get_month_insights(df, month_num=1, year=2025)
        # st.table(month_insights)

        note_insights = analysis.get_note_insights(df, "petrol", 5,2025)
        # st.table(note_insights)

        q1, q2, q3, max = analysis.get_percentiles(df)
        # st.text(f"Percentiles:{q1},{q2},{q3},{max}")

        prediction = analysis.predict_n_months(df, n=12)
        st.table(prediction)

