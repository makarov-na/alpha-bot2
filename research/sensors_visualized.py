from loader import load_data

data = load_data('./data/12_right_corner_naive_problem_on_curve/2022-05-14_15:50:45.log')

print(len(data['sensor0']))
black_level = range(0, 21)
middle_level = range(22, 79)
white_level = range(80, 101)

for i in (range(0, len(data['sensor0']))):

    out = list('_____')
    if data['sensor0'][i] in black_level:
        out[0] = 'X'
    if data['sensor1'][i] in black_level:
        out[1] = 'X'
    if data['sensor2'][i] in black_level:
        out[2] = 'X'
    if data['sensor3'][i] in black_level:
        out[3] = 'X'
    if data['sensor4'][i] in black_level:
        out[4] = 'X'
    if data['sensor0'][i] in middle_level:
        out[0] = '|'
    if data['sensor1'][i] in middle_level:
        out[1] = '|'
    if data['sensor2'][i] in middle_level:
        out[2] = '|'
    if data['sensor3'][i] in middle_level:
        out[3] = '|'
    if data['sensor4'][i] in middle_level:
        out[4] = '|'

    print("".join(out))

