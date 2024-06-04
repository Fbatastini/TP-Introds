# app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash messages


# Ruta principal para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    return redirect(url_for('index'))

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

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# Ruta para manejar la carga de archivos
if __name__ == '__main__':
    app.run(debug=True)
