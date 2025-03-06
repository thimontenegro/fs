from flask import Flask, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

# Lista de features esperadas na ordem correta
FEATURE_ORDER = [
    'latitude', 'longitude', 'garageSpaces', 'hasSpa',
    'numOfPatioAndPorchFeatures', 'lotSizeSqFt', 'avgSchoolRating',
    'MedianStudentsPerTeacher', 'numOfBathrooms', 'numOfBedrooms',
    'year_1900_1920', 'year_1920_1940', 'year_1940_1960',
    'year_1960_1980', 'year_1980_2000', 'year_2000_2010',
    'year_2010_2021', 'home_type_Multi_Residential',
    'home_type_Other_Non_Residential', 'home_type_Single_Residential'
]

# Carregar recursos (substituir com seus arquivos)
# model = joblib.load('model.pkl')
# scaler = joblib.load('scaler.pkl')

def validate_input(data):
    """Validação manual dos dados de entrada"""
    required_fields = [
        'latitude', 'longitude', 'garageSpaces', 'hasSpa',
        'numOfPatioAndPorchFeatures', 'lotSizeSqFt', 'avgSchoolRating',
        'MedianStudentsPerTeacher', 'numOfBathrooms', 'numOfBedrooms'
    ]
    
    # Verificar campos obrigatórios
    for field in required_fields:
        if field not in data:
            return False, f"Campo obrigatório faltando: {field}"

    # Verificar variáveis dummy
    year_fields = [f for f in data if f.startswith('year_')]
    home_fields = [f for f in data if f.startswith('home_type_')]

    if sum(data.get(f, 0) for f in year_fields) != 1:
        return False, "Deve haver exatamente 1 ano selecionado"
    
    if sum(data.get(f, 0) for f in home_fields) != 1:
        return False, "Deve haver exatamente 1 tipo de residência selecionado"

    return True, ""

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Receber dados JSON
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados JSON necessários"}), 400

        # Validar entrada
        is_valid, error_msg = validate_input(data)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Construir array de features na ordem correta
        input_array = np.array([[data.get(field, 0) for field in FEATURE_ORDER]])

        # Pré-processamento (exemplo)
        # scaled_input = scaler.transform(input_array)

        # Previsão (exemplo mockado)
        prediction = 300000 + (data['numOfBedrooms'] * 20000)

        return jsonify({
            "prediction": round(float(prediction), 2),
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

if __name__ == '__main__':
    # Configurar CORS para desenvolvimento
    from flask_cors import CORS
    CORS(app)
    
    app.run(host='0.0.0.0', port=8000, debug=True)