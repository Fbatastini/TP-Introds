from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, date

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root:scrumbeasts@localhost:3309/tp_database")



#Servicio que consulta disponibilidad:
@app.route('/disponibilidad', methods = ['GET'])
def disponibility():   
    conn = engine.connect()
    
    consulta = request.get_json() #diccionario que contiene fecha huespedes, ingreso y noches
    huespedes = consulta['huespedes'] 
    
    #Chequeo que la fecha sea correcta
    try:
        fecha_ingreso = datetime.strptime(consulta['fecha_ingreso'], '%Y-%m-%d')
    except Exception:
        return jsonify({'message': 'La fecha ingresada no existe.'})
    
    noches = consulta['cantidad_noches']
    fecha_salida = fecha_ingreso + timedelta(days=int(noches) + 1) 
    fecha_actual = datetime.strptime(str(date.today()), '%Y-%m-%d')
    
    #Chequeo que la fecha sea mayor a la fecha actual
    if fecha_actual > fecha_ingreso:
        return jsonify({'message': 'No se puede reservar en una fecha pasada.'}), 400

    #query que pide todos los numeros de habitaciones que con capacidad mayor o igual a la de los huespedes pedidos.
    query_1 = f"""SELECT numero, precio FROM habitaciones WHERE capacidad >= {huespedes};"""
    #query que devuelve los numeros de las habitaciones que estan reservadas en las fechas solicitadas.
    query_2 = f"""SELECT numero_habitacion FROM reservas WHERE (DATE_ADD(fecha_ingreso, INTERVAL cantidad_noches + 1 DAY) > '{fecha_ingreso}' AND fecha_ingreso < '{fecha_salida}');"""
    
    try:
        result_1 = conn.execute(text(query_1))
        result_2 = conn.execute(text(query_2))
        
        conn.close() 
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)}), 500


    disponibilidad = []
    reservas = []
    
    for row_2 in result_2:
        reservas.append(row_2.numero_habitacion)
    
    for row_1 in result_1:
        entity = {}
        if row_1.numero in reservas:
            continue
        entity['numero_habitacion'] = row_1.numero
        entity['precio'] = row_1.precio
        
        disponibilidad.append(entity)

    return jsonify(disponibilidad), 200




#Servicio que verifica si existe el usuario y su contraseña:
@app.route('/user/<user>/<password>', methods=['GET'])
def verificar_usuario(user, password):
    conn = engine.connect()

    query = f"""Select * FROM usuarios WHERE usuario = '{user}' and clave = '{password}'"""

    try:
        result = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as e:
        return jsonify(str(e.__cause__))
    
    if result.rowcount != 0:
        return jsonify({'message':'exists'}),200
    else:
        return jsonify({'message':'does not exist'})




#Servicio que muestre datos de habitaciones(promociones incluidas):
@app.route('/habitaciones', methods=['GET'])
def room():
    conn = engine.connect()
    query = """
        SELECT numero, precio, capacidad, descripcion, promocion
        FROM habitaciones;
    """
    try:
        result = conn.execute(text(query))
        conn.close()
        habitaciones = []
        for row in result:
            habitacion = {
                "numero": row.numero,
                "precio": row.precio,
                "capacidad": row.capacidad,
                "descripcion": row.descripcion,
                "promocion": row.promocion
            }
            habitaciones.append(habitacion)
        return jsonify(habitaciones), 200
    except SQLAlchemyError as e:
        return jsonify({'message': f'Error al obtener datos de habitaciones: {str(e)}'}), 500




#Servicio que hace reserva:
@app.route('/reserva', methods=['POST'])
def booking():   
    conn = engine.connect()
    new_booking = request.get_json()

    cantidad_noches = new_booking['cantidad_noches']
    fecha_ingreso = new_booking['fecha_ingreso']
    
    query = """
    INSERT INTO reservas (numero_habitacion, huespedes, fecha_ingreso, cantidad_noches, nombre, mail)
    VALUES (:numero_habitacion, :huespedes, :fecha_ingreso, :cantidad_noches, :nombre, :mail)
    """
    
    validation_query = """
    SELECT numero_habitacion 
    FROM reservas 
    WHERE numero_habitacion = :numero_habitacion 
    AND DATE_ADD(fecha_ingreso, INTERVAL :cantidad_noches DAY) > :fecha_ingreso 
    AND fecha_ingreso < DATE_ADD(:fecha_ingreso, INTERVAL :cantidad_noches DAY)
    """
    
    try:
        val_result = conn.execute(text(validation_query), {
            'numero_habitacion': new_booking['numero_habitacion'],
            'fecha_ingreso': fecha_ingreso,
            'cantidad_noches': cantidad_noches
        })

        if val_result.rowcount == 0:
            conn.execute(text(query), {
                'numero_habitacion': new_booking['numero_habitacion'],
                'huespedes': new_booking['huespedes'],
                'fecha_ingreso': fecha_ingreso,
                'cantidad_noches': cantidad_noches,
                'nombre': new_booking['nombre'],
                'mail': new_booking['mail']
            })
            conn.commit()
            conn.close()
            return jsonify({"message": "Reserva realizada con éxito"}), 200
        else:
            conn.close()
            return jsonify({"message": f"La habitación número {new_booking['numero_habitacion']} ya se encuentra reservada en las fechas seleccionadas"}), 400
    except Exception as e:
        conn.close()
        return jsonify({'message': f"Error al realizar la reserva: {str(e)}"}), 500




