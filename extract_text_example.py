import pytesseract
import os
from pdf2image import convert_from_path
from PIL import Image
import tempfile

from nltk.tokenize import sent_tokenize 
import nltk


tesseract_path = os.getenv("TESSERACT_LOCATION")
poppler_path = os.getenv("POPPLER_LOCATION")
pytesseract.pytesseract.tesseract_cmd = tesseract_path
print("Using Poppler:"+poppler_path)
print("Using Tesseract:"+tesseract_path)
#Required to split the text into sentences using nltk:
nltk.download('punkt')
pdf_files=[]

for file in os.scandir(".\\data\\documents\\."):
    print(file.path)
    if (file.path.endswith("pdf")):
        pdf_files.append(file.path)

for pdf_path in pdf_files:
    images = convert_from_path(pdf_path=pdf_path, poppler_path=poppler_path)

    doc_text = ""
    output_file_name=pdf_path.replace("pdf","txt")
    if (os.path.exists(output_file_name)):
        print(f"Skipping {pdf_path}. File {output_file_name} already exists")
        continue
    print(f"Processing {pdf_path}.")
    with tempfile.TemporaryDirectory() as tmpdirname:
        with open(output_file_name, 'w', encoding="utf-8") as f:
            print(tmpdirname)
            for count, img in enumerate(images):
                img_name = f"{tmpdirname}\page_{count}.png"  
                img.save(img_name, "PNG")

            png_files = [f for f in os.listdir(tmpdirname+"\.") if f.endswith(".png")]

            for png_file in png_files:
                extracted_text = pytesseract.image_to_string(Image.open(tmpdirname+"\\"+png_file))
                print(extracted_text)
                f.write(extracted_text)
                
            #Example on how to split the text into sentences using nltk:
            sentences = sent_tokenize(extracted_text)
            for sentence in sentences:
                print(f"Sentence: [{sentence}]")
            

