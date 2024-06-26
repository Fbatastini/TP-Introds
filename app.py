# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import requests
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash messages
# Local dev
# API_URL = 'http://127.0.0.1:5001'
# Docker
API_URL = ' http://api:5001'


login_manager = LoginManager()      #LoginManager es responsable de gestionar las sesiones de inicio de sesión de los usuarios.
login_manager.init_app(app)         #inicializa la instancia de LoginManager con la aplicación Flask
login_manager.login_view = 'login'  #establece el endpoint para la vista de inicio de sesión. 
                                    #Cuando un usuario intenta acceder a una ruta protegida sin estar autenticado, será redirigid
login_manager.login_message = ""

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

class User(UserMixin):          #Usermixin genera los metodos necesarios para que flask-login funcione, como get_id() o is_active()
    def __init__(self, id):
        self.id = id

# Ruta principal para la página de inicio
@app.route('/')
def index():
    habitaciones = requests.get(f'{API_URL}/habitaciones')
    cantidad_habitaciones = len(habitaciones.json())    
    return render_template('index.html', cantidad_habitaciones = cantidad_habitaciones, habitaciones = habitaciones.json())

@app.route('/about')
def about():
    habitaciones = requests.get(f'{API_URL}/habitaciones')
    cantidad_habitaciones = len(habitaciones.json())    
    return render_template('about.html', cantidad_habitaciones = cantidad_habitaciones)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    habitaciones = requests.get(f'{API_URL}/habitaciones')
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        mail = request.form.get('email')
        huespedes = request.form.get('huespedes')
        numero_habitacion = request.form.get('numero_habitacion')
        fecha_ingreso = request.form.get('fecha_ingreso')
        cantidad_noches = request.form.get('cantidad_noches')
        reserva = {
            'fecha_ingreso': fecha_ingreso,
            'cantidad_noches': cantidad_noches,
            'nombre': nombre,
            'huespedes': huespedes,
            'numero_habitacion': numero_habitacion,
            'mail': mail
        }
        response = requests.post(f'{API_URL}/reserva', json=reserva)

        if response.status_code == 201:
            flash(response.json()["message"])
        else:
            flash(response.json()["message"])
            return redirect(url_for('booking'))
    return render_template('booking.html', habitaciones=habitaciones.json())


@app.route('/verify_disponibility', methods=['GET', 'POST'])
def verify_disponibility():
    if request.method == 'POST':
        fecha_ingreso = request.form.get('fecha_ingreso')            
        cantidad_noches = request.form.get('cantidad_noches')
        huespedes = request.form.get('huespedes')
        disponibilidad = {
            'fecha_ingreso': fecha_ingreso,
            'cantidad_noches': cantidad_noches,
            'huespedes': huespedes
        }
        response = requests.get(f'{API_URL}/disponibilidad', json=disponibilidad)

        if response.status_code == 200:
            habitaciones = requests.get(f'{API_URL}/habitaciones')
            return render_template('booking.html', habitaciones_disponibles=response.json(), habitaciones=habitaciones.json())
        else:
            flash(response.json()["message"])
            return redirect(url_for('booking'))
    return redirect(url_for('booking'))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        mail = request.form['mail']
        asunto = request.form['asunto']
        mensaje = request.form['mensaje']
        contacto = {
            'nombre': nombre,
            'mail': mail,
            'asunto': asunto,
            'mensaje': mensaje
        }
        response = requests.post(f'{API_URL}/agregar_contacto', json=contacto)
        if response.status_code == 201:
            flash(response.json()["message"])
        else:
            flash(response.json()["message"])
            return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/room')
