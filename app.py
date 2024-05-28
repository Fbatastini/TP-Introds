# app.py
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash messages


# Ruta principal para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')


# Ruta para manejar la carga de archivos
if __name__ == '__main__':
    app.run(debug=True)
