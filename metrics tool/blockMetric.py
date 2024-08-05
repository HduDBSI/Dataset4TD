from javalang import parse, tree
import sys
import time
import copy
import numpy as np
sys.path.append("../") 
from project_Info import projects, granularities, project_names
import pandas as pd
node_types = [
    tree.Annotation,                    # An annotation node in the AST.
    tree.AnnotationDeclaration,         # A declaration of an annotation type.
    tree.AnnotationMethod,              # A method declaration within an annotation type.
    tree.ArrayCreator,                  # An array creation expression.
    tree.ArrayInitializer,              # An array initializer expression.
    tree.ArraySelector,                 # An array access expression.
    tree.AssertStatement,               # An assert statement.
    tree.Assignment,                    # An assignment expression.
    tree.BasicType,                     # A basic type (e.g., int, float, boolean).
    tree.BinaryOperation,               # A binary operation expression (e.g., +, -, *, /).
    tree.BlockStatement,                # A block of statements.
    tree.BreakStatement,                # A break statement.
    tree.Cast,                          # A type cast expression.
    tree.CatchClause,                   # A catch clause in a try-catch block.
    tree.CatchClauseParameter,          # A parameter in a catch clause.           same with catchClause
    tree.ClassCreator,                  # A class instance creation expression.
    tree.ClassDeclaration,              # A class declaration.
    tree.ClassReference,                # A reference to a class.
    tree.CompilationUnit,               # A compilation unit (i.e., a source file).
    tree.ConstantDeclaration,           # A declaration of a constant variable.
    tree.ConstructorDeclaration,        # A constructor declaration.
    tree.ContinueStatement,             # A continue statement.
    tree.Creator,                       # A creator expression (e.g., new).
    tree.Declaration,                   # A declaration statement.
    tree.Documented,                    # A node that has associated documentation.
    tree.DoStatement,                   # A do-while loop statement.
    tree.ElementArrayValue,             # An element in an array initializer expression.
    tree.ElementValuePair,              # A named argument in an annotation type.
    tree.EnhancedForControl,            # A for-each loop statement.
    tree.EnumBody,                      # The body of an enum declaration.
    tree.EnumConstantDeclaration,       # A declaration of an enum constant.
    tree.EnumDeclaration,               # An enum declaration.
    tree.ExplicitConstructorInvocation, # A constructor invocation statement.
    tree.Expression,                    # A generic expression node.
    tree.FieldDeclaration,              # A field declaration.
    tree.ForControl,                    # A for loop control expression.
    tree.FormalParameter,               # A formal parameter in a method declaration.
    tree.ForStatement,                  # A for loop statement.
    tree.IfStatement,                   # An if statement.
    tree.Import,                        # An import statement.
    tree.InferredFormalParameter,       # An inferred formal parameter in a lambda expression.
    tree.InnerClassCreator,             # An inner class instance creation expression.
    tree.InterfaceDeclaration,          # An interface declaration.
    tree.Invocation,                    # An invocation of a method.
    tree.LambdaExpression,              # A lambda expression.
    tree.Literal,                       # A literal value (e.g., a string or number).
    tree.LocalVariableDeclaration,      # A local variable declaration statement.
    tree.Member,                        # A member of a class or interface.
    tree.MemberReference,               # A reference to a member of a class or interface.
    tree.MethodDeclaration,             # A method declaration.
    tree.MethodInvocation,              # A method invocation expression.
    tree.MethodReference,               # A reference to a method.
    tree.Node,                          # A generic node in the AST.
    tree.PackageDeclaration,            # A package declaration.
    tree.Primary,                       # A primary expression.
    tree.ReferenceType,                 # A reference to a type.
    tree.ReturnStatement,               # A return statement in a method or lambda.
    tree.Statement,                     # A statement in a block.
    tree.StatementExpression,           # An expression used as a statement.
    tree.SuperConstructorInvocation,    # A call to a constructor of the superclass.
    tree.SuperMemberReference,          # A reference to a member of the superclass.
    tree.SuperMethodInvocation,         # A call to a method of the superclass.
    tree.SwitchStatement,               # A switch statement.
    tree.SwitchStatementCase,           # A case label in a switch statement.
    tree.SynchronizedStatement,         # A synchronized block.
    tree.TernaryExpression,             # A ternary expression.
    tree.This,                          # A reference to the current object.
    tree.ThrowStatement,                # A throw statement.
    tree.TryResource,                   # A resource in a try-with-resources statement.
    tree.TryStatement,                  # A try-catch-finally statement.
    tree.Type,                          # A type node in a declaration or expression.
    tree.TypeArgument,                  # A type argument in a generic method or constructor.
    tree.TypeDeclaration,               # A type declaration (class, interface, enum, or annotation).
    tree.TypeParameter,                 # A type parameter in a generic class, interface, method, or constructor.
    tree.VariableDeclaration,           # A variable declaration statement.
    tree.VariableDeclarator,            # A variable declarator in a variable declaration statement.
    tree.VoidClassReference,            # A reference to the void class.
    tree.WhileStatement                 # A while loop statement.                                             
]

