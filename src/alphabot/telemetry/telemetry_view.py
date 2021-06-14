import ast
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

#file_name = '/home/mna/tmp/data/without_zero_speed/2021-05-09_16:57:07.log'

#file_name = '/home/mna/tmp/data/with_zero_speed/2021-05-09_16:49:53.log'
file_name = '/home/mna/tmp/data/2021-06-14_20:27:43.log'

def read_metrics_from_file(file_name):
    with open(file_name) as file_stream:
        raw_data = file_stream.readlines()
    metrics = []
    for str_line in raw_data:
        metrics.append(ast.literal_eval(str_line))
    return metrics


metrics = read_metrics_from_file(file_name)

time_data = [0]
left_sensor_data = []
right_sensor_data = []
turn_data = []
left_pid_error = []
left_pid_out = []
left_pid_out_p = []
left_pid_out_d = []
left_pid_out_i = []
right_pid_out_p = []
right_pid_out_d = []
right_pid_out_i = []
right_pid_error = []
right_pid_out = []

for metric in metrics:
    time_data.append(time_data[-1] + metric['flv']['dt'])
    left_sensor_data.append(metric['flv']['sns'][1] - 348)
    right_sensor_data.append(metric['flv']['sns'][3] - 298)
    turn_data.append((metric['flv']['tn']))
    left_pid_error.append(metric['lp']['err'])
    if left_pid_error[-1] > 0:
        left_pid_error[-1] = 0
    left_pid_out.append(metric['lp']['o'])
    if left_pid_out[-1] > 0:
        left_pid_out[-1] = 0
    left_pid_out_p.append(metric['lp']['po'])
    left_pid_out_d.append(metric['lp']['do'])
    left_pid_out_i.append(metric['lp']['io'])
    right_pid_out_p.append(metric['rp']['po'])
    right_pid_out_d.append(metric['rp']['do'])
    right_pid_out_i.append(metric['rp']['io'])
    right_pid_error.append(metric['rp']['err'])
    if right_pid_error[-1] > 0:
        right_pid_error[-1] = 0
    right_pid_out.append(metric['rp']['o'])
    if right_pid_out[-1] > 0:
        right_pid_out[-1] = 0

time_data.remove(0)

turn_data = [-number if number > 0 else number for number in turn_data]
left_pid_error = [-number if number < 0 else number for number in left_pid_error]
#left_pid_out = [-number if number < 0 else number for number in left_pid_out]

right_pid_error = [-number if number < 0 else number for number in right_pid_error]
right_pid_out = [-number if number < 0 else number for number in right_pid_out]

fig, ax = plt.subplots()
#ax.plot(time_data, left_sensor_data, label='left sensor')
ax.plot(time_data, left_pid_error, label='left PID error')
ax.plot(time_data, left_pid_out, label='left PID out')



ax.plot(time_data, left_pid_out_p, label='lpop')
ax.plot(time_data, left_pid_out_d, label='lpod')
#ax.plot(time_data, left_pid_out_i, label='lpoi')
#ax.plot(time_data, right_sensor_data, label='right sensor')
#ax.plot(time_data, right_pid_error, label='right PID error')
#ax.plot(time_data, right_pid_out, label='right PID out')
#ax.plot(time_data, right_pid_out_p, label='rpop')
#ax.plot(time_data, right_pid_out_d, label='rpod')
#ax.plot(time_data, right_pid_out_i, label='rpoi')
#ax.plot(time_data, turn_data, label='turn value')

major_xticks = np.linspace(0, time_data[-1], 50)
major_yticks = np.linspace(min(left_sensor_data), max(left_sensor_data), 50)
ax.set_xticks(major_xticks)
ax.set_yticks(major_yticks)
ax.legend()
ax.grid()
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
plt.show()
