import os
import tempfile
import json

txt_files=[]
json_files=[]


for file in os.scandir(".\\data\\documents\\."):
    #print(file.path)
    if (file.path.endswith("documento2.txt")):
        txt_files.append(file)
       

for file in os.scandir(".\\data\\jsons\\."):
    #print(file.path)
    if (file.path.endswith("json")):
        json_files.append(file)
       


for txt in txt_files:
    print("Processing txt =  "+txt.path)
    with open(txt.path, 'r', encoding="utf8") as f:
        lines = f.readlines()
        
    test =" \ "
    test2= test.strip()+"n"
    lines = [line.replace('\n', test2) for line in lines]
    
    
    print("Creado txt nuevo docuemnto"+txt.path)
    print("---------------------------------------------------------------------")
    with open(txt.path, 'w', encoding="utf8") as f:
        f.writelines(lines)


    
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




  

    
    
    
    