import onnxruntime as onnx
import os
import cupy as np
import yaml
import pandas as pd


# This module is used for predicting and analysis the results.
# Onnxruntime could run on GPU or CPU, which depends on your installed version of this package.
# If you would like to run it on your GPU, uninstall 'onnxruntime' at first, then install 'onnxruntime-gpu'.


class Forward:
    def __init__(self, traits):
        # the path of models, it should be like:
        # ../
        # onnx/
        #   -- model1.onnx
        #   -- modeln.onnx
        # if this path does not exist, it will be automatically create, and weights will be downloaded to it
        if not os.path.exists(r'data/onnx'):
            pass
        self.modelsPath = r'data/onnx/'
        # list of supported Quality Traits and corresponding index to value dictionary
        with open("data/p_trait.yaml") as p:
            self.data_p = yaml.safe_load(p)
        with open("data/n_trait.yaml") as n:
            self.data_n = yaml.safe_load(n)
        # traits to predict
        self.traits = list(set(traits))
        # preload needed models
        self.models = {trait: onnx.InferenceSession(self.modelsPath + trait + '_best.onnx', providers=['CUDAExecutionProvider', 'CPUExecutionProvider']) for trait in self.traits}

    # input is a list of samples
    # here, unpack the input data and split results by different trait types
    def forward(self, index_list, input_data=None, batch_size=1):
        # transform the cupy array to numpy array (to avoid onnxruntime errors)
        input_data = np.asnumpy(input_data)
        # outputs of final results
        df = pd.DataFrame(None, columns=self.traits, index=index_list)
        # predict each trait for each sample
        for trait, model in self.models.items():
            # determine if this trait is a Quality Trait
            if trait in self.data_p.keys():
                # results
                results = []
                # indexed levels dictionary of this trait
                traitLevels = self.data_p[trait]
                # generate batched data and forward them
                for batch in self.batch_generator(input_data, batch_size):

                    # raw results of this batch, its shape is batch * levels' amount
                    out = model.run(['output'], {'input': batch})[0]
                    # turn raw results to indexes
                    out = out.argmax(axis=1)
                    # merge output to list results, for matching levels in only one loop
                    results += out.tolist()
                df[trait] = [traitLevels[result] for result in results]
            # this trait is a Quantity Trait
            else:
                # results
                results = []
                traitMax = self.data_n[trait]['max']
                traitMin = self.data_n[trait]['min']
                traitDiff = traitMax - traitMin
                for batch in self.batch_generator(input_data, batch_size):
                    # raw results of this batch, its shape is batch * levels' amount
                    out = model.run(['output'], {'input': batch})[0]
                    # merge output to list results, for matching levels in only one loop
                    results += out.tolist()
                # denormalize the result
                df[trait] = np.array(results) * traitDiff + traitMin
        return df

    # slice the input data into batches
    def batch_generator(self, input_data, batch_size=1):
        start = 0
        # which batch is running now
        times = 1
        while start < input_data.shape[0]:
            end = start + batch_size
            # load input data batch by batch
            yield input_data[start:end, :, :, :]
            start = end
            times += 1

    def output_dataframe(self, dataframe):
        dataframe.to_excel("./result.xlsx")