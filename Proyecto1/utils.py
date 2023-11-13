

import pandas as pd

def getColumnTypes(dataset):
    continuas = []
    discretas = []
    categoricas = []
    fechas = []

    for col in dataset.columns:
        if (dataset[col].dtype == 'int64'):
            discretas.append(col)
        elif(dataset[col].dtype == 'float64'):
            continuas.append(col)
        elif(dataset[col].dtype == 'datetime64'):
            fechas.append(col)
        elif(dataset[col].dtype == 'object'):
                categoricas.append(col)

    return continuas, discretas, categoricas, fechas