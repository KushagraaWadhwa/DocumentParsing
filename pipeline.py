from py_pdf_parser.loaders import load_file
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline, AutoModelWithLMHead, AutoModelForSeq2SeqLM, BertForQuestionAnswering, GPT2LMHeadModel, GPT2Tokenizer
import pandas as pd
import torch
import os
import re
import json
import csv
import camelot
from llama_parse import LlamaParse
import nest_asyncio
nest_asyncio.apply()


class TextExtractor:
    def __init__(self, config):
        self.config = config
        self.output_folder = config.get('output_folder', 'output')

    def get_text_parsing_module(self):
        if self.config['text_parsing'] == 'pypdfparser':
            return self.parse_text_with_pypdfparser
        elif self.config['text_parsing'] == 'pypdf2':
            return self.parse_text_with_pypdf2

    def parse_text_with_pypdfparser(self, file_path):
        try:
            title_font = ['BCDFEE+TrebuchetMS-Bold,18.0', 'GZRTRE+TrebuchetMS-Bold,18.0',
              'BCDEEE+Calibri-Bold,24.0', 'BCDEEE+Calibri-Bold,28.0']
            subheading_font = ["ORLRHD+Calibri-Bold,13.9", "BCDGEE+Calibri-Bold,14.0",
                            'BCDEEE+Calibri-Bold,16.0', 'BCDEEE+Calibri-Bold,16.6']
            nested_subheading_font = ['BCDEEE+Calibri-Bold,12.0','BCDJEE+Calibri-Bold,12.0','BCDEEE+Calibri-Bold,13.0', 'BCDEEE+Calibri-Bold,13.0']
            content_font = ["RPVPOE+Calibri,12.0", 'BCDEEE+Calibri,12.0', 'BCDGEE+Calibri-BoldItalic,12.0',
                            'BCDHEE+Calibri,12.0', 'BCDIEE+Calibri-BoldItalic,12.0',
                            'BCDKEE+Calibri-Italic,12.0', 'BCDNEE+Calibri-Italic,11.0', 'BCDFEE+Calibri,12.0']
            ignored_font = ['ArialMT,8.0']
            document = load_file(file_path)
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

            output_data = {"title_policy": title_policy, "content": data}
            os.makedirs(self.output_folder, exist_ok=True)
            output_file_path = os.path.join(
                self.output_folder, f"{os.path.splitext(os.path.basename(file_path))[0]}_parsed_text.json")
            with open(output_file_path, "w") as json_file:
                json.dump(output_data, json_file, indent=4)
            print(f"File saved successfully at {output_file_path}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def parse_text_with_pypdf2(self, file_path):
        try:
            os.makedirs(self.output_folder, exist_ok=True)
            document = PdfReader(file_path)
            text = ""
            for page in document.pages:
                text += page.extract_text()
            output_data = {"text": text}
            output_file_path = os.path.join(
                self.output_folder, f"{os.path.splitext(os.path.basename(file_path))[0]}_parsed_text.json")
            with open(output_file_path, "w", encoding='utf-8') as output_file:
                json.dump(output_data, output_file, indent=4)
            print(f"File saved successfully at {output_file_path}")
        except Exception as e:
            print(f"Error processing file with PyPDF2: {str(e)}")


class TableExtractor:
    def __init__(self, config):
        self.config = config
        self.output_folder = config.get('output_folder', 'output_tables')
        load_dotenv()

    def get_table_parsing_module(self):
        if self.config['table_parsing'] == 'camelot':
            return self.parse_tables_with_camelot
        elif self.config['table_parsing'] == 'llm':
            return self.parse_tables_with_llm

    def parse_tables_with_camelot(self, file_path):
        os.makedirs(self.output_folder, exist_ok=True)
        tables = camelot.read_pdf(
            file_path, pages='all', flavor="lattice", suppress_stdout=True)
        csv_dir = os.path.join(self.output_folder, 'csv_files')
        os.makedirs(csv_dir, exist_ok=True)
        for i, table in enumerate(tables):
            output_path = os.path.join(csv_dir, f'table_{i}.csv')
            table.to_csv(output_path)
        tables_dict = self.export_csv_tables_to_dict(csv_dir)
        json_output_path = os.path.join(
            self.output_folder, f"{os.path.splitext(os.path.basename(file_path))[0]}_parsed_tables.json")
        self.save_dict_to_json(tables_dict, json_output_path)
        print(f"Tables saved as JSON in {json_output_path}")
        return json_output_path

    def csv_to_dict(self, file_path):
        table_dict = {}
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for column, value in row.items():
                    if column not in table_dict:
                        table_dict[column] = []
                    table_dict[column].append(value)
        return table_dict

    def export_csv_tables_to_dict(self, directory):
        tables_dict = {}
        table_number = 1
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                tables_dict[table_number] = self.csv_to_dict(file_path)
                table_number += 1
        return tables_dict

    def save_dict_to_json(self, data, file_path):
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def parse_tables_with_llm(self, file_path):
        os.makedirs(self.output_folder, exist_ok=True)
        api_key = os.getenv("LLAMA_CLOUD_API_KEY")
        if not api_key:
            raise ValueError(
                "LLAMA_CLOUD_API_KEY environment variable is not set")
        document = LlamaParse(result_type="markdown").load_data(file_path)
        tables_dict = {}
        for i, doc in enumerate(document):
            tables_dict[i + 1] = {"content": doc.text[:100000]}
        json_output_path = os.path.join(
            self.output_folder, f"{os.path.splitext(os.path.basename(file_path))[0]}_parsed_tables.json")
        self.save_dict_to_json(tables_dict, json_output_path)
        print(f"Tables have been saved to {json_output_path}")
        return json_output_path


class QAPairBuilder:
    def __init__(self, config):
        self.config = config
        self.output_folder = config.get('output_folder', 'output')
        self.model_name = "mrm8488/t5-base-finetuned-question-generation-ap"
        self.load_model()

    def load_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

    def generate_question(self, answer, context, max_length=64):
        input_text = f"answer: {answer} context: {context}"
        features = self.tokenizer([input_text], return_tensors='pt')
        output = self.model.generate(input_ids=features['input_ids'], 
                                     attention_mask=features['attention_mask'],
                                     max_length=max_length)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    def build_qa_pairs(self, pdf_name):
        qa_pairs = []

        # Process parsed text
        text_file = f"{pdf_name}_parsed_text.json"
        parsed_text = self.load_json_file(text_file)
        qa_pairs.extend(self.process_parsed_text(parsed_text))

        # Process parsed tables
        table_file = f"{pdf_name}_parsed_tables.json"
        parsed_tables = self.load_json_file(table_file)
        qa_pairs.extend(self.process_parsed_tables(parsed_tables))

        return qa_pairs

    def load_json_file(self, file_name):
        file_path = os.path.join(self.output_folder, file_name)
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {file_path}")
            return {}

    def process_parsed_text(self, parsed_text):
        qa_pairs = []
        for key, value in parsed_text.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    heading = f"{key} - {sub_key}"
                    context = sub_value.get('content', '')
                    question = self.generate_question(context, heading)
                    qa_pairs.append((question, context))
            else:
                question = self.generate_question(value, key)
                qa_pairs.append((question, value))
        return qa_pairs

    def process_parsed_tables(self, parsed_tables):
        qa_pairs = []
        for table_num, table in parsed_tables.items():
            for column, values in table.items():
                context = f"Table {table_num}, Column {column}"
                question = self.generate_question(str(values), context)
                qa_pairs.append((question, str(values)))
        return qa_pairs

    def save_qa_pairs_to_csv(self, qa_pairs, pdf_name):
        output_file = os.path.join(self.output_folder, f'{pdf_name}_qa_pairs.csv')
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Question', 'Answer'])
            writer.writerows(qa_pairs)
        print(f"QA pairs saved to {output_file}")
        return output_file




class DTDLBotPipeline:
    def __init__(self, config):
        self.config = config
        self.text_extractor = TextExtractor(config)
        self.table_extractor = TableExtractor(config)
        self.qa_pair_builder = QAPairBuilder(config)
        # self.model_fine_tuner = ModelFineTuner(config)

    def run(self):
        try:
            pdf_path = self.config.get('pdf_path')
            if os.path.isfile(pdf_path):
                self.process_single_pdf(pdf_path)
            elif os.path.isdir(pdf_path):
                self.process_pdf_folder(pdf_path)
            else:
                raise ValueError(
                    f"Invalid path: {pdf_path}. It should be a file or a directory.")

            print(f"Pipeline run successfully with config: {self.config}")
        except Exception as e:
            print(f"Error running pipeline: {str(e)}")

    def process_single_pdf(self, pdf_path):
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # Parse text and tables
        self.text_extractor.get_text_parsing_module()(pdf_path)
        self.table_extractor.get_table_parsing_module()(pdf_path)

        # Build QA pairs
        qa_pairs = self.qa_pair_builder.build_qa_pairs(pdf_name)
        output_file = self.qa_pair_builder.save_qa_pairs_to_csv(
            qa_pairs, pdf_name)

        print(f"Processed single PDF: {pdf_name}")

    def process_pdf_folder(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(folder_path, filename)
                self.process_single_pdf(pdf_path)

        print(f"Processed all PDFs in folder: {folder_path}")


config = {
    'pdf_path': '/Users/kushagrawadhwa/Desktop/PDF parser/source_docs/handbook.pdf',
    'text_parsing': 'pypdfparser',  # or 'pypdfparser'
    'table_parsing': 'llm',  # or 'llama'
    'output_folder': 'OUTPUT',
    'model_name': 't5-base'  # or 'bert-base-uncased' or 'gpt2' for GPT-4o
}

pipeline = DTDLBotPipeline(config)
pipeline.run()
