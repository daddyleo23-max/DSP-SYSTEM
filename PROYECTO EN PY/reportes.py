from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generar_reporte_inicio_curso(clase, grupo, alumnos):
    filename = f"inicio_curso_{clase}_{grupo}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Cabecera
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "INSTITUTO TECNOLÓGICO DE PACHUCA")
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Clase: {clase} - Grupo: {grupo}")
    
    # Lista de alumnos
    y = 700
    for alumno in alumnos:
        c.drawString(100, y, f"• {alumno['nombre']} ({alumno['control']})")
        y -= 20
    
    c.save()
    return filename