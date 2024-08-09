import camelot
import pandas as pd
import json
import tabula

class TableExtractor:
    def __init__(self):
        pass

    def table_to_markdown(self, df):
        return df.to_markdown(index=False)

    def table_to_csv(self, df, csv_path):
        df.to_csv(csv_path, mode='a', index=False)

    def table_to_json(self, df):
        return df.to_json(orient='records', indent=4)

    def parse_pdf_table_camelot(self, pdf_path, output_prefix):
        tables = camelot.read_pdf(pdf_path, pages='all')
        all_markdown = ""
        
        for i, table in enumerate(tables):
            df = table.df
            markdown_output = self.table_to_markdown(df)
            csv_output_path = f"{output_prefix}_camelot_table_{i+1}.csv"
            json_output = self.table_to_json(df)
            
            # Append Markdown output to the combined string
            all_markdown += f"### Table {i+1}\n\n"
            all_markdown += markdown_output + "\n\n"
            
            # Save individual outputs
            self.table_to_csv(df, csv_output_path)
            
            with open(f"{output_prefix}_camelot_table_{i+1}.json", 'w') as json_file:
                json_file.write(json_output)
            
            print(f"Camelot Table {i+1} processed and saved.")
        
        # Save the combined Markdown output to a single file
        with open(f"{output_prefix}_camelot_all_tables.md", 'w') as md_file:
            md_file.write(all_markdown)

# Example usage:
# extractor = TableExtractor()
# pdf_path = "/Users/kushagrawadhwa/Desktop/PDF parser/source_docs/policy2.pdf"
# output_prefix = "output"
# extractor.parse_pdf_table_camelot(pdf_path, output_prefix)

