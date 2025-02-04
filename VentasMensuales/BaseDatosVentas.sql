CREATE DATABASE VentasDB;
USE VentasDB;

CREATE TABLE ventas_mensuales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mes VARCHAR(20),
    ventas INT
);
