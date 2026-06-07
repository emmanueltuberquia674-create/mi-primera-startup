from flask import Flask, jsonify, request

app = Flask(__name__)

# Esta será nuestra Base de Datos temporal (una lista vacía)
base_de_datos_usuarios = []

# RUTA 1: Ver los usuarios que tenemos (Método GET)
@app.route('/usuarios', methods=['GET'])
def ver_usuarios():
    return jsonify({
        "usuarios_registrados": base_de_datos_usuarios,
        "total": len(base_de_datos_usuarios)
    })

# RUTA 2: Registrar un nuevo usuario (Método POST)
@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    # Recibimos los datos que nos envían desde internet
    datos_recibidos = request.get_json()
    
    # Guardamos el nuevo usuario en nuestra lista
    base_de_datos_usuarios.append(datos_recibidos)
    
    return jsonify({
        "mensaje": "Usuario guardado con exito en la startup",
        "usuario_creado": datos_recibidos
    })

if __name__ == '__main__':
    app.run(debug=True)