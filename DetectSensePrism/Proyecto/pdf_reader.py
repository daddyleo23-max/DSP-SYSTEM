# pdf_reader/pdf_reader.py

import re
from PyPDF2 import PdfReader

def extraer_datos_pdf(ruta_pdf):
    reader = PdfReader(ruta_pdf)
    texto = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
    texto = texto.upper()

    # --------------------
    # EXTRAER DATOS DEL CURSO
    # --------------------
    curso = {
        'periodo_escolar': extraer_dato_bloque(texto, r'PERIODO ESCOLAR\s*\n(.*?)\n'),
        'ciclo_estudios': extraer_dato_bloque(texto, r'CICLO DE ESTUDIOS\s*\n(.*?)\n'),
        'departamento_academico': extraer_dato_bloque(texto, r'DEPARTAMENTO ACADEMICO\s*\n(.*?)\n'),
        'materia': '',
        'clave': '',
        'grupo': '',
        'rfc_catedratico': '',
        'nombre_catedratico': '',
        'horario': '',
        'alumnos': []
    }

    # MATERIA, CLAVE y GRUPO están juntos
    match_mcg = re.search(r'MATERIA CLAVE GRUPO\s*\n(.*?)\s+([A-Z0-9]+)\s+([A-Z0-9]+)', texto)
    if match_mcg:
        curso['materia'] = match_mcg.group(1).strip()
        curso['clave'] = match_mcg.group(2).strip()
        curso['grupo'] = match_mcg.group(3).strip()

    # RFC y CATEDRATICO
    match_rfc = re.search(r'RFC CATEDRATICO\s*\n([A-Z0-9]+)\s+(.*?)\n', texto)
    if match_rfc:
        curso['rfc_catedratico'] = match_rfc.group(1).strip()
        curso['nombre_catedratico'] = match_rfc.group(2).strip()

    # HORARIO
    match_horario = re.search(r'HORARIO\s*\n(.*?)\n', texto)
    if match_horario:
        curso['horario'] = match_horario.group(1).strip()

    # ALUMNOS
    alumnos = []
    for match in re.finditer(r'(\d+)\s+(.*?)\s+(\d+)', texto):
        alumnos.append({
            'numero_control': match.group(1).strip(),
            'nombre': match.group(2).strip(),
            'matricula': match.group(3).strip()
        })
    curso['alumnos'] = alumnos

    return curso


def extraer_dato_bloque(texto, patron):
    match = re.search(patron, texto)
    return match.group(1).strip() if match else ''
