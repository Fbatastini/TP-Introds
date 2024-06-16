# habitaciones_routes.py
from flask import redirect, url_for, request
from flask_login import login_required
import requests
from config import API_URL

def register_habitaciones_routes(app):
    @app.route('/delete_room', methods=['POST'])
    @login_required
    def enviar_eliminacion():
        num = {'id': request.form.get('id')}
        respuesta = requests.delete(f'{API_URL}/eliminar_habitacion', json=num).json()
        message = respuesta.get('message')

        return redirect(url_for('mod_rooms', message=message))

    @app.route('/create_room', methods=['POST'])
    @login_required
    def enviar_crear_hab():
        num = request.form.get('num')
        capacidad = request.form.get('capacidad')
        precio = request.form.get('precio')
        descripcion = request.form.get('descripcion')
        promocion = request.form.get('promocion')

        habitacion = {'numero': num, 'precio': precio, 'capacidad': capacidad, 'descripcion': descripcion,
                      'promocion': promocion}
        respuesta = requests.post(f'{API_URL}/agregar_habitacion', json=habitacion).json()
        message = respuesta.get('message')

        return redirect(url_for('mod_rooms', message=message))

    @app.route('/modify_price', methods=['POST'])
    @login_required
    def enviar_precio():
        num = request.form.get('num')
        precio = request.form.get('precio')
        modificaciones = {'numero': num, 'nuevo_precio': precio}

        respuesta = requests.patch(f'{API_URL}/cambiar_precio', json=modificaciones).json()
        message = respuesta.get('message')

        return redirect(url_for('mod_rooms', message=message))

    @app.route('/modify_promotion', methods=['POST'])
    @login_required
    def enviar_promocion():
        num = request.form.get('num')
        promocion = request.form.get('promocion')
        modificaciones = {'numero_habitacion': num, 'nueva_promocion': promocion}

        respuesta = requests.patch(f'{API_URL}/cambiar_promocion', json=modificaciones).json()
        message = respuesta.get('message')

        return redirect(url_for('mod_rooms', message=message))
