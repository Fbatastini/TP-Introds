# app.py
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash messages


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
        entrada=datetime.fromisoformat(request.form.get('entrada'))
        nombre=request.form.get('nombre')
        salida=datetime.fromisoformat(request.form.get('salida'))
        huespedes=request.form.get('huespedes')
        habitacion=request.form.get('habitacion')
        email=request.form.get('email')
        comentario=request.form.get('comentario')
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

# Ruta para manejar la carga de archivos
if __name__ == '__main__':
    app.run(debug=True)
