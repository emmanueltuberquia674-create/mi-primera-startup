from flask import Flask, jsonify, request, render_template
import json
import os

# Configuración de rutas absolutas para Render
ruta_base = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(ruta_base, 'templates'),
    static_folder=os.path.join(ruta_base, 'static')
)

ARCHIVO_DB = 'usuarios.json'
ARCHIVO_CONFIG = 'config.json'

def leer_configuracion():
    # Si por alguna razón no existe, usamos valores por defecto
    if not os.path.exists(ARCHIVO_CONFIG):
        return {
            "nombre_sistema": "Vantage VC",
            "moneda": "USD",
            "simbolo_moneda": "$",
            "limite_vip": 100.0,
            "mensaje_bienvenida": "Panel de Control"
        }
    with open(ARCHIVO_CONFIG, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def leer_usuarios_del_disco():
    if not os.path.exists(ARCHIVO_DB):
        return []
    with open(ARCHIVO_DB, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def guardar_usuarios_en_disco(lista_usuarios):
    with open(ARCHIVO_DB, 'w', encoding='utf-8') as archivo:
        json.dump(lista_usuarios, archivo, indent=4)

# 1. RUTA PRINCIPAL (DASHBOARD)
@app.route('/')
def index():
    config = leer_configuracion()
    # Le pasamos la configuración al HTML para que pinte el nombre dinámico de la empresa
    return render_template('index.html', config=config)

# 2. RUTA PARA VER USUARIOS
@app.route('/usuarios', methods=['GET'])
def ver_usuarios():
    usuarios = leer_usuarios_del_disco()
    return jsonify({
        "usuarios_registrados": usuarios,
        "total": len(usuarios)
    })

# 3. RUTA PARA REGISTRAR USUARIO
@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    datos_recibidos = request.get_json()
    usuarios_actuales = leer_usuarios_del_disco()
    config = leer_configuracion()
    
    # LÓGICA INTELIGENTE CON CONFIGURACIÓN DINÁMICA
    fortuna_texto = datos_recibidos.get('fortuna_estimada', '0').upper().replace('M', '')
    try:
        fortuna_num = float(fortuna_texto)
        # Usamos el límite VIP establecido en el config.json
        if fortuna_num >= config['limite_vip']:
            datos_recibidos['categoria'] = 'VIP ✨'
        else:
            datos_recibidos['categoria'] = 'Estándar'
    except:
        datos_recibidos['categoria'] = 'Estándar'

    usuarios_actuales.append(datos_recibidos)
    guardar_usuarios_en_disco(usuarios_actuales)
    return jsonify({"mensaje": "Usuario procesado con éxito", "usuario_creado": datos_recibidos})

# 4. RUTA PARA ELIMINAR USUARIO
@app.route('/eliminar', methods=['POST'])
def eliminar_usuario():
    nombre_a_borrar = request.get_json().get('nombre')
    usuarios_actuales = leer_usuarios_del_disco()
    
    # Filtramos la lista para dejar por fuera al que queremos borrar
    usuarios_filtrados = [u for u in usuarios_actuales if u.get('nombre') != nombre_a_borrar]
    
    guardar_usuarios_en_disco(usuarios_filtrados)
    return jsonify({"mensaje": "Usuario eliminado correctamente"})

# EL ARRANQUE SIEMPRE VA AL FINAL DEL ARCHIVO
if __name__ == '__main__':
    import os
    # Render asigna un puerto en la variable de entorno PORT. Si no existe, usa el 5000 local.
    puerto = int(os.environ.get('PORT', 5000))
    # Escucha en 0.0.0.0 para que sea accesible desde el exterior en la nube
    app.run(host='0.0.0.0', port=puerto)