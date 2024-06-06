from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from api.queries import get_query_nueva_reserva
from api.verificaciones_reservas import verificar_disponibilidad, verificar_fecha_pasada

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://usuario:scrumbeasts@localhost:3309/tp_database", echo=True)

@app.route("/")
def index():
    return jsonify({"message": "Server running"})

@app.route('/agregar_reserva', methods=['POST'])
def agregar_reserva_route():
    return agregar_reserva()

def agregar_reserva():
    conn = engine.connect()
    reserva = request.get_json()
    try:
        verificar_fecha_pasada(conn, reserva)
        verificar_disponibilidad(conn, reserva)
        query = get_query_nueva_reserva(reserva)
        conn.execute(text(query))
        conn.commit()
        conn.close()
        return jsonify({'message': 'The reservation has been added correctly '}), 201
    except Exception as e:
        conn.close()
        return jsonify({'message': 'An Error has occured adding the reservation ' + str(e)})

if __name__ == "__main__":
    app.run("127.0.0.1", port=5001, debug=True)