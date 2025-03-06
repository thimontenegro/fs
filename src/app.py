import streamlit as st 
import requests
import json

st.title('Model Prediction')
"""
'latitude', 'longitude', 'garageSpaces', 'hasSpa',
       'numOfPatioAndPorchFeatures', 'lotSizeSqFt', 'avgSchoolRating',
       'MedianStudentsPerTeacher', 'numOfBathrooms', 'numOfBedrooms',
       'year_1900-1920', 'year_1920-1940', 'year_1940-1960', 'year_1960-1980',
       'year_1980-2000', 'year_2000-2010', 'year_2010-2021',
       'home_type_Multi Residential', 'home_type_Other/Non-Residential',
       'home_type_Single Residential'
"""
#continous variables 
latitude = st.number_input('Latitude', value = 0.0)
longitude = st.number_input('longitude', value = 0.0)
garageSpaces = st.number_input('garageSpaces', value = 0.0)
numOfPatioAndPorchFeatures = st.number_input('numOfPatioAndPorchFeatures', value = 0.0)

lotSizeSqFt = st.number_input('lotSizeSqFt', value = 0.0)
avgSchoolRating = st.number_input('avgSchoolRating', value = 0.0)

MedianStudentsPerTeacher = st.number_input('MedianStudentsPerTeacher', value = 0.0)
numOfBathrooms = st.number_input('numOfBathrooms', value = 0.0)
numOfBedrooms = st.number_input('numOfBedrooms', value = 0.0)
#dummy variables
# Dummy variables
hasSpa = st.selectbox('Has Spa?', ['Yes', 'No'])
hasSpa_value = 1 if hasSpa.lower() == 'yes' else 0

# Year dummy variables
year_house_options = [
    'year_1900-1920', 'year_1920-1940', 'year_1940-1960',
    'year_1960-1980', 'year_1980-2000', 'year_2000-2010', 'year_2010-2021'
]
year_house = st.selectbox('House Year', options=year_house_options)
year_house_dict = {option: 0 for option in year_house_options}
year_house_dict[year_house] = 1

# Home type dummy variables
home_type_options = [
    'home_type_Multi Residential', 'home_type_Other/Non-Residential',
    'home_type_Single Residential'
]
home_type = st.selectbox('Home Type', options=home_type_options)
home_type_dict = {option: 0 for option in home_type_options}
home_type_dict[home_type] = 1
if st.button('Prever Preço'):
    # Construir payload com todos os parâmetros
    payload = {
        'latitude': latitude,
        'longitude': longitude,
        'garageSpaces': garageSpaces,
        'hasSpa': hasSpa_value,
        'numOfPatioAndPorchFeatures': numOfPatioAndPorchFeatures,
        'lotSizeSqFt': lotSizeSqFt,
        'avgSchoolRating': avgSchoolRating,
        'MedianStudentsPerTeacher': MedianStudentsPerTeacher,
        'numOfBathrooms': numOfBathrooms,
        'numOfBedrooms': numOfBedrooms,
        **year_house_dict,
        **home_type_dict
    }
    
    def predict_price(data):
        """Função para fazer a previsão usando a API"""
        url = 'http://localhost:8000/predict'  # Substitua pelo seu endpoint
        headers = {'Content-Type': 'application/json'}
        print(data)
        print(json.dumps(data))
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f'Erro na requisição: {str(e)}')
            return None
        
        # Fazer a previsão
    print(payload)
    result = predict_price(payload)
        
    if result and 'prediction' in result:
        st.success(f'Preço previsto: ${result["prediction"]:,.2f}')
    elif result:
        st.error('Resposta inesperada da API')