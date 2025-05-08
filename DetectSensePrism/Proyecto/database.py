# database/database.py

import pymysql
from config import DB_CONFIG
from pdf_reader import extraer_datos_pdf

def conectar_bd():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def insertar_datos_pdf(datos):
    try:
        conexion = conectar_bd()
        with conexion.cursor() as cursor:
            # Insertar curso
            sql_curso = """
                INSERT INTO cursos 
                (periodo_escolar, ciclo_estudios, departamento_academico, materia, clave, grupo, rfc_catedratico, nombre_catedratico, horario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_curso, (
                datos['periodo_escolar'], datos['ciclo_estudios'], datos['departamento_academico'],
                datos['materia'], datos['clave'], datos['grupo'], datos['rfc_catedratico'],
                datos['nombre_catedratico'], datos['horario']
            ))
            curso_id = cursor.lastrowid

            # Insertar alumnos
            sql_alumno = "INSERT INTO alumnos (numero_control, nombre, curso_id) VALUES (%s, %s, %s)"
            for alumno in datos['alumnos']:
                cursor.execute(sql_alumno, (alumno['numero_control'], alumno['nombre'], curso_id))

        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al insertar datos: {e}")
        return False
