import os

from docx import Document


def get_docx_chunk(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    doc = Document()
    doc.add_paragraph(text)
    temp = 'temp.docx'
    doc.save(temp)
    with open(temp, 'rb') as f:
        chunk = f.read()
    os.remove(temp)
    return chunk
