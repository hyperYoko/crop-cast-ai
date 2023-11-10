#! C:/Users/Yoko/AppData/Local/Programs/Python/Python311/python.exe
import sys
sys.path.append("C:/Users/Yoko/AppData/Local/Programs/Python/Python311/Lib/site-packages")

import pandas as pd
import datetime
from bs4 import BeautifulSoup
import pickle
import requests, json 

dist_list = ['AHMEDNAGAR', 'AKOLA', 'AMRAVATI', 'AURANGABAD', 'BEED', 'BHANDARA', 'BULDHANA', 'CHANDRAPUR', 'DHULE', 'GADCHIROLI', 'GONDIA', 'HINGOLI', 'JALGAON', 'JALNA', 'KOLHAPUR', 'LATUR', 'NAGPUR', 'NANDED', 'NANDED', 'NASHIK', 'OSMANABAD', 'PARBHANI', 'PUNE', 'SANGLI', 'SATARA', 'SATARA', 'THANE', 'WARDHA', 'WASHIM', 'YAVATMAL']
crop_list = ['Jowar', 'Bajra', 'Wheat']
soil_list = ['chalky', 'clay', 'loamy', 'sandy', 'silty']


district = sys.argv[1]
Crop = sys.argv[2]
Area = int(sys.argv[3])
soil_type = sys.argv[4]

district = "District:_"+district
Crop = "Crop:_"+Crop
soil_type = "Soil_type:_"+soil_type

api_key = "e5f2f9816cc847be5d9e3971dc1e73d0"

base_url = "http://api.openweathermap.org/data/2.5/weather?"
  
city_name = sys.argv[1]

complete_url = base_url + "appid=" + api_key + "&q=" + city_name 

response = requests.get(complete_url) 
x = response.json() 

y = x["main"] 
temp = y["temp"]-273
humi = y["humidity"]
preci = 10

X = ['Area', 'Temperature', 'Precipitaion', 'Humidity', 'Soil_type:_chalky',
   'Soil_type:_clay', 'Soil_type:_loamy', 'Soil_type:_peaty',
   'Soil_type:_sandy', 'Soil_type:_silt',
   'District:_AHMEDNAGAR', 'District:_AKOLA', 'District:_AMRAVATI',
   'District:_AURANGABAD', 'District:_BEED', 'District:_BHANDARA',
   'District:_BULDHANA', 'District:_CHANDRAPUR', 'District:_DHULE',
   'District:_GADCHIROLI', 'District:_GONDIA', 'District:_HINGOLI',
   'District:_JALGAON', 'District:_JALNA', 'District:_KOLHAPUR',
   'District:_LATUR', 'District:_NAGPUR', 'District:_NANDED',
   'District:_NANDURBAR', 'District:_NASHIK', 'District:_OSMANABAD',
   'District:_PARBHANI', 'District:_PUNE', 'District:_SANGLI',
   'District:_SATARA', 'District:_SOLAPUR', 'District:_THANE',
   'District:_WARDHA', 'District:_WASHIM', 'District:_YAVATMAL',
   'Crop:_Bajra', 'Crop:_Jowar', 'Crop:_Wheat', 'Season:_Kharif',
   'Season:_Rabi', 'Season:_Rabi       ']

index_dict = dict(zip(X,range(len(X))))
vect = {}
for key, val in index_dict.items():
    vect[key] = 0
vect[district] = 1
vect[Crop] = 1
vect[soil_type] = 1
vect['Area'] = Area
vect['Temperature'] = temp
vect['Precipitaion'] = preci
vect['Humidity'] = humi

now = datetime.datetime.today()
season = "Season:_Kharif" if (now.month >= 7 and now.month <= 10) else "Season:_Rabi"
vect[season] = 1


df1 = pd.DataFrame.from_records(vect, index=[0])



import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

df = pd.read_csv('data used.csv')
X = df[['Area', 'Temperature', 'Precipitaion', 'Humidity', 'Soil_type:_chalky',
       'Soil_type:_clay', 'Soil_type:_loamy', 'Soil_type:_peaty',
       'Soil_type:_sandy', 'Soil_type:_silt',
       'District:_AHMEDNAGAR', 'District:_AKOLA', 'District:_AMRAVATI',
       'District:_AURANGABAD', 'District:_BEED', 'District:_BHANDARA',
       'District:_BULDHANA', 'District:_CHANDRAPUR', 'District:_DHULE',
       'District:_GADCHIROLI', 'District:_GONDIA', 'District:_HINGOLI',
       'District:_JALGAON', 'District:_JALNA', 'District:_KOLHAPUR',
       'District:_LATUR', 'District:_NAGPUR', 'District:_NANDED',
       'District:_NANDURBAR', 'District:_NASHIK', 'District:_OSMANABAD',
       'District:_PARBHANI', 'District:_PUNE', 'District:_SANGLI',
       'District:_SATARA', 'District:_SOLAPUR', 'District:_THANE',
       'District:_WARDHA', 'District:_WASHIM', 'District:_YAVATMAL',
       'Crop:_Bajra', 'Crop:_Jowar', 'Crop:_Wheat', 'Season:_Kharif',
       'Season:_Rabi', 'Season:_Rabi']]
y = df['Yield']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.50)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
df1 = sc.fit_transform(df1)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow import keras 
from tensorflow.keras.models import Sequential 
from tensorflow.keras import Input
from tensorflow.keras.layers import Dense, Activation, Flatten

model = Sequential()
model.add(Dense(128, kernel_initializer='normal',input_dim = X_train.shape[1], activation='relu'))
model.add(Dense(256, kernel_initializer='normal',activation='relu'))
model.add(Dense(256, kernel_initializer='normal',activation='relu'))
model.add(Dense(256, kernel_initializer='normal',activation='relu'))
model.add(Dense(1, kernel_initializer='normal',activation='linear'))
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])
from tensorflow.keras.callbacks import ModelCheckpoint
checkpoint_name = 'Weights-{epoch:03d}--{val_loss:.5f}.hdf5' 
checkpoint = ModelCheckpoint(checkpoint_name, monitor='val_loss', verbose = 0, save_best_only = True, mode ='auto', save_format='h5')
callbacks_list = [checkpoint]
model.fit(X_train, y_train, epochs=500, batch_size=32, validation_split = 0.2, callbacks=callbacks_list,verbose = 0)
prediction = abs((model.predict(df1)[0][0])*100)
print("The predicted YIELD for given attributes is approximately: ", (prediction), "tons.")

