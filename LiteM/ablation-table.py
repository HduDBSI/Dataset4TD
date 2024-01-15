adaptedSMOTE = 'results/within_project.txt'
SMOTE = 'results/within_project_SMOTE.txt'
NoSMOTE = 'results/within_project_NoSMOTE.txt'
ADASYN = 'results/within_project_ADASYN.txt'

def readLines(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return lines

def getProject_items(line:str):
    items = line.split("&")
    project = items.pop(0)
    items = [float(item.strip().replace('\\enspace', '').replace('\\%', '').replace('\\\\', '').replace('\n', '')) for item in items]
    return project, items


ASMOTE_lines = readLines(adaptedSMOTE)
SMOTE_lines = readLines(SMOTE)
NoSMOTE_lines = readLines(NoSMOTE)
ADASYN_lines = readLines(ADASYN)

# adaptedSMOTE_lines = ['& adaptedSMOTE' + line for line in adaptedSMOTE_lines]
# SMOTE_lines = ['& SMOTE' + line for line in SMOTE_lines]
# NoSMOTE_lines = ['& NoSMOTE' + line for line in NoSMOTE_lines]
# ADASYN_lines = ['& ADASYN' + line for line in ADASYN_lines]

new_lines = []
for i in range(len(SMOTE_lines)):
    project, items1 = getProject_items(NoSMOTE_lines[i])
    _, items2 = getProject_items(SMOTE_lines[i])
    _, items3 = getProject_items(ADASYN_lines[i])
    _, items4 = getProject_items(ASMOTE_lines[i])

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
                if element < 10:
                    transformed_row.append(f'\enspace{element:.2f}\\%')
                else:
                    transformed_row.append(f'{element:.2f}\\%')
        transformed_data.append(transformed_row)

    lines = [" & ".join(row) for row in transformed_data]
    lines[0] = '& NoSMOTE &' + lines[0] + '\\\\\n'
    lines[1] = '& SMOTE &' + lines[1] + '\\\\\n'
    lines[2] = '& ADASYN &' + lines[2] + '\\\\\n'
    lines[3] = '& ASMOTE &' + lines[3] + '\\\\\n'
    lines = [f'\multirow{{4}}{{*}}{{{project.strip()}}}\n'] + lines + ['\cmidrule[0.8pt]{1-14}\n\n']
    new_lines = new_lines + lines

with open('results/ablation.txt', 'w') as file:
    file.writelines(new_lines)