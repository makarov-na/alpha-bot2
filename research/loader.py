import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def load_data(file_name):
    with open(file_name, mode='r') as data_file:
        lines = data_file.readlines()
    metrics = []
    for line in lines:
        metric = eval(line)
        for sns_count in range(0, len(metric['sns'])):
            metrics.append({'snv': metric['sns'][sns_count], 'sensor': sns_count})

    return pd.DataFrame(metrics)
    
     