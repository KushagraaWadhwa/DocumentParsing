# DocumentParsing-DTDL

**Objective/Primary Focus:-** Implementation of Doc Parser in Python using pre-trained NLP models/ libraries. Building an efficient code to completely parse the internal policy documents of the organisation, basically converting the unstructured source document to a structured format, extracting proper information, texts, images, proper structured tables.

**Purpose:-** Fine-tuning dataset and Department level Benchmark dataset preparation.

**Acceptance Criteria:-** The Acceptance criteria of the assigned task was having a document coverage greater than 90 percent.

It consists of two evaluation metrics:-

**~Difflib Similarity**( Check for word overlap, longest occurring continuous sequence of words)-Python inbuilt library.

[Difflib Documentation](https://docs.python.org/3/library/difflib.html)

**~Sentence BERT Similarity**(Checks for the overall semantic interpretation of dataset)-Hugging Face PreTrained model(''all-MiniLM-L6-v2') [Sentence-BertDocumentation](https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html)
 
*--> The first sheet contains the coverage comparison between Raw Truth and Ground Truth of the various HR documents*
 
The metrics have been computed between:-

- (i)Raw Truth and Ground Truth(Complete Corpus)
- (ii)Raw Truth and Ground Truth(Unique Corpus)
- (iii) Raw Truth v/s Raw Truth (Interlibrary coverage comparison)
 
*--> The second sheet of this excel document contains the similarity metrics for the combined QA pairs set between Native QA and T-5 model based QA*

**Constraints:-** Extracting the exact order of the document, Maintaining the structure of the tables, Achieving a high document coverage rate

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Research about Libraries,Packages and Frameworks used

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Python Libraries specifically for PDF text Parsing
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
- **Not Plug-and-Play:** Requires writing custom code for extraction tasks.Some manual inputs are required regarding adding fonts
- Implementation of extraction of table data is very complex

*Excellent library to seggregate document, identify sections from the document such as <heading><subheading><content>. Faces issues if all the documents are not in a generalised format!

**Documentation:** [py_pdf_parser Documentation](https://py-pdf-parser.readthedocs.io/en/latest/overview.html/)

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

**Documentation:** [LlamaParse Documentation](https://docs.cloud.llamaindex.ai/llamaparse/getting_started/)

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

**Documentation:** [PyMuPDF Documentation](https://pymupdf.readthedocs.io/en/latest/intro.html/)
  
## Python Libraries specifically for Parsing,extracting and analysing the tables present in the PDF documents
### 5. Camelot

**Features:**
- **Table Extraction:** Specializes in extracting tables from text-based PDFs.
- **Export Options:** Can export tables to CSV, JSON and Markdown.

**Pros:**
- **Integration:** Tables are extracted into pandas DataFrames, making it easy to integrate with data analysis workflows.

**Cons:**
- **Text-Based PDFs Only:** Does not work with scanned documents.
- **Limited Scope:** Focused primarily on table extraction.

*The best library observed throughout the experimentation to analyse, parse, extract table data!

**Documentation:** [Camelot Documentation](https://camelot-py.readthedocs.io/en/master/)

### 6. Tabula

**Features:**
- **Table Extraction:** Specializes in extracting tables from text-based PDFs.

*Tables were not found to be extracted in a good format hence discarded as an option!

**Documentation:** [Tabula Documentation](https://tabula-py.readthedocs.io/en/latest/tabula.html/)

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Dataset

My current experimentation included three major policy documents of the organisation namely:-

- Internal Mobility Guidelines ( policy1.pdf ): 2pages, 84kb 
- Employee Performance Improvement Policy ( policy2.pdf ): 4pages, 273kb 
- Employee Handbook ( handbook.pdf ): 75pages,981kb 


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="543" alt="Screenshot 2024-08-07 at 10 35 07 AM" src="https://github.com/user-attachments/assets/122e6f3d-a661-4f7b-934f-fcab97ab39be"> 
<img width="541" alt="Screenshot 2024-08-07 at 10 35 30 AM" src="https://github.com/user-attachments/assets/0f4b8035-0186-4456-aa57-bd9a247d5e23">
<img width="540" alt="Screenshot 2024-08-07 at 10 34 50 AM" src="https://github.com/user-attachments/assets/1f66a6a8-4a84-4d05-8d3b-abcd9d04cab4">


**The above images are an output to a streamlit dashboard I built to analyse the pdf documents.*

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Workflow followed

```mermaid
graph TD;
    A[Actor: Source Documents] -->|Various Libraries (Raw Text obtained)| B[Q/A Pair Generation];
    A -->|Ground Truth Text| B;
    B --> C[Native QA];
    B --> D[T5 QA];
    B --> E[GPT-4];
    
    subgraph Libraries Used
        B1[pypdf2]
        B2[py_pdf_parser]
        B3[PyMuPDF]
        B4[LLamaparser]
    end
    
    B1 --> B
    B2 --> B
    B3 --> B
    B4 --> B
```

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Summary

The project aimed to implement a document parser in Python using pre-trained NLP models and libraries to convert unstructured internal policy documents into a structured format, extracting text, images, and tables while maintaining their original order. The chosen parser, integrating PyMuPDF and Camelot, was selected for its ability to provide image metadata, extract images, and efficiently read text and tables in the exact order they appear in the documents.Amongst the text parsing libraries PyMUPDF is the fastest and best amongst its competitors, LlamaParser has quite a lot exploraton but is not allowed to be used for company's internal documents, the best lbrary for parsing turned out to be Camelot; which can provide tables in three formats:- Markdown, CSV, JSON. The research phase evaluated various libraries, ultimately discarding some due to poor performance and not being able to help us achieve the results. The final solution was tested on three major policy documents, achieving the required document coverage rate of over 90%. A Streamlit dashboard was also developed to visualize the pdf documents about the corpus count, pages count, images count, tables count etc.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Limitations

- Multillingual Parsing Capability of the parser
- Duplication of the table content(May or may not affect the further usage of the documentation)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Next Steps

- Integrating OCR to read the image content along with the display of image metadata
- Adding Multillingual Capability to the parser
- Remove the duplicate parsing of tables
- Tables in json format





