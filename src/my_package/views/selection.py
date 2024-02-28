import json
import random
import string
from flask import Blueprint, redirect, request
from src.ml_modules import main
from Config.config import dataset_save_path, experiment_save_path
import os, torch
import threading

selection_views = Blueprint('selection_views',__name__)


def experiment_save(result_data_json: json, 
                    model: torch.nn.Module,
                    experiment_save_dir):
    random_model_name = ''.join(random.choices(string.ascii_letters + string.digits, k=6)) + ".pth"
    result_save_path = os.path.join(experiment_save_dir,"result.json")
    with open (result_save_path, "w") as f:
        f.write(result_data_json)

    assert random_model_name.endswith(".pth") or random_model_name.endswith(".pt"), "model_name should end with '.pt' or '.pth'"
    model_save_path = os.path.join(experiment_save_dir,random_model_name)

    torch.save(obj=model,
             f=model_save_path)
    
def sending_model_to_train(training_folder, epochs, pretrained_model_name, learning_rate, experiment_save_dir, random_dir_name, model_name):
    results, model, class_names =  main.main(training_folder=training_folder,
              epochs=epochs,
              pretrained_model_name=pretrained_model_name,
              learning_rate=learning_rate
            )
  
    
    results["class_names"] = class_names
    results["model_used"] = pretrained_model_name
    results["status"] = "completed"
    results["dir_name"] = random_dir_name
    results["model_name"] = model_name
    
    result_data_json = json.dumps(results)
    experiment_save(result_data_json, model, experiment_save_dir)
    return


@selection_views.route("/selection/<folder_name>", methods=["POST"])
def selection(folder_name: str):
    epochs = request.form["epochs"]
    model_name = request.form["model_name"]
    learning_rate = float(request.form["learning_rate"])
    pretrained_model_name = request.form["model"]
    folder_name = folder_name
    training_folder = os.path.join(dataset_save_path, folder_name, "train")


    random_dir_name = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    experiment_save_dir = os.path.join(experiment_save_path,random_dir_name)
    os.makedirs(experiment_save_dir, exist_ok=True)
    result_save_path = os.path.join(experiment_save_dir,"result.json")

    thread2 = threading.Thread(target=sending_model_to_train, args= [training_folder, epochs, pretrained_model_name, learning_rate, experiment_save_dir, random_dir_name, model_name])

    thread2.start()


    result = {"status":"incomplete", "pretrained_model_name":pretrained_model_name, "model_name":model_name}
    with open (result_save_path, "w") as f:
        f.write(json.dumps(result))

    return redirect("/list_models")