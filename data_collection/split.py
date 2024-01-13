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
dic1, dic2 = {}, {}
median = {}
for line in file:
    # 处理每行数据
    line = line.strip()  # 移除行尾换行符和空格
    data = line.split('&')  # 按&符号分割数据
    dic1[data[0]] = {
        '#file': data[1],
        '#fwc': num2str( str2num(data[5]) + str2num(data[6]), 5),
        'pfwc': pad("{:.2%}".format((str2num(data[5]) + str2num(data[6])) / str2num(data[1]) )),

        '#class': data[2],
        '#cwc': num2str(str2num(data[7]) + str2num(data[8]), 5),
        'pcwc': pad("{:.2%}".format((str2num(data[7]) + str2num(data[8])) / str2num(data[2]) )),

        '#method': data[3],
        '#mwc': num2str( str2num(data[9]) + str2num(data[10]), 6),
        'pmwc': pad("{:.2%}".format((str2num(data[9]) + str2num(data[10])) / str2num(data[3]) )),

        '#block': data[4],
        '#bwc': num2str( str2num(data[11]) + str2num(data[12]), 6),
        'pbwc': pad("{:.2%}".format((str2num(data[11]) + str2num(data[12])) / str2num(data[4]) )),
    }

    dic2[data[0]] = {
        '#fwc': num2str(str2num(data[5]) + str2num(data[6]), 5),
        '#fwc1': data[5],
        'pfwc1': pad("{:.2%}".format(str2num(data[5]) / (str2num(data[5]) + str2num(data[6])) )),

        '#cwc': num2str(str2num(data[7]) + str2num(data[8]), 5),
        '#cwc1': data[7],
        'pcwc1': pad("{:.2%}".format(str2num(data[7]) / (str2num(data[7]) + str2num(data[8])) )),

        '#mwc': num2str(str2num(data[9]) + str2num(data[10]), 6),
        '#mwc1': data[9],
        'pmwc1': pad("{:.2%}".format(str2num(data[9]) / (str2num(data[9]) + str2num(data[10])) )),

        '#bwc': num2str(str2num(data[11]) + str2num(data[12]), 6),
        '#bwc1': data[11].replace('\\\\',''),
        'pbwc1': pad("{:.2%}".format(str2num(data[11]) / (str2num(data[11]) + str2num(data[12])) )),
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