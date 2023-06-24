# from sentence_transformers import SentenceTransformer
import re
from os.path import exists
from nltk.tokenize import sent_tokenize 
import nltk
from nltk.tokenize import word_tokenize
# import requests
import json
from datetime import datetime
from elasticsearch import Elasticsearch
import time
from sentence_transformers import SentenceTransformer
import os
import json
import matplotlib.pyplot as plt

def getAllDocuments():
    #Stream the document:
    all_documents = []
    json_files = []
    for file in os.scandir(".\\data\\jsons\\."):
        print(file.path)
        if (file.path.endswith("json")):
            json_files.append(file.path)
    
    for the_json in json_files:
        with open(the_json,'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
            doc = {}
            if 'title' in data:
                doc['title']=data['title']
            else:
                raise Exception(f"The file {the_json} doesn't contain the required field 'title', skipping.")
            if 'id' in data:
                doc['id']=data['id']
            else:
                raise Exception(f"The file {the_json} doesn't contain the required field 'id', skipping.")
            if 'metadata' in data:
                    doc['description']=data['metadata']
            if 'url' in data:
                doc['url']=data['url']
            if 'content_split' in data:
                if len(data['content_split']) >0:
                    doc['content_split']=data['content_split']
            if 'content' in data:
                doc['content']=data['content']
            else:
                raise Exception(f"The file {the_json} doesn't contain the required field 'content', skipping.")
            all_documents.append(doc)
    return all_documents




def plot_histogram(numbers, w):
    # Group numbers into ranges in multiples of 10
    ranges = [i for i in range(min(numbers)//w*w, max(numbers)//w*w+(w+1), w)]
    counts = [0] * len(ranges)

    # Count the numbers in each range
    for num in numbers:
        for i, r in enumerate(ranges):
            if num <= r + (w-1):
                counts[i] += 1
                break

    # Plot the histogram
    plt.bar(ranges, counts, width=(w-1), align='edge')
    plt.xlabel('Range')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    plt.show()

def filter_sentences(sentences):
    # Create a new list to store filtered sentences
    filtered_sentences = []

    # Iterate through each sentence in the input array
    for sentence in sentences:
        # Split the sentence into words
        words = word_tokenize(sentence)

        # Check if the sentence has 3 or more words
        if len(words) >= 3:
            # If yes, append it to the filtered_sentences list
            filtered_sentences.append(sentence)

    return filtered_sentences


def main():
    tesseract     = os.getenv("TESSERACT_LOCATION")
    elastic_host  = os.getenv("ELASTIC_HOST")
    elastic_port  = os.getenv("ELASTIC_PORT")
    elastic_ssl   = os.getenv("ELASTIC_SSL_ASSERT")
    elastic_user  = os.getenv("ELASTIC_USER")
    elastic_pwd   = os.getenv("ELASTIC_PASSWORD")
    elastic_index = os.getenv("ELASTIC_INDEX")

    model = SentenceTransformer('gtr-t5-base')
    nltk.download('punkt')

    documents = getAllDocuments()
    # print (documents[0])
    
    total = len(documents)
    start = time.time()

    token_count_array = []

    for current_doc,doc in enumerate(documents):
        sentences = []
        if 'content-split' in doc:
            sentences = doc['content-split']
        else:
            content = doc['content']
            sentences = sent_tokenize(content)
            # sentences = [content]

        for sentence in sentences:
            words = word_tokenize(sentence)
            if len(words) > 20:
                continue
            token_count_array.append(len(words))
    
    print("Indexed ",current_doc,"/",total," documents")
    end = time.time()

    print("JSON Elapsed ",str(end - start))
    print(f"Token array size = {len(token_count_array)}")
    plot_histogram(token_count_array,2)
        # break
        # embeddings = model.encode(sentences)
        # print(embeddings)

if __name__ == "__main__":
    main()