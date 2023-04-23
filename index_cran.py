# from sentence_transformers import SentenceTransformer
import re
from os.path import exists
from nltk.tokenize import sent_tokenize 
import nltk
# import requests
import json
from datetime import datetime
from elasticsearch import Elasticsearch
import time
from sentence_transformers import SentenceTransformer
import os

lines_regexp = {
    'doc_id': re.compile(r'\.I (?P<id>[0-9]+).*\n'),
    'title': re.compile(r'\.T.*\n'),
    'author': re.compile(r'\.A.*\n'),
    'biblio': re.compile(r'\.B.*\n'),
    'text': re.compile(r'\.W.*\n'),
}

def parse_one_line(line):
    for key, pattern in lines_regexp.items():
        found = pattern.search(line)
        if found:
            break
    if found:
        return key, found
    return None, None

def getAllDocuments():
    #Stream the document:
    all_documents = []
    doc = {}
    is_title = False
    is_author = False
    is_biblio = False
    is_text = False
    title = ""
    biblio = ""
    author = ""
    text = ""
    doc_num = 0
    thefile = "data/cran/cran.all.1400"
    if not exists(thefile):
        print ("ERROR: file '{}' does not exists.".format(thefile))
        return 
    with open(thefile,'r') as document_reader:
        for line in document_reader.readlines():
            # print("Processing line '{}'".format(line))
            key,data = parse_one_line(line)

            if key == None: #No regex matched, we are parsing one of the fields...
                if is_title:
                    title += line.replace('\n',' ')
                elif is_author:
                    author += line.replace('\n',' ')
                elif is_biblio:
                    biblio += line.replace('\n',' ')
                elif is_text:
                    text += line.replace('\n',' ')
                continue
            else: # We got a match, let's reset the statuses
                if is_title:
                    doc['title'] = title
                elif is_author:
                    doc['author'] = author
                elif is_biblio:
                    doc['bibliography'] = biblio
                elif is_text:
                    doc['content'] = text
                is_title = False
                is_author = False
                is_biblio = False
                is_text = False
                title = ""
                biblio = ""
                author = ""
                text = ""                    

            if key == 'doc_id':
                doc_id = data.group('id')
                #starting a new document:
                if doc == {}:
                    doc['id']=doc_id
                else: # There was a document already, we save it to the array first
                    all_documents.append(doc.copy())
                    # print("Processed document: {}, # {}.".format(doc,doc_num))
                    # print("Processed document: {}.".format(doc_num))
                    doc_num += 1
                    doc = {}
                    doc['id']=doc_id
                continue

            if key == 'title':
                #Title is in the next line:
                is_title = True
                continue

            if key == 'author':
                is_author = True
                continue

            if key == 'biblio':
                is_biblio = True
                continue

            if key == 'text':
                is_text = True
                continue

    return all_documents



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
    for current_doc,doc in enumerate(documents):
        try:
            es = Elasticsearch(hosts=[elastic_host+":"+elastic_port],
                                ssl_assert_fingerprint=elastic_ssl,
                                basic_auth=(elastic_user,elastic_pwd))
                               

            index_name = elastic_index

            content = doc['content']

            # sentences = sent_tokenize(content)
            sentences = [content]

            # TODO: Get the sentence vector from the model
            
            result_list = model.encode(sentences)
            vectors=[]
            for result in result_list:
                # print(len(result.get("vector")))
                vectors.append(result)

            #Parent document:
            doc_id = doc['id']
            parent = {
                "title": doc['title'],
                "my_id": doc_id,
                "content": doc["content"],
                "articles_sentence":"articles"
            }

            #Index the parent document:

            try:
                r = es.index(
                    id = doc_id,
                    index = index_name,
                    body = parent
                )
                # print("response: ",r )
            except Exception as err:
                print("error:", err)
                exit()

            #Index the child documents:
            for i, sentence in enumerate(sentences):
                child_id = str(doc['id'] + "_" + str(i))
                child = {
                    "title": doc['title'],
                    "my_id": child_id,
                    "sentence-vector": vectors[i],
                    "articles_sentence":{
                        "name": "sentence",
                        "parent": doc['id']
                    },
                    "sentence": sentence
                }
                # print(json.dumps(child,indent=2))
                # And index it:
                try:
                    r = es.index(
                        id = child_id,
                        routing = doc_id,
                        index = index_name,
                        body = child
                    )
                except Exception as err:
                    print("error:", err)
        except Exception as err:
            print("error:", err)
        print("Indexed ",current_doc,"/",total," documents")
    end = time.time()
    print("CRAN Elapsed ",str(end - start))
        # break
        # embeddings = model.encode(sentences)
        # print(embeddings)

if __name__ == "__main__":
    main()




