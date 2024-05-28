# app.py
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash messages


# Ruta principal para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def index():
    return render_template('about.html')

@app.route('/booking')
def index():
    return render_template('booking.html')

@app.route('/contact')
def index():
    return render_template('contact.html')

@app.route('/room')
def index():
    return render_template('room.html')

@app.route('/service')
def index():
    return render_template('service.html')

@app.route('/team')
def index():
    return render_template('team.html')

@app.route('/testimonial')
def index():
    return render_template('testimonial.html')

# Ruta para manejar la carga de archivos
if __name__ == '__main__':
    app.run(debug=True)
