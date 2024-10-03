import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from altair import value
from pygments.unistring import xid_start

sns.set(style='dark')

#create helper function
def create_weather_df(df):
    weather_df= df.groupby("weathersit").agg({
        'registered':'sum',
        'casual': 'sum',
        'cnt' : 'sum'
    }).reset_index()
    weather_df.rename(columns={
        'cnt': 'total perjalanan',
        'casual': 'perjalanan kasual',
        'registered': 'perjalanan registered'

    }, inplace=True)
    weather_df = weather_df.sort_values('weathersit')
    return weather_df


def create_weekday_tren_df(df):
    weekday_tren_df = df.resample(rule='D', on='dteday').agg({
        'casual': 'sum',
        'registered': 'sum',
        'cnt': 'sum'
    }).reset_index()

    weekday_tren_df.rename(columns={
        'cnt': 'total perjalanan',
        'casual': 'perjalanan kasual',
        'registered': 'perjalanan_registered'
    }, inplace=True)

    weekday_tren_df['weekday'] = weekday_tren_df['dteday'].dt.day_name()
    weekday_tren_df['weekday'] = pd.Categorical(weekday_tren_df['weekday'],
                                                 categories=['Monday',
                                                             'Tuesday',
                                                             'Wednesday',
                                                             'Thursday',
                                                             'Friday',
                                                             'Saturday',
                                                             'Sunday'],
                                                 ordered=True)

    return weekday_tren_df


def create_hour_tren_df(df):
    hour_tren_df = df.groupby(['hr', 'weekday']).agg({
        'casual': 'sum',
        'registered': 'sum',
        'cnt': 'sum'
    }).reset_index()

    hour_tren_df.rename(columns={
        'cnt': 'total perjalanan',
        'casual': 'perjalanan kasual',
        'registered': 'perjalanan registered'
    }, inplace=True)

    return hour_tren_df


hour_df = pd.read_csv("Dashboard/bike_clean_hour1.csv")
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

min_date = hour_df["dteday"].min()   #Membuat filter
max_date = hour_df["dteday"].max()


#Side bar
st.sidebar.subheader("Menu Navigasi")
with st.sidebar:
    st.image("https://st2.depositphotos.com/57698706/50500/v/450/depositphotos_505000244-stock-illustration-orange-bike-in-front-of.jpg",width=200)
    start_date, end_date = st.date_input(
        label='Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour_df[(hour_df["dteday"] >= str(start_date)) &
                (hour_df["dteday"] <= str(end_date))]

weather_df=create_weather_df(main_df)
weekday_tren_df=create_weekday_tren_df(main_df)
hour_tren_df=create_hour_tren_df(main_df)

#Halaman Utama
st.title(":bar_chart: Bike Sharing Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    total_perjalanan=main_df['cnt'].sum()
    st.metric("Total Perjalanan",value=total_perjalanan)

with col2:
    total_registered=main_df['registered'].sum()
    st.metric("Total perjalanan registered",value=total_registered)

with col3:
    total_casual=main_df['casual'].sum()
    st.metric("Total perjalanan casual",value=total_casual)

st.subheader("Jumlah Pengguna di Kondisi Cuaca")

col1, col2, col3 = st.columns(3)

with col1:
    plt.figure(figsize=(4, 3))
    sns.barplot(
        x='weathersit',
        y='cnt',
        data=hour_df,
        ci=None
    )
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Perjalanan')
    plt.title('Jumlah Rental dari Seluruh Kondisi Cuaca')
    plt.xticks(rotation=18)
    st.pyplot(plt)

with col2:
    plt.figure(figsize=(4, 3))
    sns.barplot(
        x='weathersit',
        y='registered',
        data=hour_df,
        ci=None
    )
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Perjalanan registered')
    plt.title('Jumlah Rental dari registered')
    plt.xticks(rotation=18)
    st.pyplot(plt)

with col3:
    plt.figure(figsize=(4, 3))
    sns.barplot(
        x='weathersit',
        y='casual',
        data=hour_df,
        ci=None
    )
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Perjalanan Kasual')
    plt.title('Jumlah Rental dari casual')
    plt.xticks(rotation=18)
    st.pyplot(plt)

st.subheader("Tren Dalam Weekday")

plt.figure(figsize=(8, 4))
sns.barplot(x='weekday', y='total perjalanan', data=weekday_tren_df,ci=None)
plt.title('Weekday - Total Perjalanan')
plt.xlabel('Weekday')
plt.ylabel('total perjalanan')
st.pyplot(plt)

plt.figure(figsize=(8, 4))
sns.barplot(x='weekday', y='perjalanan_registered', data=weekday_tren_df,ci=None)
plt.title('Weekday - Perjalanan Registered')
plt.xlabel('Weekday')
plt.ylabel('Total Perjalanan Registered')
st.pyplot(plt)

# Casual Trips
plt.figure(figsize=(8, 4))
sns.barplot(x='weekday', y='perjalanan kasual', data=weekday_tren_df,ci=None)
plt.title('Weekday - Perjalanan Kasual')
plt.xlabel('Weekday')
plt.ylabel('Perjalanan Kasual')
st.pyplot(plt)


st.subheader("Tren Dalam Hour ")

plt.figure(figsize=(10, 6))
sns.lineplot(x='hr', y='total perjalanan', data=hour_tren_df)
plt.title('Tren Per Jam - Total Perjalanan')
plt.xlabel('Jam')
plt.ylabel('Total Perjalanan')
st.pyplot(plt)

# Registered Trips
plt.figure(figsize=(10, 6))
sns.lineplot(x='hr', y='perjalanan registered', data=hour_tren_df)
plt.title('Tren Per Jam - Perjalanan Terdaftar')
plt.xlabel('Jam')
plt.ylabel('Perjalanan Terdaftar')
st.pyplot(plt)

# Casual Trips
plt.figure(figsize=(10, 6))
sns.lineplot(x='hr', y='perjalanan kasual', data=hour_tren_df)
plt.title('Tren Per Jam - Perjalanan Kasual')
plt.xlabel('Jam')
plt.ylabel('Perjalanan Kasual')
st.pyplot(plt)

st.caption('Copyright (c) Muhammad Heru 2024')


