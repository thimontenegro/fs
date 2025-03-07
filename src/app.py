import streamlit as st
import requests
import json

st.title('Model Prediction')
"""
'latitude', 'longitude', 'garageSpaces', 'hasSpa',
       'numOfPatioAndPorchFeatures', 'lotSizeSqFt', 'avgSchoolRating',
       'MedianStudentsPerTeacher', 'numOfBathrooms', 'numOfBedrooms',
       'priceRange', 'year_1900-1920', 'year_1920-1940', 'year_1940-1960',
       'year_1960-1980', 'year_1980-2000', 'year_2000-2010', 'year_2010-2021',
       'home_type_Multi Residential', 'home_type_Other',
       'home_type_Single Residential'"
"""
#continuous variables
latitude = st.number_input('Latitude', value = 0.0)
longitude = st.number_input('longitude', value = 0.0)
garageSpaces = st.number_input('garageSpaces', value = 0.0)
numOfPatioAndPorchFeatures = st.number_input('numOfPatioAndPorchFeatures', value = 0.0)
lotSizeSqFt = st.number_input('lotSizeSqFt', value = 0.0)
avgSchoolRating = st.number_input('avgSchoolRating', value = 0.0)
MedianStudentsPerTeacher = st.number_input('MedianStudentsPerTeacher', value = 0.0)
numOfBathrooms = st.number_input('numOfBathrooms', value = 0.0)
numOfBedrooms = st.number_input('numOfBedrooms', value = 0.0)

#has spa dummy variables
hasSpa = st.selectbox('Has Spa?',['Yes','No'])

hasSpa_value = 1 if hasSpa.lower() == 'yes' else 0

# year variable

year_options = ['year_1900-1920', 'year_1920-1940', 'year_1940-1960',
       'year_1960-1980', 'year_1980-2000', 'year_2000-2010', 'year_2010-2021']
years_option  = st.selectbox('Select the year of desire house',options = year_options)

year_dict_values = {option: 0 for option in year_options}
year_dict_values[years_option] = 1
yearhouse_value = year_dict_values[years_option] 
# home type variable

home_type_options = ['home_type_Multi Residential', 'home_type_Other',
       'home_type_Single Residential']
homes_option  = st.selectbox('Select the home type',options = home_type_options)

home_dict_values = {option: 0 for option in home_type_options}
home_dict_values[homes_option] = 1
home_value = home_dict_values[homes_option] 

if st.button('Predict'):
  
    payload = {
    'latitude':latitude,
    'longitude': longitude, 'garageSpaces':garageSpaces, 'hasSpa':hasSpa_value,
       'numOfPatioAndPorchFeatures':numOfPatioAndPorchFeatures, 'lotSizeSqFt':lotSizeSqFt, 'avgSchoolRating':avgSchoolRating,
       'MedianStudentsPerTeacher':MedianStudentsPerTeacher, 'numOfBathrooms':numOfBathrooms, 'numOfBedrooms':numOfBedrooms,
        **year_dict_values,
        **home_dict_values
    }
    
    def predict(data):
        url = 'http://127.0.0.1:8000/predict'
        headers = {'Content-Type': 'application/json'}
        print(data)
        try:
            response = requests.post(url, data = json.dumps(data), headers = headers)
            #response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f'{e}')
            return None

    result = predict(payload)
    print('resultado do retorno')
    print(result)
    if result and 'prediction' in result:
        st.success(f"Price: {result['prediction']}")
    elif result: 
        st.error('Wrong API Call.')

