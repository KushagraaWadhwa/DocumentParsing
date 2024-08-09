import fitz  # PyMuPDF
import pandas as pd
import camelot
import os

class PyMUCamelot_Extractor:
    def __init__(self, pdf_document, output_image_dir):
        self.pdf_path = pdf_document
        self.output_image_dir = output_image_dir
        self.extracted_text = ""
        self.doc = fitz.open(self.pdf_path)  # Corrected this line

    def extract_tables_from_pdf(self, page_num):
        tables = camelot.read_pdf(self.pdf_path, pages=str(page_num))
        return tables

    def table_to_markdown(self, df):
        return df.to_markdown(index=False)

    def save_image(self, image_bytes, image_ext, page_num, image_index):
        if not os.path.exists(self.output_image_dir):
            os.makedirs(self.output_image_dir)
        image_filename = f"page_{page_num + 1}_image_{image_index}.{image_ext}"
        image_path = os.path.join(self.output_image_dir, image_filename)
        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)
        return image_path

    def extract_text_block_wise(self, page):
        output = page.get_text("blocks")
        previous_block_id = 0  # Set a variable to mark the block id
        text = ""
        for block in output:
            if block[6] == 0:  # We only take the text
                if previous_block_id != block[5]:
                    text += "\n"
                text += block[4]
                previous_block_id = block[5]  # Update previous block id
        return text

    def process_pdf(self):
        extracted_text = ""
        for page_num in range(self.doc.page_count):
            page = self.doc[page_num]
            # Extract text block-wise and perform replacements
            page_text = self.extract_text_block_wise(page)
            page_text = page_text.replace('Deutsche Telekom Digital Labs Private Limited ', "")
            page_text = page_text.replace('Version Control: V.6.0, Released on 01-April-2024', "")
            page_text = page_text.replace('Document Author: Nihar Mathur ', "")
            page_text = page_text.replace('For Internal Circulation Only', "")
            
            # Extract and display tables using Camelot
            tables = self.extract_tables_from_pdf(page_num + 1)
            if tables:
                print(f"[+] Found {len(tables)} table(s) on page {page_num + 1}")
                for table_index, table in enumerate(tables, start=1):
                    df = table.df
                    table_metadata = f"[Table {table_index} on page {page_num + 1}]"
                    page_text += "\n" + table_metadata + "\n" + self.table_to_markdown(df) + "\n"
            else:
                print(f"[!] No tables found on page {page_num + 1}")
            
            # Extract and display images
            image_list = page.get_images(full=True)
            if image_list:
                print(f"[+] Found a total of {len(image_list)} images on page {page_num + 1}")
                for image_index, img in enumerate(image_list, start=1):
                    xref = img[0]
                    base_image = self.doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image_path = self.save_image(image_bytes, image_ext, page_num, image_index)
                    image_metadata = f"[Image {image_index} on page {page_num + 1}: xref={xref}, ext={image_ext}]"
                    page_text += "\n" + image_metadata + "\n"
            else:
                print(f"[!] No images found on page {page_num + 1}")
            
            extracted_text += page_text
        self.doc.close()
        with open(f"output/PyMUCamelot_Parsed_{self.pdf_path.split('/')[-1].split('.')[0]}.txt", 'w') as f:
            f.write(extracted_text)
        return extracted_text, len(extracted_text.split())
    

# Example usage:
# pdf_document = "/Users/kushagrawadhwa/Desktop/PDF_parsing phase-2/source_docs/policy2.pdf"
# output_image_dir = "./extracted_images"
# pdf_extractor = PyMUCamelot_Extractor(pdf_document=pdf_document, output_image_dir=output_image_dir)
# extracted_text, word_count = pdf_extractor.process_pdf()
# print(f"The Extracted text is as follows:\n{extracted_text}")
# print(f"Total words in the document: {word_count}")