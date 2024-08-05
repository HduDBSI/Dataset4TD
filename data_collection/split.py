# 打开文件
file = open('distribution.txt', 'r')

def str2num(s:str)->int:
    s = s.strip().replace('\\;', '').replace('\\enspace', '').replace(',', '').replace('\\', '')
    return int(s)

def num2str(i:int, max_num:int)->str:
    i = str(i)
    l = len(i)
    if len(i) > 3:
        i = i[:-3] + ',' + i[-3:]
    i = (max_num-l)*'\\enspace' + i
    return i

def pad(s:str)->str:
    if len(s) < 6:
        s = '\enspace' + s
    return s

# 逐行读取文件内容
dic1, dic2, dic3 = {}, {}, {}
median = {}
for line in file:
    # 处理每行数据
    line = line.strip()  # 移除行尾换行符和空格
    data = line.split('&')  # 按&符号分割数据
    dic1[data[0]] = {
        'f#cs': data[1],
        'f#ccs': num2str( str2num(data[5]) + str2num(data[6]), 5),
        'f%%ccs': pad("{:.2%}".format((str2num(data[5]) + str2num(data[6])) / str2num(data[1]) )),

        'c#cs': data[2],
        'c#ccs': num2str(str2num(data[7]) + str2num(data[8]), 5),
        'c%%ccs': pad("{:.2%}".format((str2num(data[7]) + str2num(data[8])) / str2num(data[2]) )),

        'm#cs': data[3],
        'm#ccs': num2str( str2num(data[9]) + str2num(data[10]), 6),
        'm%%ccs': pad("{:.2%}".format((str2num(data[9]) + str2num(data[10])) / str2num(data[3]) )),

        'b#cs': data[4],
        'b#ccs': num2str( str2num(data[11]) + str2num(data[12]), 6),
        'b%%ccs': pad("{:.2%}".format((str2num(data[11]) + str2num(data[12])) / str2num(data[4]) )),
    }

    dic2[data[0]] = {
        'f#ccs': num2str(str2num(data[5]) + str2num(data[6]), 5),
        'f#tdwa': data[5],
        'f%%tdwa': pad("{:.2%}".format(str2num(data[5]) / (str2num(data[5]) + str2num(data[6])) )),

        'c#ccs': num2str(str2num(data[7]) + str2num(data[8]), 5),
        'c#tdwa': data[7],
        'c%%tdwa': pad("{:.2%}".format(str2num(data[7]) / (str2num(data[7]) + str2num(data[8])) )),

        'm#ccs': num2str(str2num(data[9]) + str2num(data[10]), 6),
        'm#tdwa': data[9],
        'm%%tdwa': pad("{:.2%}".format(str2num(data[9]) / (str2num(data[9]) + str2num(data[10])) )),

        'b#ccs': num2str(str2num(data[11]) + str2num(data[12]), 6),
        'b#tdwa': data[11].replace('\\\\',''),
        'b%%tdwa': pad("{:.2%}".format(str2num(data[11]) / (str2num(data[11]) + str2num(data[12])) )),
    }

    dic3[data[0]] = {
        'f#cs': data[1],
        'f#ccs': num2str( str2num(data[5]) + str2num(data[6]), 5),
        'f%%ccs': pad("{:.2%}".format((str2num(data[5]) + str2num(data[6])) / str2num(data[1]) )),
        'f#tdwa': data[5],
        'f%%tdwa': pad("{:.2%}".format(str2num(data[5]) / (str2num(data[5]) + str2num(data[6])) )),

        'c#cs': data[2],
        'c#ccs': num2str( str2num(data[7]) + str2num(data[8]), 5),
        'c%%ccs': pad("{:.2%}".format((str2num(data[7]) + str2num(data[8])) / str2num(data[2]) )),
        'c#tdwa': data[7],
        'c%%tdwa': pad("{:.2%}".format(str2num(data[7]) / (str2num(data[7]) + str2num(data[8])) )),

        'm#cs': data[3],
        'm#ccs': num2str( str2num(data[9]) + str2num(data[10]), 5),
        'm%%ccs': pad("{:.2%}".format((str2num(data[9]) + str2num(data[10])) / str2num(data[3]) )),
        'm#tdwa': data[9],
        'm%%tdwa': pad("{:.2%}".format(str2num(data[9]) / (str2num(data[9]) + str2num(data[10])) )),

        'b#cs': data[4],
        'b#ccs': num2str( str2num(data[11]) + str2num(data[12]), 5),
        'b%%ccs': pad("{:.2%}".format((str2num(data[11]) + str2num(data[12])) / str2num(data[4]) )),
        'b#tdwa': data[11].replace('\\\\',''),
        'b%%tdwa': pad("{:.2%}".format(str2num(data[11]) / (str2num(data[11]) + str2num(data[12])) )),
    }


    
# 关闭文件
file.close()

with open('t1.txt', 'w') as f:
    for key, value in dic1.items():
        line = key + '&' + '&'.join(value.values()) + '\\\\'
        line = line.replace('%', '\%')
        f.write(line + "\n\hline\n")
        
with open('t2.txt', 'w') as f:
    for key, value in dic2.items():
        line = key + '&' + '&'.join(value.values()) + '\\\\'
        line = line.replace('%', '\%')
        f.write(line + "\n\hline\n")

with open('t3.txt', 'w') as f:
    for key, value in dic3.items():
        line = key + '&' + '&'.join(value.values()) + '\\\\'
        line = line.replace('%', '\%')
        f.write(line + "\n\hline\n")

with open('t1.csv', 'w') as f:
    for key, value in dic1.items():
        tmp = value.values()
        tmp = [t.replace('\\enspace', '').replace(',', '').replace('\;','') for t in tmp]
        line = key + ',' + ','.join(tmp)
        f.write(line + "\n")

with open('t2.csv', 'w') as f:
    for key, value in dic2.items():
        tmp = value.values()
        tmp = [t.replace('\\enspace', '').replace(',', '').replace('\;','') for t in tmp]
        line = key + ',' + ','.join(tmp)
        f.write(line + "\n")

with open('t3.csv', 'w') as f:
    for key, value in dic3.items():
        tmp = value.values()
        tmp = [t.replace('\\enspace', '').replace(',', '').replace('\;','') for t in tmp]
        line = key + ',' + ','.join(tmp)
        f.write(line + "\n")
