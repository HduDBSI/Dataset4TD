import subprocess
import pandas as pd
import sys
sys.path.append("../") 
from project_Info import projects
from tqdm import tqdm


remove_str1 = "( ClassOrInterfaceDeclaration_A ( Modifier_public ) Modifier_public ( SimpleName_A ) SimpleName_A ( MethodDeclaration_void_B ( Modifier_public ) Modifier_public ( SimpleName_B ) SimpleName_B ( VoidType_null ) VoidType_null "
remove_str2 = " ) MethodDeclaration_void_B ) ClassOrInterfaceDeclaration_A"
def call_jar(input_string, block_statement=True):
    if block_statement:
        input_string = 'public class A{ public void B (){ ' + input_string + '}}' 
    
    # fetch python version
    current_version = sys.version_info

    if current_version >= (3, 7): # for python >= 3.7
        result = subprocess.run(['java', '-jar', 'SBT_single.jar', input_string], capture_output=True, text=True)
        output_string = result.stdout.strip()
    
    else:           # for python <= 3.6
        result = subprocess.run(['java', '-jar', 'SBT_single.jar', input_string], stdout=subprocess.PIPE)
        output_string = result.stdout.decode('utf-8').strip()

    if block_statement:
        output_string = output_string.replace(remove_str1,'').replace(remove_str2,'')
    
    return output_string

# def process(srcFile, tgtFile):
#     src_df= pd.read_csv(srcFile)
#     SBT = []
#     for i in tqdm(range(len(src_df))):
#         SBT.append(call_jar(src_df['Content'][i]))
    
#     src_df['SBT'] = SBT
#     src_df[['SBT', 'CommentsAssociatedLabel']].to_csv(tgtFile, index=False)

# for project in projects:
#     srcFile = f'../code snippets-with-labels&metrics/block/{project}_blockLevel.csv'
#     tgtFile = f'data/{project}_blockLevel.csv'
#     process(srcFile, tgtFile)
#     print(project,'done.')


# 示例调用
def test():
    input_string = """
        return requests.remove(id);
    """
    output_string = call_jar(input_string)
    print(output_string)


test()