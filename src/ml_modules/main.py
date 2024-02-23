import torch
from src.ml_modules import data_loder, train, pre_trained_model
from torch import nn


def main(training_folder:str,
         epochs: int,
         pretrained_model_name: str,
         learning_rate: float):
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    train_dir = training_folder

    auto_transfoms, in_features, model =  pre_trained_model.initialisation(pretrained_model_name=pretrained_model_name,
                                                                           device=device)


    train_dataloader, validation_loader, class_names = data_loder.data_loader(train_dir=train_dir,
                                                                                auto_transfoms=auto_transfoms)
    
    out_features = len(class_names)

    model, loss_fn, optimizer = pre_trained_model.classifier(in_features=in_features,
                                 out_features=out_features,
                                 device=device,
                                 learning_rate=learning_rate,
                                 model=model,
                                 pretrained_model_name=pretrained_model_name)
    
    model.fc = nn.Sequential(
        torch.nn.Dropout(p=0.2, inplace=True), 
        torch.nn.Linear(in_features=in_features, 
                        out_features=out_features, 
                        bias=True)).to(device)
    
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(params=model.parameters(),
                                lr=learning_rate)
    
    results = train.train(model=model,
                          train_dataloader=train_dataloader,
                          validation_loader=validation_loader,
                          optimizer=optimizer,
                          loss_fn=loss_fn,
                          epochs=epochs,
                          device=device)

    return results, model, class_names