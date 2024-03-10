import requests
from PyPDF2 import PdfReader
from io import BytesIO
from typing import Any, Optional, Type
from gentopia.tools.basetool import BaseModel, BaseTool, Field

class PDFReadArgs(BaseModel):
    file_path_or_url: str = Field(..., description="")

class PDFTool(BaseTool):
    """Tool that reads text from PDF files, including those available online."""

    name = "pdf_tool"
    description = "A tool for reading text from PDF files."
    args_schema: Optional[Type[BaseModel]] = PDFReadArgs

    def read_pdf(self, file_path_or_url: str) -> str:
        if file_path_or_url.startswith(('http://', 'https://')):
            response = requests.get(file_path_or_url, stream=True)
            response.raise_for_status()  # Ensure the request was successful
            if response.headers['Content-Type'] == 'application/pdf':
                file = BytesIO(response.content)
            else:
                raise ValueError("URL did not point to a PDF file.")
        else:
            file = open(file_path_or_url, "rb")

        try:
            pdf = PdfReader(file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        finally:
            file.close()

        return text.strip()

        return text.strip()

    def split_text(self, text, max_length=3000):
        return [text[i:i+max_length] for i in range(0, len(text), max_length)]

    def process_text_chunks(self, text):

        chunks = self.split_text(text)
        for chunk in chunks:
            print(chunk[:50])

    def _run(self, file_path_or_url: str) -> str:
        extracted_text = self.read_pdf(file_path_or_url)
        print(extracted_text)
        self.process_text_chunks(extracted_text)
        return "Text processing complete."

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    pdf_tool = PDFTool()
    print(pdf_tool._run(file_path_or_url=""))
