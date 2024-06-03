# db table queries
create_habitaciones_table = """
    CREATE TABLE IF NOT EXISTS habitaciones (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tipo_habitacion VARCHAR(50),
        cantidad INT
    )
"""

create_reservas_table = """
    CREATE TABLE IF NOT EXISTS reservas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100),
        mail VARCHAR(100),
        tipo_habitacion VARCHAR(50),
        cant_personas INT,
        check_in DATE,
        check_out DATE
    )
"""

create_dias_reservados_table = """
    CREATE TABLE IF NOT EXISTS dias_reservados (
        id_reserva INT,
        dia DATE,
        tipo_habitacion VARCHAR(50),
        FOREIGN KEY (id_reserva) REFERENCES reservas(id)
    )
"""