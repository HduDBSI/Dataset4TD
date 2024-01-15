from javalang import parse, tree

def compute_metrics(code: str):
    DeclNbr, ExprStmtNbr = 0, 0
    try:
        ast = parse.parse('public class A{' + code + '}')
        for _, node in ast:
            if type(node) == tree.VariableDeclaration:
                DeclNbr += 1
            elif type(node) == tree.StatementExpression:
                ExprStmtNbr += 1
    except:
        # print('parse error')
        pass
    return f'{DeclNbr},{ExprStmtNbr}'