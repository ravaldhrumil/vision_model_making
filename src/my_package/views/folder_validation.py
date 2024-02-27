import json
from zipfile import ZipFile
from flask import Blueprint, render_template, request, redirect
import os, random, string, shutil
import pandas as pd
from Config.config import temporary_save_path, dataset_save_path

validation_views = Blueprint('validation_views',__name__)

def is_valid_std_format(folder_path):

    img_count = 0
    try:
        no_of_folders = len(os.listdir(folder_path))
        if no_of_folders > 1:
            return {"msg":"There are more than 1 folder in your main folder",
                    "validity":False}
        

        if not os.path.exists(os.path.join(folder_path, 'train')):
            return {"msg":"There is no train folder",
                    "validity":False}
        
        
        train_folders = os.listdir(os.path.join(folder_path, 'train'))
        
        for folder in train_folders:
            path = os.path.join(folder_path, "train" ,folder)

            if not os.path.isdir(path):
                return {"msg":f"There is something other than folder in your train folder", 
                        "validity":False}

            for _, dirs, _ in os.walk(path):
                if len(dirs) > 0:
                    return {"msg":f"There is a folder {dirs[0]} inside your classes folder", 
                            "validity":False}
            
       
            for file in os.listdir(path):
                img_count+=1
                if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    return {"msg":f"Your folder {folder} contains file {file} which is not an image",
                            "validity":False}
            
    except NotADirectoryError:
        return {"msg":"There is no directory in your train folder",
                "validity":False}
    
    if img_count < 10:
        return {"msg":f"Minimum 10 images required",
                "validity":False}
        
    return{"msg":"Uploaded folder is valid",
            "validity":True}


def csv_file_validation(csv_file, folder_path):
    df = df2 = pd.read_csv(csv_file)

    if len(df.columns) == 2:

        for cols in df.columns:
            if df[cols].isna().sum() > 0:
                return {"msg":"There is a null value in your {cols} column in csv file",
                        "validity":False}
        else:
            no_of_rows = len(df.index)

            file_dir = None
            for _,_,files in os.walk(folder_path):
                file_dir = files
                no_of_images = len(files)

            if no_of_rows == no_of_images - 1:
                df2 = df2[~df2.iloc[:, 0].isin(file_dir)]

                if len(df2.index) == 0:
                    return {"msg":"Uploaded Folder is in correct sequence",
                            "validity":True}

                else:
                    return {"msg":"Name of images mismatched in csv file",
                            "validity":False}

            else:
                return {"msg":"No of rows in csv and number of images does not match",
                        "validity":False}

    else:
        return {"msg":"There are more than 2 columns in your csv file",
                "validity":False}
    

def convert_to_std_format(csv_file, folder_path):
    df = pd.read_csv(csv_file)

    class_names = set(df["image_class"])

    for folder_name in class_names:
        os.makedirs(os.path.join(folder_path, "train", folder_name), exist_ok=True)

    for file in os.listdir(folder_path):
        for index,row in df.iterrows():
            if row["image_name"] == file:
                shutil.move(os.path.join(folder_path,file),
                            os.path.join(folder_path, "train" ,row["image_class"]))
                
    for _,_,file in os.walk(folder_path):
        os.remove(os.path.join(folder_path,file[0]))
        break
    

def is_valid_csv_format(folder_path):
    csv_count = 0
    csv_file = None
    img_count = 0

    for root, dirs, files in os.walk(folder_path):
        if dirs:
            return {"msg":"There exist another folder which is not correct",
                    "validity":False}
        for file in files:
            if file.endswith('.csv'):
                csv_count += 1
                csv_file = os.path.join(root, file)
                if csv_count > 1:
                    csv_file = None
                    return {"msg":"There are multiple CSV files in the directory.",
                            "validity":False}
            
                img_count+=1
                if not file.lower().endswith(('.png', '.jpg', '.jpeg', ".csv")):
                    return {"msg":"There is a file which is not an image",
                            "validity":False}

    if img_count < 10:
        return {"msg":f"Minimum 10 images required",
                "validity":False}

    if csv_count == 1:
        csv_check = csv_file_validation(csv_file, folder_path)
        if csv_check["validity"]:
            convert_to_std_format(csv_file, folder_path)
        return csv_check
    
    elif csv_count == 0:
        return {"msg":"There are no CSV files in the directory.",
                "validity":False}
    

def handle_uploaded_folder(folder_path, folder_type):
    if folder_type ==  "std_format":
        response = is_valid_std_format(folder_path)

    elif folder_type == "csv_format":
        response = is_valid_csv_format(folder_path)
    
    return response
        

def extract_file(folder):
    with ZipFile(folder, 'r') as zip_ref:
            zip_ref.extractall(temporary_save_path)

    return


def class_name_process(folder_path):
    class_details = {"no_of_classes":0, "class_names":[], "image_count":{}}
    for each_class_name in os.listdir(folder_path):
        class_details["class_names"].append(each_class_name)

        for _,_,files in os.walk(os.path.join(folder_path,each_class_name)):
            class_details["image_count"][each_class_name] = len(files)

        class_details["no_of_classes"] = len(class_details["class_names"])

    return class_details 


@validation_views.route("/",methods=["GET"])
def home():
    return render_template("index.html")


@validation_views.route("/folder_upload",methods=["POST"])
def folder_upload():
    folder_type = request.form["folder_type"]
    folder = request.files["folder"]

    extract_file(folder)

    for root ,dir, _ in os.walk(os.path.join(temporary_save_path)):
        folder_path = os.path.join(root,dir[0])
        break
   
    response = handle_uploaded_folder(folder_path, folder_type)
    
    if response["validity"] == True:
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        os.rename(folder_path,os.path.join(temporary_save_path,random_name))
    
        try:
            shutil.move(os.path.join(temporary_save_path,random_name), os.path.join(dataset_save_path,random_name))
        except Exception as e:
            print(f"Error moving file: {e}")

        class_details = class_name_process(os.path.join(dataset_save_path,random_name,"train"))
        with open(os.path.join(dataset_save_path,random_name,"data_configuration.json"), "w") as f:
            json.dump(class_details, f)

        return render_template("parameter_selection.html",
                               msg=response["msg"],
                               validity=response["validity"],
                               class_names=class_details["class_names"],
                               num_classes=len(class_details["class_names"]),
                               image_count=class_details["image_count"],
                               folder_name=random_name)
        
    
    elif response["validity"] == False:
        shutil.rmtree(folder_path)
        return render_template("/index.html" , error=response["msg"])