#Servicio que cancela reserva:
@app.route('/cancelar_reserva', methods=['DELETE'])
def cancel_booking():   
    conn = engine.connect()
    cancel_data = request.get_json()

    query = """
    DELETE FROM reservas
    WHERE id = :id
    """

    validation_query = """
    SELECT * 
    FROM reservas 
    WHERE id = :id
    """

    try:
        val_result = conn.execute(text(validation_query), {
            'id': cancel_data['id']
        })

        if val_result.rowcount > 0:
            conn.execute(text(query), {
                'id': cancel_data['id']
            })
            conn.commit()
            conn.close()
            return jsonify({"message": "Reserva cancelada con éxito"}), 200
        else:
            conn.close()
            return jsonify({"message": "No se encontró una reserva con el ID proporcionado"}), 404
    except Exception as e:
        conn.close()
        return jsonify({"message": f"Error al cancelar la reserva: {str(e)}"}), 500




#Servicio que cambia cantidad de noches, o dia de check in:
@app.route('/cambiar_reserva', methods=['PATCH'])
def change_booking():
    conn = engine.connect()
    mod_booking_data = request.get_json()

    numero_habitacion = mod_booking_data.get('numero_habitacion')
    nueva_fecha_ingreso = mod_booking_data.get('nueva_fecha_ingreso')
    nuevas_noches = mod_booking_data.get('nuevas_noches')

    # Validar si la habitación existe en la base de datos
    query_validation = f"SELECT * FROM habitaciones WHERE numero = {numero_habitacion};"
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount == 0:
            conn.close()
            return jsonify({'message': f"No existe la habitación número {numero_habitacion}"}), 404
    except SQLAlchemyError as err:
        return jsonify({'message': str(err.__cause__)}), 500

    # Actualizar la reserva
    query = f"""UPDATE reservas
                SET fecha_ingreso = '{nueva_fecha_ingreso}', cantidad_noches = {nuevas_noches}
                WHERE id = {id};"""
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify({'message': str(err.__cause__)}), 500

    return jsonify({'message': 'Se ha modificado la reserva correctamente'}), 200





#Servicio que agrega habitacion(admin):
@app.route('/agregar_habitacion', methods = ['POST'])
def create_room():   
    conn = engine.connect()
    new_room = request.get_json()

    query = f"""INSERT INTO habitaciones (numero, precio, capacidad, descripcion, promocion)
    VALUES ({new_room['numero']}, {new_room['precio']}, {new_room['capacidad']}, '{new_room['descripcion']}', '{new_room['promocion']}');"""
    validation_query = f"SELECT numero FROM habitaciones WHERE numero = {new_room['numero']}"
    try:
        val_result = conn.execute(text(validation_query))

        if val_result.rowcount == 0:
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({"message": f"La habitacion número {new_room['numero']} ya existe."}), 400
    except SQLAlchemyError as err:
        return jsonify({'message': f'Se ha producido un error'})
    
    return jsonify({'message': 'Se ha agregado correctamente'}), 201




#Servicio que elimina habitacion(admin):
@app.route('/eliminar_habitacion', methods = ['DELETE'])    
def delete_room():
    conn = engine.connect()
    del_room = request.get_json()

    query = f"""DELETE FROM habitaciones WHERE numero = {del_room['numero']};"""
    validation_query = f"SELECT * FROM habitaciones WHERE numero = {del_room['numero']}"
    try:
        val_result = conn.execute(text(validation_query))
        if val_result.rowcount != 0 :
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({"message": f"La habitacion número {del_room['numero']} no existe."}), 404
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    return jsonify({'message': 'Se ha eliminado correctamente'}), 202




#Servicio que cambia el precio de una habitacion(modo admin):
@app.route('/cambiar_precio', methods = ['PATCH'])
def change_price():
    conn = engine.connect()
    mod_room_price = request.get_json()
    
    query = f"""UPDATE habitaciones SET precio = '{mod_room_price['nuevo_precio']}' WHERE numero = {mod_room_price['numero']};"""
    query_validation = f"SELECT * FROM habitaciones WHERE numero = {mod_room_price['numero']};"
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount != 0:
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({'message': f"No existe la habitacion número {mod_room_price['numero']}"}), 404
    except SQLAlchemyError as err:
        return jsonify({'message': str(err.__cause__)})
    
    return jsonify({'message': 'Se ha modificado correctamente'}), 200




