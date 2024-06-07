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
        respuesta = requests.get(f'http://127.0.0.1:5000/user/{user}/{passwd}')
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
    #comentarios = request.get('http://127.0.0.1:5000/contactos')
    return render_template('admin.html', comentarios = {})

@app.route('/redireccion', methods=['POST', 'GET'])
def redireccion():
    ingreso = request.form.get('metodo')
    if ingreso == 'check_in' or ingreso == 'noches':
        return redirect(url_for('mod_bookings', ingreso=ingreso))
    elif ingreso in ('precio', 'descripcion', 'promocion'):\
        return redirect(url_for('mod_rooms', ingreso=ingreso))
    
@app.route('/modify-rooms', methods=['GET', 'POST'])
@login_required
def mod_rooms():
    #habitaciones = request.get('http://127.0.0.1:5000/habitaciones')
    ingreso = request.args.get('ingreso', None)
    if ingreso:
        return render_template('mod_rooms.html', habitaciones = {}, ingreso = ingreso)
    return render_template('mod_rooms.html', habitaciones = {})

@app.route('/modify-bookings')
@login_required
def mod_bookings():
    #reservas = request.get('http://127.0.0.1:5000/reservas')
    ingreso = request.args.get('ingreso', None)
    if ingreso:
        return render_template('mod_book.html', reservas = {}, ingreso = ingreso)
    return render_template('mod_book.html', reservas={})

# Ruta para manejar la carga de archivos
if __name__ == '__main__':
    app.run(debug=True)
