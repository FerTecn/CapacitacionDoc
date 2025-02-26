from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors

def draw_table(data, col_widths, styles):
    processed_data = []
    
    for fila in data:
        processed_row = []
        
        for i, celda in enumerate(fila):
            contenido = str(celda)
            if fila == data[0]:
                paragraph = contenido
            else:
                contenido = Paragraph(contenido, styles['Normal'])
            processed_row.append(contenido)
        
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
