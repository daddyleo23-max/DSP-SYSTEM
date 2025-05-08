-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS asistencia;
USE asistencia;

-- Tabla de clases/asignaturas
CREATE TABLE IF NOT EXISTS cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    grupo VARCHAR(50) NOT NULL,
    profesor VARCHAR(255),
    horario VARCHAR(100)
);

-- Tabla de alumnos
CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    numero_control VARCHAR(50) NOT NULL,
    curso_id INT NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES cursos(id)
);