def room():
    habitaciones = requests.get(f'{API_URL}/habitaciones').json()
    return render_template('room.html', habitaciones = habitaciones)

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        passwd = request.form.get('password')
        respuesta = requests.get(f'{API_URL}/user/{user}/{passwd}')
        respuesta = respuesta.json()
        if respuesta['message'] == 'exists':
            usuario = User(user)
            login_user(usuario)
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', mensaje = 'Wrong user or password')
    logout_user()
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#------------------------------- Paginas de admin -------------------------------

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    comentarios = requests.get(f'{API_URL}/contactos').json()
    ingreso = request.args.get('ingreso', None)
    mensaje = request.args.get('message', None)
    if ingreso:
        return render_template('admin.html', comentarios =  comentarios, ingreso=ingreso)
    if mensaje:
        return render_template('admin.html', comentarios = comentarios, mensaje = mensaje)
    return render_template('admin.html', comentarios = comentarios)

@app.route('/redireccion', methods=['POST', 'GET'])
def redireccion():
    opciones_reservas = ("modificar","cancelar")
    opciones_habitaciones = ("borrar_hab", "agregar_hab", "cambiar_precio", "cambiar_prom", "cambiar_des")
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
        return render_template('mod_rooms.html', habitaciones =  habitaciones, ingreso=ingreso)
    if mensaje:
        return render_template('mod_rooms.html', habitaciones = habitaciones, mensaje = mensaje)
    return render_template('mod_rooms.html', habitaciones = habitaciones)

@app.route('/modify-bookings')
@login_required
def mod_bookings():
    reservas = requests.get(f'{API_URL}/reservas').json()
    ingreso = request.args.get('ingreso', None)
    mensaje = request.args.get('message', None)
    if ingreso:
        return render_template('mod_book.html', reservas = reservas, ingreso = ingreso)
    if mensaje:
        return render_template('mod_book.html', reservas = reservas, mensaje = mensaje)
    return render_template('mod_book.html', reservas = reservas)

# --------------------------------- Envios a la API ---------------------------------------------------------
#---------------------------------- Reservas ----------------------------------------------------------------

@app.route('/cancel_book', methods=['POST'])
@login_required
def enviar_cancelacion():
    id = {'id':request.form.get('id')}
    respuesta = requests.delete(f'{API_URL}/cancelar_reserva', json=id).json()
    message = respuesta.get('message')

    return redirect(url_for('mod_bookings', message = message))

@app.route('/modify_book', methods=['POST'])
@login_required
def enviar_modif_res():
    id = request.form.get('id')
    habitacion = request.form.get('numero_habitacion')
    huespedes = request.form.get('huespedes')
    checkin = request.form.get('nueva_fecha_checkin')
    noches = request.form.get('nuevas_noches')
    
    data = {'id':id, 'numero_habitacion':habitacion, 'huespedes': huespedes, 'nueva_fecha_ingreso':checkin, 'nuevas_noches':noches}
    respuesta = requests.patch(f'{API_URL}/cambiar_reserva', json=data).json()
    message = respuesta.get('message')
    
    return redirect(url_for('mod_bookings', message=message))

#---------------------------------------------- Habitaciones ---------------------------------------------------

@app.route('/delete_room', methods=['POST'])
@login_required
def enviar_eliminacion():
    num = {'numero':request.form.get('num')}
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

    habitacion = {'numero': num, 'precio': precio, 'capacidad': capacidad, 'descripcion': descripcion, 'promocion': promocion}
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



@app.route('/modify_description', methods=['POST'])
@login_required
def enviar_descripcion():
    num = request.form.get('num')
    descripcion = request.form.get('descripcion')
    modificaciones = {'numero': num, 'nueva_descripcion': descripcion}

    respuesta = requests.patch(f'{API_URL}/cambiar_descripcion', json=modificaciones).json()
    message = respuesta.get('message')

    return redirect(url_for('mod_rooms', message=message))

#---------------------------------------------- Contactos ---------------------------------------------------
@app.route('/delete_contact', methods = ['POST'])
@login_required
def eliminar_contacto():
    id = {'id':request.form.get('id')}
    respuesta = requests.delete(f'{API_URL}/eliminar_contacto', json=id).json()
    message = respuesta.get('message')

    return redirect(url_for('admin', message = message))


#---------------------------------------------- ErrorHandlers ---------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


# # Ruta para manejar la carga de archivos
# if __name__ == '__main__':
#     app.run(debug=True)

# for docker
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)