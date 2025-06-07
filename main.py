import streamlit as st
from file_manager import get_data
import analysis
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = None
    month, year, slider_n = 0, 0, 0
    note = ""

    with st.sidebar:
        file_uploader = st.file_uploader("Choose a '.csv' file or excel file.")
        data = get_data(file_uploader)

        if data is not None:
            # print(df.shape)
            df = analysis.feature_engineering(data)

            month_range = analysis.get_month_range(df)
            year_range = analysis.get_year_range(df)

            if month_range is not None:
                month = st.selectbox(
                    "Month:",
                    month_range
                )

            if year_range is not None:
                year = st.selectbox(
                    "Year:",
                    year_range
                )

            slider_n = st.slider("Select # forecasted months:", min_value = 1, max_value = 12)

            note = st.text_input("Enter note: ",placeholder = "Medicines")
    
    if df is not None:
        if year > 0:
            st.subheader("📊 Month-wise Expense Overview")
            month_wise_expense = analysis.get_month_wise_expense(df, year)
            st.bar_chart(month_wise_expense.set_index("Month"))

            year_expense = analysis.get_year_expense(df, year)
            fig, ax = plt.subplots(figsize=(10, 5))
            year_expense.boxplot(column="Amount", by="Month", ax=ax)

            # Enhance plot aesthetics
            ax.set_title(f"Monthly Expense Distribution for {year}")
            ax.set_xlabel("Month")
            ax.set_ylabel("Expense Amount")
            plt.suptitle("")  # Removes default matplotlib title

            # Display plot in Streamlit
            st.pyplot(fig)


        if month > 0 and year > 0:
            st.subheader("📅 Monthly Insights")
            month_insights = analysis.get_month_insights(df, month, year)
            st.table(month_insights)

            if len(note) > 0:
                st.subheader("📅 Note Based Insights")
                note_insights = analysis.get_note_insights(df, note, month, year)
                st.table(note_insights)

            q1, q2, q3, max = analysis.get_percentiles(df, month, year)
            st.subheader("📈 Expense Distribution Percentiles")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("25th Percentile", f"{q1:.2f}")
            col2.metric("50th Percentile (Median)", f"{q2:.2f}")
            col3.metric("75th Percentile", f"{q3:.2f}")
            col4.metric("Max Expense", f"{max:.2f}")

        if slider_n > 0:
            prediction = analysis.predict_n_months(df, n=slider_n)
            st.subheader(f"🔮 Forecast for Next {slider_n} Months")
            st.line_chart(prediction.set_index("ds")[["yhat","yhat_upper","yhat_lower"]])
