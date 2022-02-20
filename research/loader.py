import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_data_in_test_fomat(file_name):
    with open(file_name, mode='r') as data_file:
        lines = data_file.readlines()
    metrics = []
    for line in lines:
        metric = eval(line)
        for sns_count in range(0, len(metric['sns'])):
            metrics.append({'snv': metric['sns'][sns_count], 'sensor': sns_count})

    return pd.DataFrame(metrics)


def load_data(file_name):
    with open(file_name, mode='r') as data_file:
        lines = data_file.readlines()

    result = {}
    for sensor_index in range(0, 5):
        result['sensor' + str(sensor_index)] = []
        pass

    result['left_pid_out'] = []
    result['right_pid_out'] = []
    result['tm'] = []

    for line in lines:
        metric = eval(line)
        result['sensor0'].append(metric['flv']['sns'][0])
        result['sensor1'].append(metric['flv']['sns'][1])
        result['sensor2'].append(metric['flv']['sns'][2])
        result['sensor3'].append(metric['flv']['sns'][3])
        result['sensor4'].append(metric['flv']['sns'][4])
        result['left_pid_out'].append(metric['lp']['o'] * -1)
        result['right_pid_out'].append(metric['rp']['o'] * -1)
        if ('tm' in metric['flv']):
            result['tm'].append(metric['flv']['tm'])

    return result
