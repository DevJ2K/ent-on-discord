from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter


document = PdfFileReader(open("menuCantine1.pdf", 'rb'))

pdftext = ""
for page in range(document.numPages):
    pageObj = document.getPage(page)
    pdftext += pageObj.extractText().replace('\n','')

print(pdftext)