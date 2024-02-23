import zipfile
from flask import Blueprint, render_template, request, send_file
import torch
from Config.config import experiment_save_path, temporary_save_path
import os, json
from PIL import Image
from io import BytesIO
from torchvision import transforms

model_interaction_views = Blueprint("model_interaction_views", __name__)

@model_interaction_views.route("/model_use_type", methods=["GET"])
def model_use_type():
    return render_template("model_use_type.html")


@model_interaction_views.route("/list_models", methods=["GET"])
def list_models():
    model_details_json = {}
    count_trained = 1
    
    for root,_,files in os.walk(experiment_save_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                model_details_json["model" + str(count_trained)] = {"folder":os.path.basename(root),"result":data}
                count_trained+=1

    return render_template("model_selection.html", model_details_json=model_details_json)


@model_interaction_views.route("/model_selected/<folder>", methods=["POST","GET"])
def model_selected(folder: str):
    return render_template("prediction.html", folder=folder)


@model_interaction_views.route("/predict/<folder>", methods=["POST","GET"])
def predict(folder: str):
    
    folder_path = os.path.join(experiment_save_path, folder)
    for file in os.listdir(folder_path):
        if file.endswith(".pth") or file.endswith(".pt"):
            model_path = os.path.join(folder_path,file)
            model = torch.load(f= model_path)

        if file.endswith(".json"):
            json_file = os.path.join(folder_path,file)
            with open(json_file, "r") as f:
                data = json.load(f)
            class_names = data["class_names"]

    device = "cuda" if torch.cuda.is_available() else "cpu"
    image =request.files["image"]
    img = Image.open(image)
    trans = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor()
    ])
    img = trans(img)
    pred = model(img.unsqueeze(dim=0).to(device)).argmax(dim=1)
    pred_class = class_names[pred]

    return render_template("prediction.html",prediction=pred_class, folder=folder)


def zip_folder_for_download(folder_path: str,
                            readme_file: str):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))
        
        zipf.write(readme_file, os.path.basename(readme_file))

    zip_buffer.seek(0)
    return zip_buffer


@model_interaction_views.route("/to_download_model", methods=["GET"])
def download_model():
    readme_file = os.path.join(temporary_save_path,"readme.txt")
    zip_buffer = zip_folder_for_download(experiment_save_path, readme_file)
    return send_file(zip_buffer, as_attachment=True, download_name='Trained_models.zip')