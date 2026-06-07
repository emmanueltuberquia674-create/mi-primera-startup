from flask import Flask, jsonify, request, render_template
import json
import os

app = Flask(__name__)
ARCHIVO_DB = 'usuarios.json'

def leer_usuarios_del_disco():
    if not os.path.exists(ARCHIVO_DB):
        return []
    with open(ARCHIVO_DB, 'r') as archivo:
        return json.load(archivo)

def guardar_usuarios_en_disco(lista_usuarios):
    with open(ARCHIVO_DB, 'w') as archivo:
        json.dump(lista_usuarios, archivo, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuarios', methods=['GET'])
def ver_usuarios():
    usuarios = leer_usuarios_del_disco()
    return jsonify({
        "usuarios_registrados": usuarios,
        "total": len(usuarios)
    })

@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    datos_recibidos = request.get_json()
    usuarios_actuales = leer_usuarios_del_disco()
    
    # LÓGICA INTELIGENTE: Clasificación automática de clientes
    # Limpiamos el texto de fortuna (ej: "100M" -> 100) para analizarlo
    fortuna_texto = datos_recibidos.get('fortuna_estimada', '0').upper().replace('M', '')
    try:
        fortuna_num = float(fortuna_texto)
        if fortuna_num >= 100:
            datos_recibidos['categoria'] = 'VIP ✨'
        else:
            datos_recibidos['categoria'] = 'Estándar'
    except:
        datos_recibidos['categoria'] = 'Estándar'

    usuarios_actuales.append(datos_recibidos)
    guardar_usuarios_en_disco(usuarios_actuales)
    return jsonify({"mensaje": "Usuario procesado con éxito", "usuario_creado": datos_recibidos})

# NUEVA RUTA: Para eliminar un usuario por su nombre
@app.route('/eliminar', methods=['POST'])
def eliminar_usuario():
    nombre_a_borrar = request.get_json().get('nombre')
    usuarios_actuales = leer_usuarios_del_disco()
    
    # Filtramos la lista para dejar por fuera al que queremos borrar
    usuarios_filtrados = [u for u in usuarios_actuales if u.get('nombre') != nombre_a_borrar]
    
    guardar_usuarios_en_disco(usuarios_filtrados)
    return jsonify({"mensaje": "Usuario eliminado correctamente"})

if __name__ == '__main__':
    import os
    # Render asigna un puerto en la variable de entorno PORT. Si no existe, usa el 5000 local.
    puerto = int(os.environ.get('PORT', 5000))
    # Escucha en 0.0.0.0 para que sea accesible desde el exterior en la nube
    app.run(host='0.0.0.0', port=puerto)