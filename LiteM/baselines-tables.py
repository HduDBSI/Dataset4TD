SATDID = '../SATDID/within_project.txt'
TEDIOUS = '../TEDIOUS/within_project.txt'
LiteM = 'results/within_project.txt'
DT = 'results/baseline.txt'

def readLines(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return lines

def getProject_items1(line:str):
    items = line.split("&")
    project = items.pop(0)
    items = [float(item.strip().replace('\\enspace', '').replace('\\%', '').replace('\\\\', '').replace('\n', '')) for item in items]
    return project, items


def getProject_items3(line:str):
    items = line.split("|")
    project = items[0]
    items = items[3:6]
    items = [float(item.strip().replace('%', '')) for item in items]
    items = [-999] * 9 + items
    return project, items

def getProject_items2(line:str):
    items = line.split("|")
    project = items[0]
    items = items[3:6]
    items = [float(item.strip().replace('%', '')) for item in items]
    items = [-999] * 6 + items + [-999] * 3
    return project, items

SATDID_lines = readLines(SATDID)
TEDIOUS_lines = readLines(TEDIOUS)
LiteM_lines = readLines(LiteM)
DT_lines = readLines(DT)

new_lines = []
for i in range(len(LiteM_lines)):
    project, items1 = getProject_items1(LiteM_lines[i])
    _, items2 = getProject_items1(DT_lines[i])
    _, items3 = getProject_items2(TEDIOUS_lines[i])
    _, items4 = getProject_items3(SATDID_lines[i])

    data = [items1, items2, items3, items4]
    max_values = [max(column) for column in zip(*data)]

    transformed_data = []
    for row in data:
        transformed_row = []
        for element, max_value in zip(row, max_values):
            if element == max_value:
                if element < 10:
                    transformed_row.append(f'\\textbf{{\enspace{element:.2f}\\%}}')
                else:
                    transformed_row.append(f'\\textbf{{{element:.2f}\\%}}')
            else:
                if element == -999:
                    transformed_row.append(f' - ')
                elif element < 10:
                    transformed_row.append(f'\enspace{element:.2f}\\%')
                else:
                    transformed_row.append(f'{element:.2f}\\%')
        transformed_data.append(transformed_row)

    lines = [" & ".join(row) for row in transformed_data]
    lines[0] = '& LiteM &' + lines[0] + '\\\\\n'
    lines[1] = '& DT &' + lines[1] + '\\\\\n'
    lines[2] = '& TEDIOUS &' + lines[2] + '\\\\\n'
    lines[3] = '& SATDID &' + lines[3] + '\\\\\n'
    lines = [f'\multirow{{4}}{{*}}{{{project.strip()}}}\n'] + lines + ['\cmidrule[0.8pt]{1-14}\n\n']
    new_lines = new_lines + lines

with open('results/comparison.txt', 'w') as file:
    file.writelines(new_lines)