from pypdf import PdfReader
from config import PDF_PATH

def load_pdf(pdf_path=PDF_PATH):
    """
    Reads a PDF and returns all extracted text.
    """

    reader = PdfReader(pdf_path)

    text = ""

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

if __name__ == "__main__":

    extracted_text = load_pdf()

    print("=" * 100)
    print("PDF SUCCESSFULLY LOADED")
    print("=" * 100)

    print(f"Total Characters : {len(extracted_text)}")
    print(f"Total Words      : {len(extracted_text.split())}")
    print()

    print("=" * 100)
    print("TEXT PREVIEW")
    print("=" * 100)

    print(extracted_text[:1500])