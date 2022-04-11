from PyPDF2 import PdfFileMerger
import os

pdfs = [archivo for archivo in os.listdir('./') if archivo.endswith(".pdf")]
nombre_archivo_salida = "salida.pdf"
fusionador = PdfFileMerger()

for pdf in pdfs:
    fusionador.append(open(pdf, 'rb'))

with open(nombre_archivo_salida, 'wb') as salida:
    fusionador.write(salida)