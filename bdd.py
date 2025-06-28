# ESTO ES PARA LA CREACION DE LA BASE DE DATOS Y PARA LA CREACION DE LA TABLA Usuarios
import sqlite3 as sq

conexion = sq.connect("GestionUsuarios")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE Usuarios(
id CHAR(4) PRIMARY KEY, 
nombre VARCHAR(50),
password VARCHAR(50),
apellido VARCHAR(50),
direccion VARCHAR(50),
texto TEXT
)
""")


conexion.commit()
conexion.close()