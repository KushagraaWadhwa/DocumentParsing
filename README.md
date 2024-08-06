# DocumentParsing-DTDL
Objective:- Building an efficient code to completely parse the internal policy documents of the organisation, basically converting the unstructured source document to a structured format, extracting proper information, texts, images, proper structured tables.

Acceptance Criteria:- The Acceptance criteria of the assigned task was having a document coverage greater than 90 percent.

Constraints:- Extracting the exact order of the document, Maintaining the structure of the tables, Achieving a high document coverage rate

Research about Libraries,Packages and Frameworks used
## Python Libraries for PDF Manipulation and Parsing

### 1. PyPDF2
- **Text Extraction:** Extracts text and other data from PDF files.

**Pros:**
- **Pure Python:** No external dependencies, making it easy to install and use.
- **Versatile:** Supports a wide range of PDF manipulations.

**Cons:**
- **Performance:** May not be as fast as some other libraries that use C extensions.
- **Complexity:** Advanced operations can be complex to implement.

**Documentation:** [PyPDF2 Documentation](https://pypdf2.readthedocs.io/en/3.x/)

### 2. py_pdf_parser

**Features:**.
- **Custom Logic:** Allows for custom logic to locate and extract data.
- **Visualization Tool:** Comes with a visualization tool to examine PDF elements.

**Pros:**
- **Structured Data Extraction:** Ideal for extracting structured data from complex PDFs.
- **Flexibility:** Highly customizable for specific extraction needs.

**Cons:**
- **Not Plug-and-Play:** Requires writing custom code for extraction tasks.
- **Limited Text Extraction:** Not designed for simple text extraction tasks.

**Documentation:** [py_pdf_parser Documentation](https://py-pdf-parser.readthedocs.io/en/latest/overview.html)[5]

### 3. LlamaParse

**Features:**
- **GenAI-Native:** Built for generative AI use cases.
- **Table and Image Extraction:** State-of-the-art table and image extraction.
- **Multi-Format Support:** Supports various file types like PDFs, PPTX, DOCX, HTML, and XML.
- **Natural Language Instructions:** Can parse documents based on natural language instructions.

**Pros:**
- **High-Quality Parsing:** Ensures data quality before passing to downstream LLM use cases.
- **Versatile:** Supports multiple file formats and foreign languages.

**Cons:**
- **Pricing:** Free tier is limited, and additional pages require payment.
- **Beta Stage:** Some features may still be in development or under testing.

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
- **Complexity:** Can be complex for beginners due to its extensive feature set.
- **Licensing:** Dual licensing model (AGPL and commercial).

**Documentation:** [PyMuPDF Documentation](https://pymupdf.readthedocs.io/en/latest/intro.html)[11]

### 5. Camelot

**Features:**
- **Table Extraction:** Specializes in extracting tables from text-based PDFs.
- **Export Options:** Can export tables to CSV, JSON, Excel, HTML, Markdown, and SQLite.
- **Metrics:** Provides metrics like accuracy and whitespace to evaluate extraction quality.

**Pros:**
- **Ease of Use:** Simple API for extracting tables.
- **Integration:** Tables are extracted into pandas DataFrames, making it easy to integrate with data analysis workflows.

**Cons:**
- **Text-Based PDFs Only:** Does not work with scanned documents.
- **Limited Scope:** Focused primarily on table extraction.

**Documentation:** [Camelot Documentation](https://camelot-py.readthedocs.io/en/master/)[2]

These libraries offer a range of functionalities for working with PDFs in Python, each with its own strengths and limitations. Depending on your specific needs, you can choose the library that best fits your use case.

Citations:
[1] https://pypdf2.readthedocs.io/en/3.x/
[2] https://camelot-py.readthedocs.io/en/master/
[3] https://nanonets.com/blog/pypdf2-library-working-with-pdf-files-in-python/
[4] https://www.reddit.com/r/learnpython/comments/117cekd/pypdf_vs_pypdf2_vs_pypdf3_vs_pypdf4_vs_others/
[5] https://py-pdf-parser.readthedocs.io/en/latest/overview.html
[6] https://pypi.org/project/py-pdf-parser/
[7] https://www.datacamp.com/tutorial/run-llama-3-locally
[8] https://docs.llamaindex.ai/en/stable/llama_cloud/llama_parse/
[9] https://docs.cloud.llamaindex.ai/llamaparse/getting_started
[10] https://pymupdf.readthedocs.io/en/latest/tutorial.html
[11] https://pymupdf.readthedocs.io/en/latest/intro.html
[12] https://camelot-py.readthedocs.io/_/downloads/en/stable/pdf/
[13] https://pypi.org/project/camelot-py/0.2.2/
[14] https://pypi.org/project/PyPDF2/1.25/
[15] https://pymupdf.readthedocs.io/en/latest/
