# app.py
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import requests
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash messages

login_manager = LoginManager()      #LoginManager es responsable de gestionar las sesiones de inicio de sesión de los usuarios.
login_manager.init_app(app)         #inicializa la instancia de LoginManager con la aplicación Flask
login_manager.login_view = 'login'  #establece el endpoint para la vista de inicio de sesión. 
                                    #Cuando un usuario intenta acceder a una ruta protegida sin estar autenticado, será redirigido

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

class User(UserMixin):          #Usermixin genera los metodos necesarios para que flask-login funcione, como get_id() o is_active()
    def __init__(self, id):
        self.id = id

# Ruta principal para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        check_in=request.form.get('check_in')
        nombre=request.form.get('nombre')
        check_out=request.form.get('check_out')
        huespedes=request.form.get('huespedes')
        habitacion=request.form.get('habitacion')
        email=request.form.get('email')
        comentario=request.form.get('comentario')
        reserva = {
            'check_in': check_in,
            'check_out': check_out,
            'nombre': nombre,
            'cant_personas' : huespedes,
            'tipo_habitacion': habitacion,
            'mail': email,
            'comentario':comentario
            }
        request.post('http://127.0.0.1:5001/agregar_reserva', json=reserva)
        return redirect(url_for('confirmacion'))
    return render_template('booking.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/room')
def room():
    return render_template('room.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/confirmacion')
def confirmacion():
    return render_template('confirmacion.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        passwd = request.form.get('password')
        respuesta = requests.get(f'http://127.0.0.1:5001/user/{user}/{passwd}')
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

@app.route('/admin')
@login_required
def admin():
    comentarios = requests.get('http://127.0.0.1:5001/contactos')
    return render_template('admin.html', comentarios = comentarios)

@app.route('/redireccion', methods=['POST', 'GET'])
def redireccion():
    opciones_reservas = ("modificar","cancelar")
    opciones_habitaciones = ("borrar_hab", "agregar_hab", "cambiar_precio", "cambiar_prom")
    ingreso = request.form.get('metodo')

    if ingreso in opciones_reservas:
        return redirect(url_for('mod_bookings', ingreso=ingreso))
    
    elif ingreso in opciones_habitaciones:
        return redirect(url_for('mod_rooms', ingreso=ingreso))
    
@app.route('/modify-rooms', methods=['GET', 'POST'])
@login_required
def mod_rooms():
    habitaciones = requests.get('http://127.0.0.1:5001/habitaciones')
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
    reservas = request.get('http://127.0.0.1:5001/reservas')
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
    respuesta = requests.delete('http://127.0.0.1:5001/cancelar_reserva', json=id)
    message = respuesta.get('message')

    return redirect(url_for('mod_bookings', message = message))

@app.route('/modify_book', methods=['POST'])
@login_required
def enviar_modif_res():
    id = request.form.get('id')
    habitacion = request.form.get('numero_habitacion')
    checkin = request.form.get('nueva_fecha_checkin')
    noches = request.form.get('nuevas_noches')
    
    data = {'id':id, 'numero_habitacion':habitacion, 'nueva_fecha_checkin':checkin, 'nuevas_noches':noches}
    respuesta = requests.patch('http://127.0.0.1:5001/cambiar_reserva', json=data)
    message = respuesta.get('message')
    
    return redirect(url_for('mod_bookings', message=message))

#---------------------------------------------- Habitaciones ---------------------------------------------------

@app.route('/delete_room', methods=['POST'])
@login_required
def enviar_eliminacion():
    num = {'numero':request.form.get('num')}
    respuesta = requests.delete('http://127.0.0.1:5001/cancelar_reserva', json=num)
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
    respuesta = requests.post('http://127.0.0.1:5001/cancelar_reserva', json=habitacion)
    message = respuesta.get('message')

    return redirect(url_for('mod_rooms', message=message))


@app.route('/modify_price', methods=['POST'])
@login_required
def enviar_precio():
    num = request.form.get('num')
    precio = request.form.get('precio')
    modificaciones = {'numero': num, 'nuevo_precio': precio}

    respuesta = requests.delete('http://127.0.0.1:5001/cancelar_reserva', json=modificaciones)
    message = respuesta.get('message')

    return redirect(url_for('mod_rooms', message=message))


@app.route('/modify_promotion', methods=['POST'])
@login_required
def enviar_promocion():
    num = request.form.get('num')
    promocion = request.form.get('promocion')
    modificaciones = {'numero': num, 'nueva_promocion': promocion}

    respuesta = requests.delete('http://127.0.0.1:5001/cancelar_reserva', json=modificaciones)
    message = respuesta.get('message')

    return redirect(url_for('mod_rooms', message=message))

#---------------------------------------------- ErrorHandlers ---------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


# Ruta para manejar la carga de archivos
if __name__ == '__main__':
    app.run(debug=True)
