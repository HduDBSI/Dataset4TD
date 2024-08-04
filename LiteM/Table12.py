import re

SATDID_result = '../SATDID/results/cross_project.txt'
TEDIOUS_result = '../TEDIOUS/results/cross_project.txt'
LiteM_result = 'results/cross_project.txt'

def readLines(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return lines

def getProject_items(line:str):
    items = line.split("&")
    project = items.pop(0)
    pattern = re.compile(r'\\enspace|\\%|\\\\|\\n|\\;')  

    items = [float(pattern.sub('', item.strip())) for item in items]
    
    return project, items

SATDID_lines = readLines(SATDID_result)
TEDIOUS_lines = readLines(TEDIOUS_result)
LiteM_lines = readLines(LiteM_result)

new_lines = []
for i in range(len(LiteM_lines)):
    project_names, LiteM_datum = getProject_items(LiteM_lines[i])
    _, TEDIOUS_datum = getProject_items(TEDIOUS_lines[i])
    _, SATDID_datum = getProject_items(SATDID_lines[i])

    TEDIOUS_datum = [-999] * 10 + TEDIOUS_datum + [-999] * 5
    SATDID_datum = [-999] * 15 + SATDID_datum

    data = [LiteM_datum, TEDIOUS_datum, SATDID_datum]
    max_values = [max(column) for column in zip(*data)]

    transformed_data = []
    for row in data:
        transformed_row = []
        for element, max_value in zip(row, max_values):
            if element == max_value:
                transformed_row.append(f'\\textbf{{{element:.2f}}}')
            else:
                if element == -999:
                    transformed_row.append(f' - ')
                else:
                    transformed_row.append(f'{element:.2f}')
        transformed_data.append(transformed_row)

    lines = [" & ".join(row) for row in transformed_data]
    lines[0] = '& LiteM &' + lines[0] + '\\\\\n'
    lines[1] = '& TEDIOUS &' + lines[1] + '\\\\\n'
    lines[2] = '& SATDID &' + lines[2] + '\\\\\n'

    lines = [f'\multirow{{3}}{{*}}{{{project_names.strip()}}}\n'] + lines + ['\cmidrule[0.8pt]{1-22}\n\n']
    new_lines = new_lines + lines

with open('results/Table12.txt', 'w') as file:
    file.writelines(new_lines)