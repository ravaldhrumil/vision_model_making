from torch.utils.data import DataLoader
from torchvision import datasets
import torchvision
import numpy as np
from torch.utils.data.sampler import SubsetRandomSampler

def data_loader(train_dir: str,
                auto_transfoms:torchvision.transforms):
    
    data = datasets.ImageFolder(
    root=train_dir,
    transform=auto_transfoms,
    target_transform=None)

    class_names = data.classes
    BATCH_SIZE = 32
    VALIDATION_SPLIT = 0.2
    SHUFFLE_DATASET = True

    dataset_size = len(data)
    indices = list(range(dataset_size))
    split = int(np.floor(VALIDATION_SPLIT * dataset_size))

    if SHUFFLE_DATASET :
        np.random.seed(42)
        np.random.shuffle(indices)
    train_indices, val_indices = indices[split:], indices[:split]

    train_sampler = SubsetRandomSampler(train_indices)
    valid_sampler = SubsetRandomSampler(val_indices)

    train_dataloader = DataLoader(data, 
                                batch_size=BATCH_SIZE, 
                                sampler=train_sampler)
    
    validation_loader = DataLoader(data, 
                                    batch_size=BATCH_SIZE,
                                    sampler=valid_sampler)
    
    return train_dataloader, validation_loader, class_names