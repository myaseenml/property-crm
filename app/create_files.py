from docx import Document
from django.http import FileResponse
from django.templatetags.static import static

def create_invoice(date, fullname, unit_no, area, unit_type, annual_rent, sec_deposite, agency_fee):
    doc_path = static('docs/offer_letter.docx')
    doc = Document(doc_path)

    # Define the text to be replaced and the replacement text
    text_to_replace = ['temptempdate', 'temptempdatefullname', 'temptempuno', 'temptemparea', 'temptempdateutype', 'temptempannrent', 'temptempsec', 'temptempagenfee']
    replacement_text = [date, fullname, unit_no, area, unit_type, annual_rent, sec_deposite, agency_fee]

    # Iterate through the paragraphs in the document
    for paragraph in doc.paragraphs:
        for old_text, new_text in zip(text_to_replace, replacement_text):
            if old_text in paragraph.text:
                paragraph.text = paragraph.text.replace(old_text, new_text)

    doc.save('modified_document.docx')

    modified_doc = open('modified_document.docx', 'rb')
    response = FileResponse(modified_doc)
    response['Content-Disposition'] = 'attachment; filename="modified_document.docx"'
    return response

create_invoice('temp2', 'temp2', 'temp2', 'temp2', 'temp2', 'temp2', 'temp2', 'temp2')