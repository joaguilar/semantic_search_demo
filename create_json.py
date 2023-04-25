import os
import tempfile
import json

txt_files=[]



for file in os.scandir(".\\data\\documents\\."):
    print(file.path)
    if (file.path.endswith("txt")):
        print(file.path)
        print("---------------------------------------------------------------------")
        txt_files.append(file)
        print(txt_files)
        print("---------------------------------------------------------------------")
        print("---------------------------------------------------------------------")


i=0

for txt in txt_files:
    print("Processing txt =  "+txt.path)
    with open(txt.path, 'r', encoding="utf8") as f:
        lines = f.readlines()
        
    test =" \ "
    test2= test.strip()+"n"
    lines = [line.replace('\n', test2) for line in lines]
    
    if(i==3):
        i+=1 
    print("---------------------------------------------------------------------")
    print("Contador en "+str(i))
    print("---------------------------------------------------------------------")

       
    print("Creado txt nuevo docuemnto"+str(i))
    print("---------------------------------------------------------------------")
    with open(".\data\documents\Texto Json\documento"+str(i)+".txt", 'w', encoding="utf8") as f:
        f.writelines(lines)

    
    print("Abriendo JSON documento"+str(i))
    print("---------------------------------------------------------------------")
    with open(".\data\jsons\.\documento"+str(i)+".json",'r', encoding="utf8") as file:
        data = json.load(file)
    
    print("Sobreescribiendo JSON con el txt documento"+str(i))
    print("---------------------------------------------------------------------")
    with open(txt.path, 'r', encoding="utf8") as f:
        data['content']=f.read()
        #print("JSON")
        #print(data)


    
    print("Update Json document"+str(i))
    with open(".\data\jsons\.\documento"+str(i)+".json",'w', encoding="utf8") as jsonUpdate:
            json.dump(data,jsonUpdate,ensure_ascii= False)
    
    
    i+=1
    
    
    