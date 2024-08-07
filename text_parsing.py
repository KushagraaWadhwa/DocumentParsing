# text_extractor.py
import PyPDF2
from py_pdf_parser.loaders import load_file
import json
import re
import fitz
from llama_parse import LlamaParse


class TextExtractor:
    def __init__(self):
        pass

    def parse_pdf_using_PyPDF2(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            text = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
        return text

    def parse_pdf_using_py_pdf_parser(self, pdf_path):
        # Load the PDF document
        document = load_file(pdf_path)

        # Checking the fonts
        all_elements = document.elements
        # Define font categories
        title_font = []
        subheading_font = []
        nested_subheading_font = []
        content_font = []
        ignored_font = []

        # Initialize data structures
        data = {}
        title_policy = []
        current_subheading = None
        current_nested_subheading = None

        # Iterate through elements in the document
        for element in document.elements:
            try:
                if element.font in ignored_font:
                    continue
                elif element.font in title_font:
                    title_policy.append(element.text().strip())
                elif element.font in subheading_font:
                    current_subheading = element.text().strip()
                    current_nested_subheading = None
                    data[current_subheading] = {"content": "", "nested": {}}
                elif element.font in nested_subheading_font:
                    if current_subheading:
                        current_nested_subheading = element.text().strip()
                        data[current_subheading]["nested"][current_nested_subheading] = ""
                elif element.font in content_font:
                    if current_nested_subheading:
                        data[current_subheading]["nested"][current_nested_subheading] += " " + element.text().strip()
                    elif current_subheading:
                        data[current_subheading]["content"] += " " + element.text().strip()
            except Exception as e:
                print(f"Skipping element due to exception: {str(e)}")

        # Prepare the output data
        output_data = {
            "title_policy": title_policy,
            "content": data
        }
        return output_data

    def parse_markdown_to_dict(self, markdown_text):
        lines = markdown_text.split('\n')
        result = {}
        current_key = None
        current_content = []
        metadata_pattern = re.compile(r'^(Version Control:|Document Author:|For Internal Circulation Only|Released on)')

        for line in lines:
            if line.startswith('#'):
                if current_key:
                    result[current_key] = '\n'.join(current_content).strip()
                current_key = line.strip('# ')
                current_content = []
            elif not metadata_pattern.match(line) and not line.strip().startswith('Deutsche Telekom'):
                current_content.append(line)

        if current_key:
            result[current_key] = '\n'.join(current_content).strip()

        return result

    def parse_pdf_using_llama(self, pdf_path):
        documents = LlamaParse(result_type="markdown", do_not_unroll_columns=True,
                               parsing_instruction="This is a company policy document. I want accurate and exact details about each heading or subheading, do not generate content on your own.").load_data(pdf_path)

        markdown_text = ""
        for i in range(len(documents)):
            markdown_text += documents[i].text + '\n'

        parsed_dict = self.parse_markdown_to_dict(markdown_text)
        return parsed_dict

    def parse_pdf_using_pymupdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            output = page.get_text("blocks")
            previous_block_id = 0
            for block in output:
                if block[6] == 0:  # We only take the text
                    if previous_block_id != block[5]:
                        text += "\n"
                    text += block[4] + "\n"
                    previous_block_id = block[5]
        return text


# Example usage:
# extractor = TextExtractor()
# extracted_text = extractor.extract_text_from_pdf('/path/to/pdf_file.pdf')
# parsed_data = extractor.parse_pdf_using_py_pdf_parser('/path/to/pdf_file.pdf')
# llama_parsed_data = extractor.parse_pdf_using_llama('/path/to/pdf_file.pdf')
# pymupdf_text = extractor.extract_text_from_pdf_using_pymupdf('/path/to/pdf_file.pdf')
