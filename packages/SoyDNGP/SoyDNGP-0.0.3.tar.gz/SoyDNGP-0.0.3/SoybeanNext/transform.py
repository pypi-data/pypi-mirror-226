import os
import torch


# This module is used for transforming .pt weights to .onnx weights for better performance.
# The inputPath should be like:
# ../
# inputPath/
#   -- weight1.pt
#   -- weightn.pt
# Results will be outputted to inputPath/../onnx

class Transform:
    # transform .pt weights to .onnx weights, input_W and input_H should be given
    def exportAsONNX(self, inputPath, input_W=206, input_H=206, input_channel=3):
        # path of the weights
        inputPath = inputPath
        # loop through files in the path
        for name in os.listdir(inputPath):
            # determine whether it is .pt weight
            if ".pt" in name:
                # print its name
                print(name)
                # load the weight
                model = torch.load(f"{inputPath}/{name}", map_location=torch.device('cuda'))
                # get the input data's channels number
                input_channel = model[0].in_channels
                # generate a random input tensor
                dummy_input = torch.randn(1, input_channel, input_W, input_H).to('cuda')
                # determine whether the output path exists
                if not os.path.exists(f"{inputPath}/../onnx"):
                    # if not exists, create the folder
                    os.mkdir(f"{inputPath}/../onnx")
                # export the model to .onnx, the first size is dynamic, which means it supports batch-input
                dynamic_axes = {'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
                torch.onnx.export(model, dummy_input, f"{inputPath}/../onnx/{name.replace('pt', 'onnx')}", input_names=['input'], output_names=['output'], dynamic_axes=dynamic_axes)

# an example
t = Transform()
t.exportAsONNX(r"D:\Projects\website\SoybeanWebsite\predict\weight")
