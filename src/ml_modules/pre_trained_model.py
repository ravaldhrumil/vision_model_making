import torchvision, torch
from torch import nn

def initialisation(pretrained_model_name: str, 
                   device: torch.device):

    if pretrained_model_name == "EfficientNet":
        weights = torchvision.models.EfficientNet_B0_Weights.DEFAULT
        model = torchvision.models.efficientnet_b0(weights=weights).to(device)
        in_features = 1280

    elif pretrained_model_name == "ResNet152":
        weights = torchvision.models.ResNet152_Weights.DEFAULT
        model = torchvision.models.resnet152(weights=weights).to(device)
        in_features = 2048

    elif pretrained_model_name == "VGG11":
        weights = torchvision.models.VGG11_Weights.DEFAULT
        model = torchvision.models.vgg11(weights=weights).to(device)
        in_features = 25088

    auto_transfoms = weights.transforms()
    for param in model.parameters():
        param.requires_grad = False

    return auto_transfoms, in_features, model

def classifier(in_features: int,
               out_features: int,
               device: torch.device,
               learning_rate: float,
               model: torch.nn.Module,
               pretrained_model_name: str): 
    torch.cuda.manual_seed(42)

    if pretrained_model_name in ["ResNet152"]:
        model.fc = nn.Sequential(
        torch.nn.Dropout(p=0.2, inplace=True), 
        torch.nn.Linear(in_features=in_features, 
                        out_features=out_features, 
                        bias=True)).to(device)
    
    elif pretrained_model_name in ["VGG11","EfficientNet"]:
        model.classifier = nn.Sequential(
            torch.nn.Dropout(p=0.2, inplace=True), 
            torch.nn.Linear(in_features=in_features, 
                            out_features=out_features, 
                            bias=True)).to(device)
    
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(params=model.parameters(),
                                lr=learning_rate)
    
    return model, loss_fn, optimizer