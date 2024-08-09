from llama_parse import LlamaParse
import os
import re
import nest_asyncio
import json

nest_asyncio.apply()

class LlamaTextExtractor:
    def __init__(self):
        os.environ["LLAMA_CLOUD_API_KEY"] = "YOUR_API_KEY_HERE"

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
                               parsing_instruction="").load_data(pdf_path)

        markdown_text = ""
        for i in range(len(documents)):
            markdown_text += documents[i].text + '\n'

        parsed_dict = self.parse_markdown_to_dict(markdown_text)
        return parsed_dict

    def save_output_to_file(self, output, file_path):
        # Ensure the output directory exists
        output_dir = os.path.dirname(file_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the output to a file
        with open(f"{file_path}.txt", "w") as file:
            if isinstance(output, dict):
                file.write(json.dumps(output, indent=4))
            else:
                file.write(output)

# Example usage:
# llama_extractor = LlamaTextExtractor()
# llama_parsed_data = llama_extractor.parse_pdf_using_llama('/path/to/pdf_file.pdf')
# llama_extractor.save_output_to_file(llama_parsed_data, "output/llama_parsed_data")