#Servicio que cambia las promociones de las habitaciones(modo admin):
@app.route('/cambiar_promocion', methods=['PATCH'])
def change_promo():
    try:
        # Obtener datos de la solicitud PATCH
        data = request.get_json()
        numero_habitacion = data.get('numero_habitacion')
        nueva_promocion = data.get('nueva_promocion')

        # Validar que los datos requeridos estén presentes
        if not numero_habitacion or not nueva_promocion:
            return jsonify({'message': 'Se requieren el número de habitación y la nueva promoción.'}), 400

        # Actualizar la promoción en la base de datos
        conn = engine.connect()
        query = f"""
            UPDATE habitaciones
            SET promocion = :nueva_promocion
            WHERE numero = :numero_habitacion
        """
        conn.execute(text(query), nueva_promocion=nueva_promocion, numero_habitacion=numero_habitacion)
        conn.close()

        return jsonify({'message': f'Promoción actualizada para la habitación {numero_habitacion}.'}), 200

    except Exception as e:
        return jsonify({'message': f'Error al actualizar la promoción: {str(e)}'}), 500




#Servicio que muestre datos de reservas:
@app.route('/reservas', methods=['GET'])
def bookings():
    conn = engine.connect()
    query = """
        SELECT * FROM reservas;
    """
    try:
        result = conn.execute(text(query))
        conn.close()
        reservas = []
        for row in result:
            reserva = {
                "id": row.id,
                "numero_habitacion": row.numero_habitacion,
                "huespedes": row.huespedes,
                "fecha_ingreso": row.fecha_ingreso,
                "cantidad_noches": row.cantidad_noches,
                "nombre": row.nombre,
                "mail": row.mail
            }
            reservas.append(reserva)
        return jsonify(reservas), 200
    except SQLAlchemyError as e:
        return jsonify({'message': f'Error al obtener datos de reservas: {str(e)}'}), 500
    



#Servicio que muestre datos de consultas:
@app.route('/contactos', methods=['GET'])
def contacts():
    conn = engine.connect()
    query = """
        SELECT * FROM contactos;
    """
    try:
        result = conn.execute(text(query))
        conn.close()
        contactos = []
        for row in result:
            contacto = {
                "id": row.id,
                "asunto": row.asunto,
                "mensaje": row.mensaje,
                "nombre": row.nombre,
                "mail": row.mail
            }
            contactos.append(contacto)
        return jsonify(contactos), 200
    except SQLAlchemyError as e:
        return jsonify({'message': f'Error al obtener datos de contactos: {str(e)}'}), 500
    



#Servicio que agrega el mensaje con su nombre mail y asunto a la tabla de contactos.
@app.route('/agregar_contacto', methods = ['POST'])
def create_contact():
    conn = engine.connect()
    contacto = request.get_json()
    query = f"""INSERT INTO contactos (nombre, mail, asunto, mensaje) VALUES ('{contacto['nombre']}','{contacto['mail']}', '{contacto['asunto']}', '{contacto['mensaje']}');"""
    query_validation = f"""SELECT * FROM contactos WHERE nombre = '{contacto['nombre']}' AND mail = '{contacto['mail']}' AND asunto = '{contacto['asunto']}' AND mensaje = '{contacto['mensaje']}' ;"""
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount == 0:
            result = conn.execute(text(query))

            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({'message':'Ya agregaste el mensaje de ese contacto.'}), 404
        
    except SQLAlchemyError as e:
        return jsonify({'message':f'Ocurrio un error al agregar contactos: {str(e)}'}), 500

    return jsonify({'message':f'Se ha agregado correctamente el contacto'}), 200





#Servicio que elimina contacto(admin):
@app.route('/eliminar_contacto', methods = ['DELETE'])    
def delete_contact():
    conn = engine.connect()
    del_cont = request.get_json()
    id = del_cont.get('id',None)
    if not id:
        return jsonify({'message': 'Se requiere id para eliminar el contacto'}), 400

    query = f"""DELETE FROM contactos WHERE id = {id};"""
    validation_query = f"""SELECT * FROM contactos WHERE id = {id};"""
    try:
        val_result = conn.execute(text(validation_query))
        if val_result.rowcount != 0 :
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({"message": f"La consulta número {id} no existe."}), 404
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    return jsonify({'message': 'Se ha eliminado correctamente'}), 202  




if __name__ == "__main__":
    app.run("127.0.0.1", port="5001", debug=True)