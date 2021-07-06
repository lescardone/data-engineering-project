import pandas as pd
import requests
import json
import pytz
from datetime import datetime
import altair as alt
import streamlit as st
from PIL import Image

# MUST BE FIRST
st.set_page_config(layout="wide")

# FUNCTIONS
@st.cache(suppress_st_warning=True)
def grab_and_process_24_hour(url):
    response = requests.get(url)
    data = json.loads(response.text)
    df = pd.DataFrame(data = data, columns=['reference_timestamp', 'status','current_temp', 'rain', 'humidity'])
    df = format_24_hour_data(df)
    return df

def build_current_df(data):
    df = pd.DataFrame(data = data['current_temp'], 
                                      columns=['temp_min','temp','temp_max','feels_like'],index=[0])
    
    df['humidity'] = data['humidity']
    df['reference_timestamp'] = data['reference_timestamp']
    df['status'] = data['status']
   
    if bool(data['rain']):
        df['rain'] = data['rain']
    else:
        df['rain'] = 0
    return df

def format_current_df(df):
    df['max_temp_C'] = df['temp_min'].map(lambda x: (x-32)*(5/9))
    df['min_temp_C'] = df['temp_max'].map(lambda x: (x-32)*(5/9))
    df['feels_like_C'] = df['feels_like'].map(lambda x: (x-32)*(5/9))
    df['temp_C'] = df['temp'].map(lambda x: (x-32)*(5/9))

    df['time'] = df['reference_timestamp'].map(lambda x: datetime.fromtimestamp(x, tz=pytz.timezone('Asia/Shanghai')))
    df['current_time'] = df['reference_timestamp'].map(lambda x: datetime.fromtimestamp(x, tz=pytz.timezone('US/Central')))
    return(df)

def format_24_hour_data(df):
    # TEMPERATURE CONVERSION
    df['max_temp_C'] = df['current_temp'].map(lambda x: (x['temp_max']-32)*(5/9))
    df['min_temp_C'] = df['current_temp'].map(lambda x: (x['temp_min']-32)*(5/9))
    df['feels_like_C'] = df['current_temp'].map(lambda x: (x['feels_like']-32)*(5/9))
    df['temp_C'] = df['current_temp'].map(lambda x: (x['temp']-32)*(5/9))                                       
    df.drop(columns=['current_temp'],axis=1,inplace=True)
    
    # RAIN
    df['rain_volume_mm'] = df['rain'].map(lambda x: list(x.values()))
    df['rain_volume_mm'] = df['rain_volume_mm'].map(lambda x: x[0] if len(x)==1 else 0)
    df.drop(columns=['rain'],axis=1,inplace=True)
    
    # TIME
    df['time'] = df['reference_timestamp'].map(lambda x: datetime.fromtimestamp(x, tz=pytz.timezone('Asia/Shanghai')))
    
    # SORT
    df.sort_values(by='time',inplace=True)
    return(df)

# SIDEBAR
st.sidebar.title('Current Functionality')
st.sidebar.write('''
I built this webapp as a tool for Shanghai landlords and property managers to easily visualize trends in humidity and temperature.
   
Current Humidity, Temperature, & Status
- Stats are pulled every minute from Open Weather Map API
- Google Firestore houses the documents from the API call
- Most recent document is queried, processed, and displayed
Note: There may be up to a several minute time lag

Humidity Levels Over Past 24 Hours
- most recent documents over a 24 hour period queried and processed
- displays as two graphs
    - a chart color coded by weather status
    - histogram of humidity levels
''')

# API URL TRIGGERS
current = 'https://us-central1-engineer-project-metis.cloudfunctions.net/get_current_json'
past_24 = 'https://us-central1-engineer-project-metis.cloudfunctions.net/get_24_hour_json'

response = requests.get(current)
data = json.loads(response.text)
current_df = build_current_df(data)
current_df = format_current_df(current_df)


# TITLE
shanghai_timestamp = current_df['time'][0]
shanghai_datetime = pd.to_datetime(shanghai_timestamp)
month = shanghai_datetime.strftime('%B')
day = shanghai_datetime.strftime('%d')
year = shanghai_datetime.strftime('%Y')
time = shanghai_datetime.strftime('%H:%M')
weekday = shanghai_datetime.strftime('%A')
st.title(f'SHANGHAI on {weekday}, {month} {day}, {year} at {time}')
st.markdown("""---""")


# BLANK SPACE
st.text('')
st.text('')

# TEMP, HUMIDITY, STATUS
left_column, middle_column, right_column = st.beta_columns(3)
temp = int(current_df['temp_C'])
humid = int(current_df['humidity'])
status = current_df['status'][0]

left_column.markdown(""" # Temperature """)
left_column.header(f'{temp}')
middle_column.markdown(""" # Humidity """)
middle_column.header(f'{humid}%')
right_column.markdown(""" # Status """)
right_column.header(f'{status}')


# BLANK SPACE
st.text('')
st.text('')
st.text('')


# TITLE
st.title('Visualize Humidity Levels Over Past 24 Hours')
left_column, middle_column, right_column = st.beta_columns(3)

# BUTTON TO GENERATE GRAPHS
if middle_column.button('Visualize'):
    st.text('')
    df = grab_and_process_24_hour(past_24)
    df = df[['time','humidity','temp_C','status']].rename(columns={'time':'Time','humidity':'Humidity','temp_C':'Temperature','status':'Status'})

    points = alt.Chart(df).mark_circle().encode(
        x='Time',
        y='Humidity',
        color='Status'
    ).properties(
        height=400,
        title = 'Percent Humidity Over Last 24 Hours').interactive()

    points.configure_title(
    fontSize=1000,
    align='center')

    bars = alt.Chart(df).mark_bar().encode(
        alt.Y('Humidity', bin=True),
        x='count()',
        color='Humidity')

    st.altair_chart(points, use_container_width = True)
    st.altair_chart(bars, use_container_width = True)

# FOOTER
st.text('')
st.text('')
st.text('')
image = Image.open('./shanghai_small.jpg')
st.image(image)
left_column, middle_column, right_column = st.beta_columns(3)
middle_column.markdown('[photo created by 4045](https://www.freepik.com/photos/background)')