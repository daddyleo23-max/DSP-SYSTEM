import mysql.connector
from NitgenSDK import HamsterII  # SDK proporcionado por Nitgen

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="admin_dsp",
            password="DSP_2025",
            database="DetectSensePrism"
        )
        self.lector = HamsterII.inicializar()

    def registrar_huella(self, alumno_id):
        try:
            template = self.lector.capturar_huella()
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE alumnos SET huella = %s WHERE id = %s",
                (template, alumno_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al registrar huella: {e}")
            return False