from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://usuario:scrumbeasts@localhost:3309/tp_database", echo=True)

@app.route('/agregar_reserva', methods = ['POST'])
def agregar_reserva():
    conn = engine.connect()
    reserva = request.get_json()

    # NO SE PUEDE RESERVAR UN DIA QUE YA PASO (CHECK_IN >= curdate)
    query_verif = f""" 
        SELECT '{reserva["check_in"]}' >= CURDATE();
    """

    try:
        result = conn.execute(text(query_verif))
        conn.commit()
        if result.first()[0] == 0:
            return jsonify({'message': 'No se puede reservar un fecha pasada.'}), 400
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': 'Se ha producido un error ' + str(err.__cause__)})

    # NO SE PUEDE RESERVAR SI NO HAY MAS HABITACIONES DE ESE TIPO DISPONIBLES PARA ALGÚN DíA DE LA RESERVA (SELECT DATEDIFF(final, inicio))  (SELECT DATE_ADD('dia', INTERVAL n DAY);)
    dias_reservados = []

    query_cant_dias_reservados = f"""
        SELECT 
        DATEDIFF('{reserva["check_out"]}', '{reserva["check_in"]}');
    """
    query_habitaciones = f"""
        SELECT cantidad 
        FROM habitaciones 
        WHERE tipo_habitacion='{reserva["tipo_habitacion"]}';
    """
    
    try:    
        cant_dias_reservados = conn.execute(text(query_cant_dias_reservados)).first()[0]

        if cant_dias_reservados <= 0:
            return jsonify({'message': 'El check_in tiene que ser previo al check_out.'}), 400

        cantidad_habitaciones = conn.execute(text(query_habitaciones)).first()[0]
        for i in range(cant_dias_reservados):    
            query_siguiente_dia = f"""
                SELECT 
                DATE_ADD('{reserva["check_in"]}', 
                INTERVAL {i} DAY); 
            """
            dia = conn.execute(text(query_siguiente_dia)).first()[0]
            query_verif_disponibilidad = f"""
                SELECT * 
                FROM dias_reservados WHERE tipo_habitacion='{reserva["tipo_habitacion"]}' 
                AND dia='{dia}';
            """
            dias_reservados.append(dia)
            resultado = conn.execute(text(query_verif_disponibilidad))
            if resultado.rowcount >= cantidad_habitaciones:
                return jsonify({'message': f'No hay habitaciones tipo {reserva["tipo_habitacion"]} disponibles para {dia}.'}), 400
            
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error ' + str(err.__cause__)})
    

    # UNA VEZ LA RESERVA ES VÁLIDA SE AGREGA A LAS TABLAS reservas y dias_reservados
    query = f"""
        INSERT INTO reservas 
        (nombre, mail, tipo_habitacion, cant_personas, check_in, check_out)
        VALUES (
            '{reserva["nombre"]}', 
            '{reserva["mail"]}', 
            '{reserva["tipo_habitacion"]}', 
            '{reserva["cant_personas"]}', 
            '{reserva["check_in"]}', 
            '{reserva["check_out"]}'
            );
    """

    try:
        result = conn.execute(text(query))
        conn.commit()

        query_nro_reserva = f"""
            SELECT nro_reserva 
            FROM reservas 
            WHERE nombre='{reserva["nombre"]}' 
                AND mail='{reserva["mail"]}' 
                AND tipo_habitacion='{reserva["tipo_habitacion"]}' 
                AND cant_personas={reserva["cant_personas"]} 
                AND check_in='{reserva["check_in"]}' 
                AND check_out='{reserva["check_out"]}';
        """
        
        Id = conn.execute(text(query_nro_reserva)).first()[0]

        for dia in dias_reservados:
            query_dia_reservado = f"""
                INSERT INTO dias_reservados 
                VALUES (
                    {Id}, '{dia}', 
                    '{reserva["tipo_habitacion"]}'
                );
            """
            result = conn.execute(text(query_dia_reservado))
            conn.commit()
    
        conn.close()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error ' + str(err.__cause__)})
    
    
    return jsonify({'message': 'se ha agregado correctamente ' + query}), 201


if __name__ == "__main__":
    app.run("127.0.0.1", port=5001, debug=True)