import PyPDF2
from py_pdf_parser.loaders import load_file
import json
import re
import fitz
import os

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
        document = load_file(pdf_path)
        title_font = []
        subheading_font = []
        nested_subheading_font = []
        content_font = []
        ignored_font = []

        data = {}
        title_policy = []
        current_subheading = None
        current_nested_subheading = None

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

    def parse_pdf_using_pymupdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            output = page.get_text("blocks")
            previous_block_id = 0
            for block in output:
                if block[6] == 0:
                    if previous_block_id != block[5]:
                        text += "\n"
                    text += block[4] + "\n"
                    previous_block_id = block[5]
        return text

    def save_output_to_file(self, output, method_name):
        # Ensure the output directory exists
        output_dir = os.path.dirname(method_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(f"{method_name}.txt", "w") as file:
            if isinstance(output, dict):
                file.write(json.dumps(output, indent=4))
            else:
                file.write(output)

# Example usage:
# extractor = TextExtractor()
# extracted_text_pypdf2 = extractor.parse_pdf_using_PyPDF2('/path/to/your/pdf')
# parsed_data_pypdfparser = extractor.parse_pdf_using_py_pdf_parser('/path/to/your/pdf')
# extracted_text_pymupdf = extractor.parse_pdf_using_pymupdf('/path/to/your/pdf')

# extractor.save_output_to_file(extracted_text_pypdf2, "output/parse_pdf_using_PyPDF2")
# extractor.save_output_to_file(parsed_data_pypdfparser, "output/parse_pdf_using_py_pdf_parser")
# extractor.save_output_to_file(extracted_text_pymupdf, "output/parse_pdf_using_pymupdf")