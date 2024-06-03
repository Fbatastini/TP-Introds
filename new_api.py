from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from api.db_queries import create_habitaciones_table, create_reservas_table, create_dias_reservados_table
from api.queries import get_query_habitaciones, get_query_siguiente_dia, get_query_verif_disponibilidad, get_query_nueva_reserva, get_query_nro_reserva, get_query_cant_dias_reservados, get_query_verif, get_cant_habitaciones_query

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://steven:password@localhost/mysqldb")

def crear_tablas():
    # Execute SQL statements to create tables
    with engine.connect() as conn:
        conn.execute(text(create_habitaciones_table))
        conn.execute(text(create_reservas_table))
        conn.execute(text(create_dias_reservados_table))


def verificar_fecha_pasada(conn, reserva):
    query_verif = get_query_verif(reserva)

    try:
        result = conn.execute(text(query_verif)).fetchall()
        if result[0][0] == 0:
            return jsonify({'message': 'No se puede reservar una fecha pasada.'}), 400
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': 'Se ha producido un error ' + str(err.__cause__)})


def verificar_disponibilidad(conn, reserva):
    cantidad_habitaciones_query = get_cant_habitaciones_query(reserva)
    cantidad_habitaciones = conn.execute(text(cantidad_habitaciones_query)).fetchone()[0]

    cant_dias_reservados_query = get_query_cant_dias_reservados(reserva)
    cant_dias_reservados = conn.execute(text(cant_dias_reservados_query)).fetchone()[0]

    for i in range(cant_dias_reservados):
        siguiente_dia_query = get_query_siguiente_dia(reserva, i)
        dia = conn.execute(text(siguiente_dia_query)).fetchone()[0]

        verif_disponibilidad_query = get_query_verif_disponibilidad(reserva, dia)
        habitaciones_reservadas = conn.execute(text(verif_disponibilidad_query)).fetchone()[0]

        if habitaciones_reservadas >= cantidad_habitaciones:
            return jsonify({'message': f'No hay habitaciones tipo {reserva["tipo_habitacion"]} disponibles para {dia}.'}), 400


def agregar_reserva():
    conn = engine.connect()
    reserva = request.get_json()

    try:
        verificar_fecha_pasada(conn, reserva)
        verificar_disponibilidad(conn, reserva)
        conn.close()
        return jsonify({'message': 'Se ha agregado correctamente '}), 201
    except Exception as e:
        conn.close()
        return jsonify({'message': 'Se ha producido un error ' + str(e)})


@app.route("/")
def index():
    return jsonify({"mensaje": "Funcionando correctamente"})


@app.route('/agregar_reserva', methods=['POST'])
def agregar_reserva_route():
    return agregar_reserva()


@app.route("/test_reserva", methods=['POST'])
def test_reserva():
    reserva = request.get_json()
    try:
        conn = engine.connect()
        query = get_query_nueva_reserva(reserva)
        conn.execute(text(query))
        conn.commit()

        return jsonify({'message': 'Test reservation added successfully', "reserva": reserva}), 201
    
    except SQLAlchemyError as e:
        return jsonify({'message': 'Error adding test reservation: ' + str(e)}), 500

if __name__ == "__main__":
    crear_tablas()
    app.run("127.0.0.1", port=5006, debug=True)
