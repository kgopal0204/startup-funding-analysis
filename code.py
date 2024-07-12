import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# from datetime import datetime as dt

st.set_page_config(layout="wide", page_title="StratUp Analysis")

df = pd.read_csv("startup_cleaned.csv")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.strftime("%b")

# st.dataframe(df)
st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox("Select One", ["Overall Analysis", "Startup", "Investor"])


# Overall Analysis Function
def load_overall_analysis():
    col1, col2 = st.columns(2)
    with col1:
        # Total Invested Amount in StartUps
        total = df["amount"].sum()
        st.metric("Total Amount Invested in StartUps", "₹ " + str(total) + " Cr")

    with col2:
        # Average Amount Invested In a StartUp
        avg_amount = round(df.groupby("startup")["amount"].sum().mean(), 2)
        st.metric("Average Amount Invested in  StartUps", "₹ " + str(avg_amount) + " Cr")

    col3, col4 = st.columns(2)
    with col3:
        # Total Funded StartUps
        num_startups = df["startup"].nunique()
        st.metric("Total Funded StartUps", num_startups)

    with col4:
        # Maximum Invested Amount in a StartUp
        max_funding = df.groupby("startup")["amount"].sum().sort_values(ascending=False).head(1)
        st.metric("Maximum Amount Invested by Investors in a StartUp",
                  f"{max_funding.index[0]} : " + "₹ " + str(max_funding.values[0]) + " Cr")

    # Month on Month Analysis
    st.title("Month on Month Analysis")


# investor function
def load_investor_details(investor):
    # load the recent 5 investments of the investor
    st.subheader("👉 Most Recent Investments")
    last5 = df[df["investors"].str.contains(investor)].head(5).iloc[:, [0, 1, 2, 4, 5, 6, 7]]
    st.dataframe(last5)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investments
        st.subheader("👉 Biggest Investments")
        big_series = df[df["investors"].str.contains(investor)].groupby(["startup"])["amount"].sum().sort_values(
            ascending=False).head()
        # bar graph
        fig1, ax1 = plt.subplots()
        ax1.bar(big_series.index, big_series.values)
        st.pyplot(fig1)

    with col2:
        # investment % in verticals
        st.subheader("Investment % in Sectors")
        vertical = df[df["investors"].str.contains(investor)].groupby(["vertical"])["amount"].sum().sort_values(
            ascending=False).head(8)
        # pie plot
        fig2, ax2 = plt.subplots()
        ax2.pie(vertical, labels=vertical.index, autopct="%0.1f%%")
        st.pyplot(fig2)

    col3, col4 = st.columns(2)
    with col3:
        # investment % in rounds
        st.subheader("Investment % in Rounds")
        round = df[df["investors"].str.contains(investor)].groupby(["round"])["amount"].sum().sort_values(
            ascending=False)
        # pie plot
        fig3, ax3 = plt.subplots()
        ax3.pie(round, labels=round.index, autopct="%0.1f%%")
        st.pyplot(fig3)

    with col4:
        # investment % in cities
        st.subheader("Investment % in Cities")
        city = df[df["investors"].str.contains(investor)].groupby(["city"])["amount"].sum().sort_values(ascending=False)
        # pie plot
        fig4, ax4 = plt.subplots()
        ax4.pie(city, labels=city.index, autopct="%0.1f%%")
        st.pyplot(fig4)

        # investment trend in years
    st.subheader("Investment Trend in Years")
    year = df[df["investors"].str.contains(investor)].groupby(["year"])["amount"].sum()
    # line plot
    fig5, ax5 = plt.subplots()
    ax5.plot(year.index, year.values)
    st.pyplot(fig5)


if option == "Overall Analysis":
    st.title("Overall Analysis")
    btn1 = st.sidebar.button("Click for Overall Analysis")
    if btn1:
        load_overall_analysis()

elif option == "Startup":
    st.title("Startups Analysis")
    st.sidebar.selectbox("Select Startup", sorted(df["startup"].unique().tolist()))
    btn2 = st.sidebar.button("Click for Startup Details")
else:
    # st.title("Investors Analysis")
    selected_investor = st.sidebar.selectbox("Select Investor", sorted(set(df["investors"].str.split(",").sum())))
    st.title(selected_investor)
    btn3 = st.sidebar.button("Click for Investor Details")
    if btn3:
        load_investor_details(selected_investor)
