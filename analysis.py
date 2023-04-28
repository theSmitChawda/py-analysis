import numpy as np # linear algebra
import pandas as pd # data processing
import os
for dirname, _, filenames in os.walk('/sheridan/fall_2022/analysis_sc'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action="ignore", category=Warning)

#Load Data

files = [file for file in os.listdir('../input/analysis-data')]
for file in files:
    print(file)
    
all_data = pd.DataFrame()

for file in files:
    data = pd.read_csv("../input/analysis-data/" + file)
    all_data = pd.concat([all_data, data])
    
all_data.head()
all_data.shape
all_data.info()
all_data.isnull().sum()
all_data = all_data.dropna(how='all')
all_data.isnull().sum()
all_data.shape
all_data['Bookings'].unique()

#Filter out Text data that not related

filter = all_data['Bookings'] == 'Bookings'
all_data = all_data[~filter]

all_data['Bookings'].unique()
all_data.shape
all_data.dtypes


all_data['Bookings'] = all_data['Bookings'].astype(int)
all_data['Cost'] = all_data['Cost'].astype(float)
all_data['Date'] = pd.to_datetime(all_data['Date'])
all_data.dtypes
all_data['Attendance'] = all_data['Bookings'] * all_data['Cost'] 
all_data.head()

def city(x):
    return x.split(',')[1]
all_data['Campus'] = all_data['Purchase Address'].apply(city)

all_data.head()

all_data['Month'] = all_data['Date'].dt.month
all_data['Day'] = all_data['Date'].dt.dayofweek
all_data['Hour'] = all_data['Date'].dt.hour 

all_data.head()

all_data.groupby('Month')['Attendance'].sum().sort_values(ascending=False)

monthly_sales = all_data.groupby('Month').sum()

plt.figure(figsize=(10,5))

sns.barplot( 
    y=monthly_sales['Attendance'], 
    x=monthly_sales.index, 
    data=monthly_sales)

plt.title('Total Attendance by Months',fontsize =15)
plt.ylabel('Attendance in %',fontsize =12)
plt.xlabel('Months',fontsize =12)

#Find the Total sale by Hour

all_data.groupby('Hour')['Attendance'].sum()

#Visualisation

hourly_sales = all_data.groupby('Hour').sum()

plt.figure(figsize=(10,5))

sns.lineplot( 
    x=hourly_sales.index, 
    y=hourly_sales['Attendance'],
    data=hourly_sales)

plt.xticks(ticks=hourly_sales.index)
plt.title('Total Attendance by Hours',fontsize =15)
plt.xlabel('Hours',fontsize =12)
plt.ylabel('Attendance in %',fontsize =12)
plt.grid(True)
#Find the Total sale by Day

all_data.groupby('Day')['Attendance'].sum()
#Visualisation

daily_sales = all_data.groupby('Day').sum()
daily_sales.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
plt.figure(figsize=(12,5))

sns.lineplot( 
    x=daily_sales.index, 
    y=daily_sales['Attendance'],
    data=daily_sales)

plt.xticks(ticks=daily_sales.index)
plt.title('Daily Order Trend',fontsize =15)
plt.xlabel('Day of Week',fontsize =12)
plt.ylabel('Attendance in %',fontsize =12)
plt.grid(True)

#Find the total sale by Campus

all_data.groupby('Campus')['Attendance'].sum().sort_values(ascending=False)

#Visualisation

city_sales = all_data.groupby('Campus').sum()
plt.figure(figsize=(14,5))

sns.barplot( 
    x=city_sales['Attendance'], 
    y=city_sales.index, 
    data=city_sales,
    palette = "pastel")

plt.title('Total Attendance by Campus',fontsize =20)
plt.xlabel('Attendance in %',fontsize =15)
plt.ylabel('Campus',fontsize =15)

#Find the Quantity ordered of each product

all_data.groupby('Appointment')['Bookings'].count().sort_values(ascending=False)


product_order = all_data.groupby('Appointment').count().sort_values(by='Bookings', ascending=False)[:10]
plt.figure(figsize=(10,5))

sns.barplot( 
    x=product_order['Bookings'], 
    y=product_order.index, 
    data=product_order,
    palette='pastel')

plt.title('Top Subjects',fontsize =18)
plt.xlabel('Total Bookings',fontsize =14)
plt.ylabel('Appointments',fontsize =14)

#Find the duplicate of Booking ID 

df = all_data[all_data['Booking ID'].duplicated(keep=False)]
df

#Make a new column that join product with the same order ID

df['Grouped'] = df.groupby('Booking ID')['Appointment'].transform(lambda x: ','.join(x))
df

#Drop duplicate

df = df[['Booking ID', 'Grouped']].drop_duplicates()
df

#Find the top 10 products that are sold together

df.groupby('Grouped')['Booking ID'].count().sort_values(ascending = False)[:10]


#Visualisation

grouped_product = df.groupby('Grouped').count().sort_values(by='Booking ID',ascending=False)[:10]
plt.figure(figsize=(10,5))

sns.barplot( 
    x=grouped_product['Booking ID'],
    y=grouped_product.index, 
    data=grouped_product,
    palette='pastel')

plt.title('Top 10 Appointments',fontsize=18)
plt.xlabel('Total Booked',fontsize=14)
plt.ylabel('Appointments',fontsize=14)