"""api module"""
from flask import Flask
from endpoints.room import room_bp
from endpoints.booking import booking_bp
from endpoints.contact import contact_bp
from endpoints.verifications import verifications_bp

app = Flask(__name__)

# obtener, agregar y eliminar habitaciones
# cambiar precio y promo
app.register_blueprint(room_bp)

# obtener, cambiar y eliminar reservaciones
app.register_blueprint(booking_bp)

# obtener, crear y eliminar contactos
app.register_blueprint(contact_bp)

# Disponibilidad; verificar usuario
app.register_blueprint(verifications_bp)


# For docker container
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)