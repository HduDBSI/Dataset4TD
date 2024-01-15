one_num_space = '\\enspace'
two_num_space = '\\quad'
one_punc_space = '\\;'

# 1D list operation
def listDivision(list_dividend, list_divisor):
    assert len(list_dividend) == len(list_divisor)
    
    list_quotient = []
    for i in range(len(list_dividend)):
        list_quotient.append(list_dividend[i]/list_divisor[i])
    
    return list_quotient

def listAddition(list_addend1, list_addend2):
    assert len(list_addend1) == len(list_addend2)
    
    list_sum = []
    for i in range(len(list_addend1)):
        list_sum.append(list_addend1[i]+list_addend2[i])
    
    return list_sum

## 2D list operation
def getColumn(list_2D, idx):
    assert idx in range(0, len(list_2D[0])), "invalid location to fetch"
    
    column = []
    for i in range(len(list_2D)):
        column.append(list_2D[i][idx])
    return column

def insertColumn(list_2D, insert_column, idx):
    assert idx in range(0, len(list_2D[0])+1), "invalid location to insert"
    # assert len(list_2D) == len(insert_column), "length not match"
    list_2D = [row[:idx] + [insert_column[i]] + row[idx:] for i, row in enumerate(list_2D)]
    return list_2D

def replaceColumn(list_2D, replace_column, idx):
    assert idx in range(0, len(list_2D[0])), "invalid location to replace"
    assert len(list_2D) == len(replace_column), "length not match"
    
    for i in range(len(list_2D)):
        list_2D[i][idx] = replace_column[i]
    
    return list_2D

def horizontalJoin(left_list, right_list):
    assert len(left_list) == len(right_list), "length not match"
    col_num = len(left_list[0])
    for i in range(len(right_list[0])):
        column = getColumn(list_2D=right_list, idx=i)
        left_list = insertColumn(list_2D=left_list, insert_column=column, idx=col_num+i)
    
    return left_list

def insertRow(list_2D, insert_row, idx):
    assert idx in range(0, len(list_2D)+1), "invalid location to insert"
    assert len(list_2D[0]) == len(insert_row), "length not match"
    list_2D.insert(idx, insert_row)
    return list_2D

def sumEachColumn(list_2D):
    col_sums = [sum(col) for col in zip(*list_2D)]
    return col_sums

def avgEachColumn(list_2D):
    col_sums = [sum(col) if isinstance(col[0], (int, float)) else "None" for col in zip(*list_2D)]
    col_avgs = [col/len(list_2D) if isinstance(col, (int, float)) else "None" for col in col_sums ]
    return col_avgs

def formatEachElement(table_matrix):
    # Traverse through each element in the 2D list
    for i in range(len(table_matrix)):
        for j in range(len(table_matrix[i])):
            # If the element is a floating-point number less than 1
            if isinstance(table_matrix[i][j], float) and table_matrix[i][j] <= 1:
                table_matrix[i][j] = '{:.2f}\\%'.format(100*table_matrix[i][j])
            # If the element is an integer greater than 1
            elif isinstance(table_matrix[i][j], int) and table_matrix[i][j] >= 1:
                # # Convert the integer to string
                # num_str = str(table_matrix[i][j])
                # # Insert commas to separate thousands
                # table_matrix[i][j] = ','.join([num_str[i:i+3][::-1] for i in range(0, len(num_str), 3)])[::-1]
                table_matrix[i][j] = "{:,}".format(table_matrix[i][j])
            elif isinstance(table_matrix[i][j], float) and table_matrix[i][j] > 1:
                table_matrix[i][j] = str(int(table_matrix[i][j]))
                
    return table_matrix

def find_max_len_str(str_list):
    # Initialize the maximum length and corresponding string to empty values
    max_len = 0
    max_str = ''
    # Traverse through each string in the list
    for string in str_list:
        # If the length of the current string is greater than the maximum length so far
        if len(string) > max_len:
            # If the length of the current string is greater than the maximum length so far
            max_len = len(string)
            max_str = string
    # Return the string which has the maximum length
    return max_str

def countNumAndComma(s:str):
    # Initialize the counters for the number and comma characters to zero
    num_count = 0
    comma_count = 0
    
    # Traverse through each character in the input string
    for ch in s:
        # If the current character is a digit, increment the number counter
        if ch.isdigit():
            num_count += 1
        # Otherwise, increment the comma counter
        else:
            comma_count += 1
    
    # Return a tuple containing the number and comma counts
    return num_count, comma_count

def hasAlphabet(s:str):
    for ch in s:
        if ('a' <= ch and ch <= 'z') or ('A' <= ch and ch <= 'Z'):
            return True
    return False

def alignColumn(table_matrix):
    # iterate through each column of the matrix
    for col_idx in range(len(table_matrix[0])):
        # if the first row of the column contains an alphabet, skip alignment
        if hasAlphabet(table_matrix[0][col_idx]):
            continue
        else:
            # create a new list from the column
            new_col = [row[col_idx] for row in table_matrix]
            # if the column contains percentage values
            if '%' in new_col[0]:
                # add leading space to each percentage value if it has less than 7 characters
                for i in range(len(new_col)):
                    if len(new_col[i]) < 7:
                        new_col[i] = one_num_space + new_col[i]
                # replace the original column with the aligned one
                table_matrix = replaceColumn(table_matrix, new_col, col_idx)

            # if the column contains integer values
            else:
                # find the string with the maximum length in the column
                max_str = find_max_len_str(new_col)
                max_num_count, max_comma_count = countNumAndComma(max_str)

                # align each integer value with leading space and comma
                for i in range(len(new_col)):
                    num_count, comma_count = countNumAndComma(new_col[i])
                    new_col[i] = (max_num_count-num_count)*one_num_space + new_col[i]
                    new_col[i] = (max_comma_count-comma_count)*one_punc_space + new_col[i]
                # replace the original column with the aligned one
                table_matrix = replaceColumn(table_matrix, new_col, col_idx)
    # return the aligned matrix
    return table_matrix

# Concatenate each element of a line with '&' and end each line with '\\' symbol.
def concatLine(table_matrix):
    lines = []
    for i in range(len(table_matrix)):
        line = ' & '.join(table_matrix[i]) + '\\\\'
        lines.append(line)
    return lines


def writeTable(table_matrix, save_file):
    # Format each element in the table
    table_matrix = formatEachElement(table_matrix)
    # Align columns in the table
    table_matrix = alignColumn(table_matrix)
    # Concatenate lines in the table
    lines = concatLine(table_matrix)

    # Write the formatted table to file
    with open(save_file, 'w') as f:
        for line in lines:
            f.write(line + '\n')


def test():
    # a = [["DBeaver", 0.40, 0.036, 1234],["Elasticsearch", 0.5561, 0.0866, 23]]

    # writeTable(a)
    
    matrix = [
        [1234, 1234, 2334, 75], 
        [1344, 893, 3094, 9], 
        [364, 2585, 1349, 1432]
    ]
    firstColumn = ['dataset1', 'dataset2', 'dataset3']
    sums = sumEachColumn(matrix)
    matrix = insertRow(matrix, sums, len(matrix))
    firstColumn.append('Total')
    matrix = insertColumn(matrix, firstColumn, 0)
    writeTable(matrix)
    
if __name__=='__main__':
    test()