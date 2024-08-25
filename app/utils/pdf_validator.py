import fitz
from fastapi import HTTPException, UploadFile


async def validate_pdf(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Uploaded file is not a PDF.")

    try:
        file_content = await file.read()
        pdf_document = fitz.open(stream=file_content, filetype="pdf")

        if pdf_document.page_count == 0:
            raise HTTPException(status_code=400, detail="PDF has no pages.")

        file.file.seek(0)
        pdf_document.close()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid PDF file.")
