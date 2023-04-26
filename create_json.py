import os
import tempfile
import json

txt_files=[]
json_files=[]


for file in os.scandir(".\\data\\documents\\."):
    #print(file.path)
    if (file.path.endswith("txt")):
        print("---------------------------------------------------------------------")
        txt_files.append(file)
        print("---------------------------------------------------------------------")
        print("---------------------------------------------------------------------")

for file in os.scandir(".\\data\\jsons\\."):
    #print(file.path)
    if (file.path.endswith("json")):
        print("---------------------------------------------------------------------")
        json_files.append(file)
        print("---------------------------------------------------------------------")
        print("---------------------------------------------------------------------")


i=0





  
    
for json_Data in json_files:
    data={}

    print("---------------------------------------------------------------------")
    with open(json_Data.path,'r', encoding="utf8") as file:
        print("Load Json: "+ str(file))
        data = json.load(file)
    
        print("Processing"+ json_Data.path)
        print("---------------------------------------------------------------------")

        test= json_Data.path.replace(".json",".txt").replace("jsons","documents\\")
        print("Ruta del txt: " + test)
        print("Ruta del json: " + json_Data.path)

        with open(test, 'r', encoding="utf8") as f:
            data['content']=f.read()
    
    print("Update Json document"+ json_Data.path)
    with open(json_Data.path,'w', encoding="utf8") as jsonUpdate:
        json.dump(data,jsonUpdate,ensure_ascii= False)
    
    
    
    