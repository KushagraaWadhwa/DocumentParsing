import difflib
import docx
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def read_text_from_file(file_path):
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file format. Only .txt and .docx files are supported.")

def preprocess_text(text):
    # Remove specific substrings
    text = text.replace("\n", "").replace(" Deutsche Telekom Digital Labs Pvt. Ltd Version Control: 1.0, Released on 1-Feb-21 Document Author: People Team For Internal Circulation Only ", "")
    text = text.replace(" Deutsche Telekom Digital Labs Pvt. Ltd Version Control: 1.1, Released on 1-May-23, Document Author: Hina Chhikara For Internal Circulation Only ", "")
    text = text.replace(" Deutsche Telekom Digital Labs Private Limited Version Control: V.6.0, Released on 01-April-2024, Document Author: Nihar Mathur For Internal Circulation Only ", "")
    text = text.replace("|", "").replace(" ", "").replace("#", "")
    return text

def compute_text_overlap_score_and_differences(file_path1, file_path2):
    text1 = preprocess_text(read_text_from_file(file_path1))
    text2 = preprocess_text(read_text_from_file(file_path2))
    matcher = difflib.SequenceMatcher(None, text1, text2)
    score = matcher.ratio()

    differ = difflib.Differ()
    diff = list(differ.compare(text1.split(), text2.split()))

    return score, diff

# Iterate over directories and files
directories = ["ground_truth","pymupdf"]
files = ['policy1', 'policy2', 'handbook']

for dir1 in directories:
    for file in files:
        file_path2 = f'/Users/kushagrawadhwa/Desktop/PDF parser/{dir1}/{file}_parsed.txt'
        print(f"Processing {file} in {dir1}")

        for dir2 in directories:
            file_path1 = f'/Users/kushagrawadhwa/Desktop/PDF parser/{dir2}/{file}_parsed.txt'
            print(f"Comparing {file_path1} with {file_path2}")

            score, differences = compute_text_overlap_score_and_differences(file_path1, file_path2)
            print(f"Text Overlap Score: {score:.2f}")

            # Optionally print differences (first 100 lines)
            # for line in differences[:100]:
            #     print(line)
        print("\n")