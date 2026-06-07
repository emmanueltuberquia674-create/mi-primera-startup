from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Nombre del archivo que servirá como nuestra Base de Datos en el disco duro
ARCHIVO_DB = 'usuarios.json'

# Función auxiliar para LEER los usuarios del archivo
def leer_usuarios_del_disco():
    # Si el archivo no existe todavía, devolvemos una lista vacía
    if not os.path.exists(ARCHIVO_DB):
        return []
    
    # Si existe, lo abrimos y leemos su contenido
    with open(ARCHIVO_DB, 'r') as archivo:
        return json.load(archivo)

# Función auxiliar para GUARDAR los usuarios en el archivo
def guardar_usuarios_en_disco(lista_usuarios):
    with open(ARCHIVO_DB, 'w') as archivo:
        json.dump(lista_usuarios, archivo, indent=4)


# RUTA 1: Ver los usuarios (Ahora lee directamente del disco duro)
@app.route('/usuarios', methods=['GET'])
def ver_usuarios():
    usuarios = leer_usuarios_del_disco()
    return jsonify({
        "usuarios_registrados": usuarios,
        "total": len(usuarios)
    })


# RUTA 2: Registrar usuario (Ahora escribe en el disco duro)
@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    datos_recibidos = request.get_json()
    
    # 1. Traemos los usuarios que ya existían en el archivo
    usuarios_actuales = leer_usuarios_del_disco()
    
    # 2. Le sumamos el nuevo usuario a la lista
    usuarios_actuales.append(datos_recibidos)
    
    # 3. Guardamos la lista actualizada de vuelta en el disco duro
    guardar_usuarios_en_disco(usuarios_actuales)
    
    return jsonify({
        "mensaje": "Usuario guardado con exito en el disco duro de la startup",
        "usuario_creado": datos_recibidos
    })


if __name__ == '__main__':
    app.run(debug=True)