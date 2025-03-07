from flask import Flask, request, jsonify 
import numpy as np 
import pickle 

app = Flask(__name__)
with open('./models/model.pkl', 'rb') as file:
    rfc = pickle.load(file)

FEATURE_ORDER = ['latitude', 'longitude', 'garageSpaces', 'hasSpa',
       'numOfPatioAndPorchFeatures', 'lotSizeSqFt', 'avgSchoolRating',
       'MedianStudentsPerTeacher', 'numOfBathrooms', 'numOfBedrooms', 'year_1900-1920', 'year_1920-1940', 'year_1940-1960',
       'year_1960-1980', 'year_1980-2000', 'year_2000-2010', 'year_2010-2021',
       'home_type_Multi Residential', 'home_type_Other',
       'home_type_Single Residential']

def validade_input(data):
    required_fields = ['latitude', 'longitude', 'garageSpaces', 'hasSpa',
       'numOfPatioAndPorchFeatures', 'lotSizeSqFt', 'avgSchoolRating',
       'MedianStudentsPerTeacher', 'numOfBathrooms', 'numOfBedrooms']
    
    for field in required_fields:
        if field not in data:
            return False, f'The Field must be included {field}'
    
    #check the dummy variables 

    year_fields = [f for f in data if f.startswith('year_')]
    home_fields = [f for f in data if f.startswith('home_type_')]

    if sum(data.get(f, 0) for f in year_fields) != 1:
        return False, f'The Year field must be included'
    if sum(data.get(f, 0) for f in home_fields) != 1:
        return False, f'The Home field must be included'

    return True, ''

@app.route('/predict', methods = ['POST'])
def predict():
    try:

        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados JSON necessários"}), 400
        # Validar entrada
        is_valid, error_msg = validade_input(data)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        input_array = np.array([[data.get(field, 0) for field in FEATURE_ORDER]])
        print("Input Array:", input_array)

        prediction = rfc.predict(input_array)
        print("Prediction:", prediction.tolist()[0])
        return jsonify({'prediction': prediction.tolist()[0], 'status': 'sucess'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000, debug = True)