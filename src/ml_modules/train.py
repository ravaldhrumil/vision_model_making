from typing import Dict, List, Tuple
import torch


def train_step(model: torch.nn.Module, 
               dataloader: torch.utils.data.DataLoader, 
               loss_fn: torch.nn.Module, 
               optimizer: torch.optim.Optimizer,
               device: torch.device) -> Tuple[float, float]:
    
    model.train()

    train_loss, train_acc = 0,0

    for batch,(X,y )in enumerate(dataloader):
        X,y = X.to(device), y.to(device)

        y_pred = model(X)

        loss = loss_fn(y_pred, y)
        train_loss += loss.item() 
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        y_pred_class = torch.argmax(torch.softmax(y_pred, dim=1), dim=1)
        train_acc += (y_pred_class == y).sum().item()/len(y_pred)

    train_loss = train_loss / len(dataloader)
    train_acc = train_acc / len(dataloader)

    return train_loss, train_acc
    

def test_step(model: torch.nn.Module, 
              dataloader: torch.utils.data.DataLoader, 
              loss_fn: torch.nn.Module,
              device: torch.device) -> Tuple[float, float]:
    
    model.eval()
    test_loss, test_acc = 0,0

    with torch.inference_mode():
        for batch,(X,y)in enumerate(dataloader):
            X,y = X.to(device), y.to(device)

            y_pred_logit = model(X) 
            loss = loss_fn(y_pred_logit, y)
            test_loss += loss.item()

            
            test_pred_labels = y_pred_logit.argmax(dim=1)
            test_acc += ((test_pred_labels == y).sum().item()/len(test_pred_labels))
   
    
    test_loss = test_loss / len(dataloader)
    test_acc = test_acc / len(dataloader)
    return test_loss, test_acc





def train(model: torch.nn.Module,   
          train_dataloader: torch.utils.data.DataLoader, 
          validation_loader: torch.utils.data.DataLoader, 
          optimizer: torch.optim.Optimizer,
          loss_fn: torch.nn.Module,
          epochs: int,
          device: torch.device) -> Dict[str, List]:
    

    results = {"epochs":[i+1 for i in range(int(epochs))],
                "train_loss": [],
               "train_acc": [],
               "test_loss": [],
               "test_acc": []
    }


    for epoch in range(int(epochs)):
        train_loss, train_acc = train_step(model=model,
                                          dataloader=train_dataloader,
                                          loss_fn=loss_fn,
                                          optimizer=optimizer,
                                          device=device)
        
        test_loss, test_acc = test_step(model=model,
          dataloader=validation_loader,
          loss_fn=loss_fn,
          device=device)

        # print(
        #   f"Epoch: {epoch+1} | "
        #   f"train_loss: {train_loss:.4f} | "
        #   f"train_acc: {train_acc:.4f} | "
        #   f"test_loss: {test_loss:.4f} | "
        #   f"test_acc: {test_acc:.4f}"
        # )

        
        results["train_loss"].append(train_loss)
        results["train_acc"].append(train_acc * 100)
        results["test_loss"].append(test_loss)
        results["test_acc"].append(test_acc * 100)

    return results