metric_dic = {}
metric_num = {}
for node_type in node_types:
    key = str(node_type).split(".")[-1][:-2]
    key = key[:1].lower() + key[1:] + 'Qty'
    metric_dic[node_type] = key
    metric_num[key] = 0
print(metric_num.keys())

def compute_lines(code_snippet):
    if type(code_snippet) == float:
        return 0, 0
    num_comment_lines = 0
    num_code_lines = 0

    in_comment = False

    # Loop through each line of code
    for line in code_snippet.split('\n'):
        line = line.strip()

        # Count comment lines
        if line.startswith('//'):
            num_comment_lines += 1
        elif line.startswith('/*'):
            num_comment_lines += 1
            in_comment = True
        elif line.endswith('*/'):
            num_comment_lines += 1
            in_comment = False
        elif in_comment:
            num_comment_lines += 1
        else:
            num_code_lines += 1
            if '//' in line:  # Check for comments after a statement
                num_comment_lines += 1
                line = line.split('//')[0].strip()  # Remove comments
    return num_code_lines, num_comment_lines

def compute_metrics(code_snippet: str):
    this_metric_num = copy.deepcopy(metric_num)
    try:
        ast = parse.parse('public class A{ public void B(){' + code_snippet + '}}')
        for path, node in ast:
            # print(path)
            # print()
            # print(node)
            # print(type(node))
            # print('-----------------')
            if type(node) in metric_dic.keys():
                key = metric_dic[type(node)]
                this_metric_num[key] += 1
        Isparsed = 1
    except:
        # print('parse error')
        Isparsed = 0
    num_code_lines, num_comment_lines = compute_lines(code_snippet)
    this_metric_num['LOC'] = num_code_lines

    return this_metric_num, list(this_metric_num.values()), Isparsed

def main():
    
    times = []
    for project in projects:
        t = time.time()
        sourceFile = '../code snippets-without-labels/block/'+project+'_blockLevel.csv'
        targetFile = '../metrics/'+project+'-block.csv'
        df = pd.read_csv(sourceFile)
        
        df.drop({'CommentFor', 'CommentsIn', 'CommentsAssociated'}, axis=1, inplace=True)
        tmp = []
        remove = []
        for i in range(len(df)):
            m, _, isparsed = compute_metrics(df['Content'][i])
            tmp.append(m)
            if isparsed == 0:
                remove.append(i)
        metric_df = pd.DataFrame(tmp)
        
        df = df.drop(remove)
        metric_df = metric_df.drop(remove)
        
        df = pd.concat([df, metric_df], axis=1)
        df.drop({'Content'}, axis=1, inplace=True)
        df.to_csv(targetFile, index=False)
        print(project, 'parse errors:', len(remove))
        times.append(time.time() - t)
    with open('time-javalang.txt', 'w') as f:
        for t, project in zip(times, project_names):
            f.write("{}\t{:.2f}\n".format(project, t))
        f.write("Median\t{:.2f}\n".format(np.median(times)))
        f.write("Total\t{:.2f}\n".format(np.sum(times)))

if __name__ == '__main__':
    main()
