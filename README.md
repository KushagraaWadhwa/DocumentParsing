# DocumentParsing-DTDL
Objective:- Building an efficient code to completely parse the internal policy documents of the organisation, basically converting the unstructured source document to a structured format, extracting proper information, texts, images, proper structured tables.

Acceptance Criteria:- The Acceptance criteria of the assigned task was having a document coverage greater than 90 percent.

Constraints:- Extracting the exact order of the document, Maintaining the structure of the tables, Achieving a high document coverage rate

#Research about Libraries,Packages and Frameworks used
## Python Libraries for PDF Manipulation and Parsing

### 1. PyPDF2
- **Text Extraction:** Extracts text and other data from PDF files.

**Pros:**
- **Pure Python:** No external dependencies, making it easy to install and use.
- **Versatile:** Supports a wide range of PDF manipulations.

**Cons:**
- **Performance:** May not be as fast as some other libraries that use C extensions.
- **Complexity:** Advanced operations can be complex to implement.
- No support for table formats

**Documentation:** [PyPDF2 Documentation](https://pypdf2.readthedocs.io/en/3.x/)

### 2. py_pdf_parser

**Features:**.
- **Custom Logic:** Allows for custom logic to locate and extract data.For example:- Can help extract data based on the font style of the content present in the pdf

**Pros:**
- **Structured Data Extraction:** Ideal for extracting structured data from complex PDFs.
- **Flexibility:** Highly customizable for specific extraction needs.

**Cons:**
- **Not Plug-and-Play:** Requires writing custom code for extraction tasks.
- Implementation of extraction of table data is very complex

**Documentation:** [py_pdf_parser Documentation](https://py-pdf-parser.readthedocs.io/en/latest/overview.html)[5]

### 3. LlamaParser

**Features:**
- **GenAI-Native:** Built for generative AI use cases.
- **Table and Image Extraction:** State-of-the-art table and image extraction.
- **Multi-Format Support:** Supports various file types like PDFs, PPTX, DOCX, HTML, and XML.
- **Natural Language Instructions:** Can parse documents based on natural language instructions.

**Pros:**
- **High-Quality Parsing:** Ensures data quality .
- **Versatile:** Supports multiple file formats and foreign languages.

**Cons:**
- **Pricing:** Free tier is limited, and additional pages require payment.
- LLM based, requires 3rd party API calls, not allowed to use for company's internal documents.

**Documentation:** [LlamaParse Documentation](https://docs.cloud.llamaindex.ai/llamaparse/getting_started)[9]

### 4. PyMuPDF

**Features:**
- **High Performance:** Known for top performance and high rendering quality.
- **Multi-Format Support:** Supports PDF, XPS, OpenXPS, CBZ, EPUB, MOBI, and FB2 formats.
- **Data Extraction:** Extracts text, images, and other data from documents.
- **Document Manipulation:** Allows for document analysis, conversion, and manipulation.

**Pros:**
- **Speed:** Fast rendering and processing.
- **Comprehensive:** Supports a wide range of document formats and operations.
- **Cross-Platform:** Works on Windows, Mac, and Linux.

**Cons:**
- **Complexity:** Can be complex due to its extensive feature set.


**Documentation:** [PyMuPDF Documentation](https://pymupdf.readthedocs.io/en/latest/intro.html)[11]

### 5. Camelot

**Features:**
- **Table Extraction:** Specializes in extracting tables from text-based PDFs.
- **Export Options:** Can export tables to CSV, JSON and Markdown.

**Pros:**
- **Integration:** Tables are extracted into pandas DataFrames, making it easy to integrate with data analysis workflows.

**Cons:**
- **Text-Based PDFs Only:** Does not work with scanned documents.
- **Limited Scope:** Focused primarily on table extraction.

**Documentation:** [Camelot Documentation](https://camelot-py.readthedocs.io/en/master/)[2]


#Dataset
My current experimentation included three major policy documents of the organisation namely:-

-Internal Mobility Guidelines ( policy1.pdf ): 2pages, 84kb 
<img width="543" alt="Screenshot 2024-08-07 at 10 35 07 AM" src="https://github.com/user-attachments/assets/122e6f3d-a661-4f7b-934f-fcab97ab39be"> 

-Employee Performance Improvement Policy ( policy2.pdf ): 4pages, 273kb 
<img width="541" alt="Screenshot 2024-08-07 at 10 35 30 AM" src="https://github.com/user-attachments/assets/0f4b8035-0186-4456-aa57-bd9a247d5e23">

-Employee Handbook ( handbook.pdf ): 75pages,981kb 
<img width="540" alt="Screenshot 2024-08-07 at 10 34 50 AM" src="https://github.com/user-attachments/assets/1f66a6a8-4a84-4d05-8d3b-abcd9d04cab4">

**The above images are an output to a streamlit dashboard I built to analyse the pdf documents.

#Workflow followed





