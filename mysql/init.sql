CREATE TABLE reservas (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    numero_habitacion INT NOT NULL,
    huespedes INT NOT NULL,
    fecha_ingreso DATE NOT NULL,
    cantidad_noches INT NOT NULL,
    nombre VARCHAR(60) NOT NULL,
    mail VARCHAR(120) NOT NULL
    
);

CREATE TABLE habitaciones (
    numero INT NOT NULL PRIMARY KEY,
    precio INT NOT NULL,
    capacidad INT NOT NULL,
    descripcion VARCHAR(500)
);




GRANT ALL PRIVILEGES ON tp_database.* TO 'usuario'@'%' IDENTIFIED BY 'scrumbeasts';
FLUSH PRIVILEGES;