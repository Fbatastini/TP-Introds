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

CREATE TABLE usuarios (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(30) NOT NULL,
    clave VARCHAR(20) NOT NULL
);


/* Agrego datos a tabla reservas */ 
INSERT INTO reservas (numero_habitacion, huespedes, fecha_ingreso, cantidad_noches, nombre, mail) VALUES (1, 4, "2024-06-15", 6, "Felipe", "felipe@gmail.com");
INSERT INTO reservas (numero_habitacion, huespedes, fecha_ingreso, cantidad_noches, nombre, mail) VALUES (3, 2, "2024-06-17", 4, "Julian", "julian@gmail.com");
INSERT INTO reservas (numero_habitacion, huespedes, fecha_ingreso, cantidad_noches, nombre, mail) VALUES (2, 3, "2024-06-18", 5, "Florencia", "florencia@gmail.com");

/* Agrego datos a tabla habitaciones */
INSERT INTO habitaciones (numero, precio, capacidad, descripcion) VALUES (1, 5000, 5, "Tipo de habitacion: Normal. Muy buenas vistas a la ciudad.");
INSERT INTO habitaciones (numero, precio, capacidad, descripcion) VALUES (2, 3000, 3, "Tipo de habitacion: Normal. Camas muy comodas.");
INSERT INTO habitaciones (numero, precio, capacidad, descripcion) VALUES (3, 8000, 2, "Tipo de habitacion: Premium. Muy buenas vistas a la ciudad.");
INSERT INTO habitaciones (numero, precio, capacidad, descripcion) VALUES (4, 7000, 6, "Tipo de habitacion: Normal. Muy espaciosa.");
INSERT INTO habitaciones (numero, precio, capacidad, descripcion) VALUES (5, 200000, 2, "Tipo de habitacion: Deluxe. Suit presidencial.");

/* Agrego datos a tabla usuarios */ 
INSERT INTO usuarios (usuario, clave) VALUES ("admin1", "1234");
INSERT INTO usuarios (usuario, clave) VALUES ("admin2", "5678");


GRANT ALL PRIVILEGES ON tp_database.* TO 'usuario'@'%' IDENTIFIED BY 'scrumbeasts';
FLUSH PRIVILEGES;