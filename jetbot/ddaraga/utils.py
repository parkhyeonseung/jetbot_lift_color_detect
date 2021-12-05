import torch
import torchvision
class AutoDrive(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.output_classes=3 # position_bool, people, x, y
        self.model_up = self.making_transfer_model1()

    
    def making_transfer_model1(self):
        model = torchvision.models.squeezenet1_0(pretrained=True)       
        model.classifier=torch.nn.Sequential(
            torch.nn.Dropout(p=0.5, inplace=True),
            torch.nn.Conv2d(512, self.output_classes, kernel_size=(1,1), stride=(1,1)),
            torch.nn.ReLU(True),
            torch.nn.AdaptiveAvgPool2d(output_size=(1,1)),
            torch.nn.Flatten()
        )
        return model

    def forward(self, up_img): # follow / to_position / line_num / loaded
        x_up = self.model_up(up_img)
        return x_up
        
class AutoDriveEF(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.output_classes=3 # position_bool, people, x, y
        self.model_up = self.making_transfer_model1()

    
    def making_transfer_model1(self):
        
        model = torchvision.models.efficientnet_b0(pretrained=True)       
        model.classifier=torch.nn.Sequential(
            torch.nn.Dropout(p=0.5, inplace=True),
            torch.nn.Linear(1280, self.output_classes),
            torch.nn.Softmax(-1),
        )
        return model

    def forward(self, up_img): # follow / to_position / line_num / loaded
        x_up = self.model_up(up_img)
        return x_up

import numpy as np

if __name__ == "__main__":
    in_f = np.random.randn(1,3,224,224)
    auto = AutoDrive()
    out = auto(torch.from_numpy(in_f).float())
    print(out)