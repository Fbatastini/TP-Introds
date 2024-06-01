CREATE TABLE reservas (
    numero_reserva INT NOT NULL PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    mail VARCHAR(120) NOT NULL,
    tipo_habitacion VARCHAR(10) NOT NULL,
    cantidad_personas INT NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_salida DATE NOT NULL
);

CREATE TABLE habitaciones (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tipo_habitacion VARCHAR(10) NOT NULL,
    cantidad_total INT NOT NULL
)

