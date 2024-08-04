techniques = ['ASMOTE', 'SMOTE', 'NoSMOTE', 'ADASYN']

def readLines(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return lines

def getProject_items(line:str):
    items = line.split("&")
    project = items.pop(0)
    items = [float(item.strip().replace('\\enspace', '').replace('\\%', '').replace('\\\\', '').replace('\n', '').replace('-', '')) for item in items]
    return project_name, project_datum

tables = []
for tech in techniques:
    table = readLines(f'results/within_project_{tech}_LightGBM.txt')
    tables.append(table)

line_num = len(tables[0])
new_lines = []

for i in range(line_num):
    project_data = []
    for table in tables:
        project_names, project_datum = getProject_items(table[i])
        project_data.append(project_datum)

    max_values = [max(column) for column in zip(*project_data)]

    transformed_data = []
    for row in project_data:
        transformed_row = []
        for element, max_value in zip(row, max_values):
            if element == max_value:
                transformed_row.append(f'\\textbf{{{element:.2f}}}')
            else:
                transformed_row.append(f'{element:.2f}')
        transformed_data.append(transformed_row)

    lines = [" & ".join(row) for row in transformed_data]
    for i, tech in enumerate(techniques):
        lines[i] = f'& {tech} &' + lines[i] + '\\\\\n'
    
    lines = [f'\multirow{{4}}{{*}}{{{project_names.strip()}}}\n'] + lines + ['\cmidrule[0.8pt]{1-22}\n\n']
    new_lines = new_lines + lines

with open('results/RQ2.txt', 'w') as file:
    file.writelines(new_lines)