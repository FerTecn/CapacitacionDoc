import re

from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
def text_processor(texto):
    """
    Procesa el texto que contenga saltos de linea para mostrarlos correctamente.
    - Sustituye dobles saltos de línea (\n\n) por un salto de párrafo.
    - Sustituye saltos de línea simples (\n) por <br/>.
    - Se asegura de que el texto procesado esté correctamente formateado.
    """

    # Reemplazar saltos de línea (\n) por <br/>
    texto = texto.replace("\n", "<br/>")
    
    # Reemplazar dobles saltos de línea (\n\n) por un salto de párrafo <p></p>
    texto = re.sub(r'(\n\s*\n)', r'</p><p>', texto)
    
    # Asegurarnos de que el texto comience y termine dentro de <p> tags
    if not texto.startswith('<p>'):
        texto = '<p>' + texto
    if not texto.endswith('</p>'):
        texto = texto + '</p>'

    return texto

def cell_text_processor(texto):
    """
    Procesa el texto dentro de una celda de tabla.
    - Sustituye dobles saltos de línea (\n\n) por viñetas.
    - Sustituye saltos de línea simples (\n) por <br/>.
    - Se asegura de que el texto procesado esté correctamente formateado.
    """

    # Reemplazar dobles saltos de línea (\n\n) por una viñeta y un salto de línea
    texto = re.sub(r'\n\s*\n', r'<br/>• ', texto)

    # Si el texto no contiene viñetas, asegurarse de que la primera línea también tenga una
    if not "•" in texto:
        texto = "• " + texto.lstrip()

    # Reemplazar saltos de línea simples (\n) por <br/> y una viñeta
    texto = texto.replace("\n", "<br/>• ")

    return texto

def draw_table(data_table, col_widths, style):
    """
    Crea la estructura de tabla.
    - Establece los encabezados de la tabla.
    - Formatea y procesa el texto de la celda si es que contiene viñetas.
    - Define el tamaño de las columnas.
    - Establece el estilo de la tabla.
    """
    processed_data = []
    columna_actividades = False #Rastrea la columna donde se requieren viñetas
    
    for fila in data_table:
        processed_row = []
        for i, celda in enumerate(fila):
            contenido = str(celda)
            if fila == data_table[0]:
                paragraph = contenido
                #Rastrea la columna
                if celda=="Actividades de Aprendizaje":
                    columna_actividades = True
            else:
                # Si la columna es donde se requiere viñetas, se usa el procesador de celdas
                if columna_actividades and i==2:
                    contenido = cell_text_processor(contenido)
                else:
                    contenido = contenido
                paragraph = Paragraph(contenido, style)
            processed_row.append(paragraph)
        
        processed_data.append(processed_row)
    
    table = Table(processed_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("VALIGN", (0, 1), (-1, -1), "TOP"),
    ]))
    return table


def draw_table_firma(data_table, col_widths):
    table = Table(data_table, colWidths=col_widths)
    table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return table

def draw_table_diagnosticos(data_table, col_widths, style_bold_center, style_normal_center):
    processed_data = []
    for row_idx, fila in enumerate(data_table):
        processed_row = []
        for col_idx, celda in enumerate(fila):
            # Encabezado (primera fila) - style_bold_center
            if row_idx == 0:
                paragraph = Paragraph(str(celda), style_bold_center)
            else:
                # Aplicar viñetas solo a la columna "Contenidos Temáticos" (col_idx == 1)
                if col_idx == 1 and "Contenidos Temáticos" in data_table[0]:
                    contenido = cell_text_processor(str(celda))
                else:
                    contenido = str(celda)
                paragraph = Paragraph(contenido, style_normal_center)
            processed_row.append(paragraph)
        processed_data.append(processed_row)

    table = Table(processed_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Fondo gris para encabezado
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),  # Texto blanco encabezado
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),  # Bordes negros
        ("FONTNAME", (0, 0), (-1, 0), "Montserrat-Bold"),  # Negrita para encabezado
    ]))
    return table