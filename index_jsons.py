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
import json

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
            if 'content_split' in data:
                if len(data['content_split']) >0:
                    doc['content_split']=data['content_split']
            if 'content' in data:
                doc['content']=data['content']
            else:
                raise Exception(f"The file {the_json} doesn't contain the required field 'content', skipping.")
            all_documents.append(doc)
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

            sentences = []
            if 'content-split' in doc:
                sentences = doc['content-split']
            else:
                content = doc['content']
                sentences = sent_tokenize(content)
                # sentences = [content]

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
    print("JSON Elapsed ",str(end - start))
        # break
        # embeddings = model.encode(sentences)
        # print(embeddings)

if __name__ == "__main__":
    main()