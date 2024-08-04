import re


MAT_result = 'results/LiteMC-PseudoLabelForCASFromMAT.txt'
MATP_result = 'results/LiteMC-PseudoLabelForCASFromMAT+.txt'
XGBoost_result = 'results/LiteMC-PseudoLabelForCASFromXGBoost.txt'
GGSATD_result = 'results/LiteMC-PseudoLabelForCASFromGGSATD.txt'

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

MAT_lines = readLines(MAT_result)
MATP_lines = readLines(MATP_result)
XGBoost_lines = readLines(XGBoost_result)
GGSATD_lines = readLines(GGSATD_result)

new_lines = []
for i in range(len(XGBoost_lines)):
    project_names, XGBoost_datum = getProject_items(XGBoost_lines[i])
    _, GGSATD_datum = getProject_items(GGSATD_lines[i])
    _, MATP_datum = getProject_items(MATP_lines[i])
    _, MAT_datum = getProject_items(MAT_lines[i])

    data = [MATP_datum, MAT_datum, XGBoost_datum, GGSATD_datum, ]
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
    lines[0] = '& MAT+ &' + lines[0] + '\\\\\n'
    lines[1] = '& MAT &' + lines[1] + '\\\\\n'
    lines[2] = '& XGB-based &' + lines[2] + '\\\\\n'
    lines[3] = '& GGSATD &' + lines[3] + '\\\\\n'

    lines = [f'\multirow{{4}}{{*}}{{{project_names.strip()}}}\n'] + lines + ['\cmidrule[0.8pt]{1-22}\n\n']
    new_lines = new_lines + lines

with open('results/Table4LiteMC.txt', 'w') as file:
    file.writelines(new_lines)