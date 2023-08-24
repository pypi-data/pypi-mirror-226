import os.path
from os import path
import numpy as np
import pandas as pd



def areaUnderCurve(models, modelNames):
    modelAreas = []
    for modelName in modelNames:
        area = 0
        tempModel = models[models['model'] == modelName].copy()
        tempModel.reset_index(drop=True, inplace=True)
        for i in range(1, len(tempModel)):  # df['A'].iloc[2]
            delta = tempModel['n'].iloc[i] - tempModel['n'].iloc[i - 1]
            y = (tempModel['uplift'].iloc[i] + tempModel['uplift'].iloc[i - 1]) / 2
            area += y * delta
        modelAreas.append(area)
    return modelAreas




