# admin_routes.py
from flask import render_template, redirect, url_for, request
from flask_login import login_required
import requests
from config import API_URL

def register_admin_routes(app):

    @app.route('/admin', methods=['GET', 'POST'])
    @login_required
    def admin():
        comentarios = requests.get(f'{API_URL}/contactos').json()
        ingreso = request.args.get('ingreso', None)
        mensaje = request.args.get('message', None)
        if ingreso:
            return render_template('admin.html', comentarios=comentarios, ingreso=ingreso)
        if mensaje:
            return render_template('admin.html', comentarios=comentarios, mensaje=mensaje)
        return render_template('admin.html', comentarios=comentarios)

    @app.route('/redireccion', methods=['POST', 'GET'])
    def redireccion():
        opciones_reservas = ("modificar", "cancelar")
        opciones_habitaciones = ("borrar_hab", "agregar_hab", "cambiar_precio", "cambiar_prom")
        opciones_contactos = ("borrar")
        ingreso = request.form.get('metodo')

        if ingreso in opciones_reservas:
            return redirect(url_for('mod_bookings', ingreso=ingreso))
        elif ingreso in opciones_habitaciones:
            return redirect(url_for('mod_rooms', ingreso=ingreso))
        elif ingreso in opciones_contactos:
            return redirect(url_for('admin', ingreso=ingreso))

    @app.route('/modify-rooms', methods=['GET', 'POST'])
    @login_required
    def mod_rooms():
        habitaciones = requests.get(f'{API_URL}/habitaciones').json()
        ingreso = request.args.get('ingreso', None)
        mensaje = request.args.get('message', None)
        if ingreso:
            return render_template('mod_rooms.html', habitaciones=habitaciones, ingreso=ingreso)
        if mensaje:
            return render_template('mod_rooms.html', habitaciones=habitaciones, mensaje=mensaje)
        return render_template('mod_rooms.html', habitaciones=habitaciones)

    @app.route('/modify-bookings')
    @login_required
    def mod_bookings():
        reservas = requests.get(f'{API_URL}/reservas').json()
        ingreso = request.args.get('ingreso', None)
        mensaje = request.args.get('message', None)
        if ingreso:
            return render_template('mod_book.html', reservas=reservas, ingreso=ingreso)
        if mensaje:
            return render_template('mod_book.html', reservas=reservas, mensaje=mensaje)
        return render_template('mod_book.html', reservas=reservas)
