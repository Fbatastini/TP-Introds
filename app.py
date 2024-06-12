"""api module"""
from flask import Flask
from sqlalchemy import create_engine

from endpoints import room, booking, contact, verifications

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root:scrumbeasts@localhost:3309/tp_database")

#Servicio que consulta disponibilidad:
@app.route('/disponibilidad', methods = ['GET'])
<<<<<<< HEAD
def disponibility():   
    conn = engine.connect()
    
    consulta = request.get_json() #diccionario que contiene fecha huespedes, ingreso y noches
    huespedes = consulta['huespedes'] 
    
    #Chequeo que la fecha sea correcta
    try:
        fecha_ingreso = datetime.strptime(consulta['fecha_ingreso'], '%Y-%m-%d')
    except Exception:
        return jsonify({'message': 'La fecha ingresada no existe.'}), 400
    
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


=======
def disponibility():
    return verifications.disponibility(engine)
>>>>>>> 6a940d9 (ajusted de handlers y de endpoints)


#Servicio que verifica si existe el usuario y su contraseña:
@app.route('/user/<user>/<password>', methods=['GET'])
def verificar_usuario(user, password):
<<<<<<< HEAD
    conn = engine.connect()

    query = f"""Select * FROM usuarios WHERE usuario = '{user}' and clave = '{password}'"""

    try:
        result = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as e:
        return jsonify(str(e.__cause__)), 500
    
    if result.rowcount != 0:
        return jsonify({'message':'exists'}), 200
    else:
        return jsonify({'message':'does not exist'}), 404


=======
    return verifications.verificar_usuario(user, password, engine)
>>>>>>> 6a940d9 (ajusted de handlers y de endpoints)


#Servicio que muestre datos de habitaciones(promociones incluidas):
@app.route('/habitaciones', methods=['GET'])
def room_end():
    return room.room(engine)


#Servicio que hace reserva:
@app.route('/reserva', methods=['POST'])
<<<<<<< HEAD
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
            return jsonify({"message": "Reserva realizada con éxito"}), 201
        else:
            conn.close()
            return jsonify({"message": f"La habitación número {new_booking['numero_habitacion']} ya se encuentra reservada en las fechas seleccionadas"}), 400
    except Exception as e:
        conn.close()
        return jsonify({'message': f"Error al realizar la reserva: {str(e)}"}), 500


=======
def booking_end():
    return booking.booking(engine)
>>>>>>> 6a940d9 (ajusted de handlers y de endpoints)


#Servicio que cancela reserva:
@app.route('/cancelar_reserva', methods=['DELETE'])
<<<<<<< HEAD
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
            return jsonify({"message": "Reserva cancelada con éxito"}), 202
        else:
            conn.close()
            return jsonify({"message": "No se encontró una reserva con el ID proporcionado"}), 404
    except Exception as e:
        conn.close()
        return jsonify({"message": f"Error al cancelar la reserva: {str(e)}"}), 500


=======
def cancel_booking():
    return booking.cancel_booking(engine)
>>>>>>> 6a940d9 (ajusted de handlers y de endpoints)


#Servicio que cambia cantidad de noches, o dia de check in:
@app.route('/cambiar_reserva', methods=['PATCH'])
def change_booking():
<<<<<<< HEAD
    conn = engine.connect()
    mod_booking_data = request.get_json()

    id_reserva = mod_booking_data.get('id')
    numero_habitacion = mod_booking_data.get('numero_habitacion')
    nueva_fecha_ingreso = mod_booking_data.get('nueva_fecha_ingreso')
    nuevas_noches = mod_booking_data.get('nuevas_noches')

    # Validar si la habitación existe en la base de datos
    query_validation = f"SELECT * FROM reservas WHERE id = {id_reserva};"
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount == 0:
            conn.close()
            return jsonify({'message': f"No existe la reserva id {id_reserva}"}), 404
    except SQLAlchemyError as err:
        return jsonify({'message': str(err.__cause__)}), 500

    # Actualizar la reserva
    query = f"""UPDATE reservas
                SET fecha_ingreso = '{nueva_fecha_ingreso}', cantidad_noches = {nuevas_noches}
                WHERE id = {id_reserva};"""
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify({'message': str(err.__cause__)}), 500

    return jsonify({'message': 'Se ha modificado la reserva correctamente'}), 200


=======
    return booking.change_booking(engine)
>>>>>>> 6a940d9 (ajusted de handlers y de endpoints)



#Servicio que agrega habitacion(admin):
@app.route('/agregar_habitacion', methods = ['POST'])
<<<<<<< HEAD
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
        return jsonify({'message': f'Se ha producido un error'}), 500
    
    return jsonify({'message': 'Se ha agregado correctamente'}), 201


=======
def create_room():
    return room.create_room(engine)
>>>>>>> 6a940d9 (ajusted de handlers y de endpoints)


#Servicio que elimina habitacion(admin):
@app.route('/eliminar_habitacion', methods = ['DELETE'])
def delete_room():
<<<<<<< HEAD
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
        return jsonify(str(err.__cause__)), 500
    return jsonify({'message': 'Se ha eliminado correctamente'}), 202


=======
    return room.delete_room(engine)
>>>>>>> 6a940d9 (ajusted de handlers y de endpoints)


#Servicio que cambia el precio de una habitacion(modo admin):
@app.route('/cambiar_precio', methods = ['PATCH'])
def change_price():
<<<<<<< HEAD
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
        return jsonify({'message': str(err.__cause__)}), 500
    
    return jsonify({'message': 'Se ha modificado correctamente'}), 200


=======
    return room.change_price(engine)
>>>>>>> 6a940d9 (ajusted de handlers y de endpoints)


#Servicio que cambia las promociones de las habitaciones(modo admin):
@app.route('/cambiar_promocion', methods=['PATCH'])
def change_promo():
    return room.change_promo(engine)


#Servicio que muestre datos de reservas:
@app.route('/reservas', methods=['GET'])
def bookings():
    return booking.bookings(engine)


#Servicio que muestre datos de consultas:
@app.route('/contactos', methods=['GET'])
def contacts_end():
    return contact.contacts(engine)


#Servicio que agrega el mensaje con su nombre mail y asunto a la tabla de contactos.
@app.route('/agregar_contacto', methods = ['POST'])
def create_contact():
<<<<<<< HEAD
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

    return jsonify({'message':f'Se ha agregado correctamente el contacto'}), 201



=======
    return contact.create_contact(engine)
>>>>>>> 6a940d9 (ajusted de handlers y de endpoints)


#Servicio que elimina contacto(admin):
@app.route('/eliminar_contacto', methods = ['DELETE'])
def delete_contact():
<<<<<<< HEAD
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
        return jsonify(str(err.__cause__)), 500
    return jsonify({'message': 'Se ha eliminado correctamente'}), 202  


=======
    return contact.delete_contact(engine)
>>>>>>> 6a940d9 (ajusted de handlers y de endpoints)


if __name__ == "__main__":
    app.run("127.0.0.1", port="5001", debug=True)
