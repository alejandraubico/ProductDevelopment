from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/saludo", methods = ['GET'])

def saludo():
    strOut = 'Hola mundo'
    print(strOut)
    return jsonify({'mensaje': strOut})

# @app.route("/sumar", methods = ['GET'])
# def sumar():
#     a = 10
#     b = 50
#     resultado = a+b
#     return jsonify({'suma': resultado})

@app.route("/sumar/<int:a>/<int:b>", methods = ['GET'])
def sumar(a=None,b=None):
    if((a==None) and (b==None)):
        return jsonify({'resultado':'No se enviaron parámetros para operar.'})
    else:
        resultado = a+b
        return jsonify({'suma': resultado})
    
# @app.route("/multiplicar/", methods = ['GET'])
# def multi():
#     a = int(request.args.get('a',None))
#     b = int(request.args.get('b',None))

#     if((a==None) and (b==None)):
#         return jsonify({'resultado':'No se enviaron parámetros para operar.'})
#     else:
#         resultado = a+b
#         return jsonify({'multiplicacion': resultado})
    
@app.route("/multiplicar/", methods = ['GET'])
def multi():
    try:
        a = int(request.args.get('a',None))
        b = int(request.args.get('b',None))
        resultado = a+b
        return jsonify({'resultado': resultado})
    except:
        return jsonify({'resultado':'No se enviaron parámetros para operar.'})

#get, post, put, delete, update 
#  
@app.route("/dividir/", methods = ['POST'])
def division():
    data = request.json
    print(data)
    return jsonify({'Mensaje': 'Procesando'})