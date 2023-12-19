from flask import Flask, request, jsonify
import pandas as pd
from pycaret.regression import load_model
from pycaret.regression import predict_model
from datetime import datetime

modelo_a = load_model("../../models/modelo_final_a")
modelo_b = load_model("../../models/modelo_final_b")
modelo_c = load_model("../../models/modelo_final_c")

app = Flask(__name__)

@app.route('/predictA', methods=['POST'])
def predictA():
    data = request.get_json()
    print(data)
    print('Type data',type(data))
    data_to_predict = pd.json_normalize(data) #pd dataframe
    print(data_to_predict)
    print('Type data',type(data_to_predict))

    try:
        print("Dentro del bloque try")
        print(f"Este es eeeeeel modelo {modelo_a}")
        prediccion = predict_model(modelo_a, data=data_to_predict)
        print("Estructura completa de la predicción:")
        print(prediccion)

        valor_predicho = round(list(prediccion['prediction_label'])[0],2)
        current_date = datetime.now()

        with open('model_logs_a.txt','a') as archivo_modificado:
            strLog = f'{"lightgbm"},{valor_predicho},{current_date.strftime("%Y-%m-%d %H:%M:%S")}\n'
            archivo_modificado.write(strLog)

        print(valor_predicho)
        return jsonify({'Prediccion':valor_predicho})
    except Exception as e:
        print("Error en el bloque try:", str(e))
        current_date = datetime.now()
        with open('model_logs_a.txt','a') as archivo_modificado:
            strLog = f'{"Error"},{current_date.strftime("%Y-%m-%d %H:%M:%S")}\n'
            archivo_modificado.write(strLog)
        return jsonify({'mensaje':'Se generó un error en la predicción.'})


@app.route('/predictB', methods=['POST'])
def predictB():
    data = request.get_json()                   #dictionary
    data_to_predict = pd.json_normalize(data)   #pd dataframe

    try:
        prediccion = predict_model(modelo_b, data=data_to_predict)
        valor_predicho = round(list(prediccion['prediction_label'])[0],2)
        current_date = datetime.now()

        with open('model_logs_b.txt','a') as archivo_modificado:
            strLog = f'{"et"},{valor_predicho},{current_date.strftime("%Y-%m-%d %H:%M:%S")}\n'
            archivo_modificado.write(strLog)

        print(valor_predicho)
        return jsonify({'Prediccion':valor_predicho})
    except Exception as e:
        print("Error en el bloque try:", str(e))
        current_date = datetime.now()
        with open('model_logs_b.txt','a') as archivo_modificado:
            strLog = f'{"Error"},{current_date.strftime("%Y-%m-%d %H:%M:%S")}\n'
            archivo_modificado.write(strLog)
        return jsonify({'mensaje':'Se generó un error en la predicción.'})
    

@app.route('/predictC', methods=['POST'])
def predictC():
    data = request.get_json()
    data_to_predict = pd.json_normalize(data) #pd dataframe

    try:
        prediccion = predict_model(modelo_c, data=data_to_predict)
        valor_predicho = round(list(prediccion['prediction_label'])[0],2)
        current_date = datetime.now()

        with open('model_logs_c.txt','a') as archivo_modificado:
            strLog = f'{"knn"},{valor_predicho},{current_date.strftime("%Y-%m-%d %H:%M:%S")}\n'
            archivo_modificado.write(strLog)

        print(valor_predicho)
        return jsonify({'Prediccion':valor_predicho})
    except Exception as e:
        current_date = datetime.now()
        with open('model_logs_c.txt','a') as archivo_modificado:
            strLog = f'{"Error"},{current_date.strftime("%Y-%m-%d %H:%M:%S")}\n'
            archivo_modificado.write(strLog)
        return jsonify({'mensaje':'Se generó un error en la predicción.'})
    
@app.route('/predictAll', methods=['POST'])
def predictAll():
    data = request.get_json()
    data_to_predict = pd.json_normalize(data) #pd dataframe

    try:
        prediccion_a = predict_model(modelo_a, data=data_to_predict)
        prediccion_b = predict_model(modelo_b, data=data_to_predict)
        prediccion_c = predict_model(modelo_c, data=data_to_predict)

        valor_predicho_a = round(list(prediccion_a['prediction_label'])[0],2)
        valor_predicho_b = round(list(prediccion_b['prediction_label'])[0],2)
        valor_predicho_c = round(list(prediccion_c['prediction_label'])[0],2)

        current_date = datetime.now()

        with open('model_logs_all.txt','a') as archivo_modificado:
            strLog = f'{"lightgbm"},{valor_predicho_a},{current_date.strftime("%Y-%m-%d %H:%M:%S")}\n'
            archivo_modificado.write(strLog)

            strLog = f'{"et"},{valor_predicho_b},{current_date.strftime("%Y-%m-%d %H:%M:%S")}\n'
            archivo_modificado.write(strLog)

            strLog = f'{"knn"},{valor_predicho_c},{current_date.strftime("%Y-%m-%d %H:%M:%S")}\n'
            archivo_modificado.write(strLog)

        return jsonify({'Prediccion lightgbm': valor_predicho_a, 'Prediccion ET': valor_predicho_b, "Prediccion KNN": valor_predicho_c})
    
    except Exception as e:
        current_date = datetime.now()
        with open('model_logs_c.txt','a') as archivo_modificado:
            strLog = f'{"Error"},{current_date.strftime("%Y-%m-%d %H:%M:%S")}\n'
            archivo_modificado.write(strLog)
        return jsonify({'mensaje':'Se generó un error en la predicción.'})