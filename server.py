# Questo modulo utilizza Flask per realizzare un web server. L'applicazione può essere eseguita in vari modi
# FLASK_APP=server.py FLASK_ENV=development flask run
# python server.py se aggiungiamo a questo file app.run()

from flask import Flask, request, jsonify
from result import Result
import user
import message
import base64

# viene creata l'applicazione con il nome del modulo corrente.
app = Flask(__name__)

# getErrorCode è una funzione di utilità che mappa i valori ritornati dal modulo user con quelli del
# protocollo HTTP in caso di errore. 
# 404 - Not Found: una risorsa non è stata trovata sul server;
# 403 - Forbidden: accesso negato;
# 409 - Conflict: è violato un vincolo di unicità. Ad esempio, esiste già un utente con la stessa mail registrata;
# Come ultima spiaggia è buona norma ritornare "500 - Internal Server Error" per indicare che qualcosa è andato storto
def getErrorCode(result: Result)->int:
    
    if result is Result.NOT_FOUND:
        code = 404
    elif result is Result.NOT_AUTHORIZED:
        code = 401
    elif result is Result.DUPLICATED:
        code = 409
    else:
        code = 500

    return code

@app.route('/user', methods=['POST'])
def createUser():
    data = request.get_json()
    name = data['name']
    surname = data['surname']
    email = data['email']
    password = data['password']
    
    result, u = user.SaveUser(name, surname, email, password)

    if result is not Result.OK:
        code = getErrorCode(result)
        return '', code
    else:
        return u, 201

@app.route('/user', methods=['DELETE'])
def deleteUser():
    result, u = authenticate(request)

    if result is not Result.OK:
        code = getErrorCode(result)
        return '', code

    user_id = u['id']

    result = user.Delete(user_id)

    if result is not Result.OK:
        code = getErrorCode(result)
        return '', code
    else:
        return '', 200

@app.route('/login', methods=['POST'])
def login():
    result, u = authenticate(request)

    if result is not Result.OK:
        code = getErrorCode(result)
        return '', code
    else:
        return u, 200

@app.route('/inbox', methods=['POST'])
def createMessage():
    result, u = authenticate(request)
    
    if result is not Result.OK:
        code = getErrorCode(result)
        return '', code
    
    data = request.get_json()
    
    sender = u['email']
    recipient = data['recipient']
    content = data['content']

    result, m = message.SaveMessage(sender, recipient, content)

    if result is not Result.OK:
        code = getErrorCode(result)
        return '', code
    else:
        return m, 201

@app.route('/inbox', methods=['GET'])
def readMessages():
    result, u = authenticate(request)
    
    if result is not Result.OK:
        code = getErrorCode(result)
        return '', code

    reader = u['email']

    result, l = message.GetMessages(reader)

    if result is not Result.OK:
        code = getErrorCode(result)
        return '', code
    else:
        return jsonify(l), 200

def authenticate(request):
    headers = request.headers
    auth_header = headers['Authorization']
    b64_credentials = auth_header.split(" ")[1]
    b64_credentials_bytes = b64_credentials.encode('ascii')
    credentials_bytes = base64.b64decode(b64_credentials_bytes)
    credentials = credentials_bytes.decode('ascii')
    credentialsComponents = credentials.split(":")
    email = credentialsComponents[0]
    password = credentialsComponents[1]

    return user.Login(email, password)

if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)
