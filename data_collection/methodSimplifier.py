import re

def removePackage(type_with_package: str) -> str:
    """
    Examples:
        type_with_package = 'java.util.List<<java.lang.String>,java.util.Set<java.io.File>>'
        return -> 'List<String>, Set<File>>'
    """
    stack = []
    
    def myPop():
        while stack and stack[-1] not in '<>,?':
            stack.pop()

    for ch in type_with_package:
        # if ch == ' ':
        #     myPop()
        # elif ch == '.':
        #     if stack[-1] == '>':
        #         stack = []
        #     else:
        #         myPop()
        if ch in ' .':
            myPop()
        else:
            stack.append(ch)
    
    return ''.join(stack).replace(',', ', ')

def simplifyMethodSignature1(signature: str) -> str:
    """
    Simplifies a method signature of the form "returnType methodName(paramType1, paramType2, ..., paramTypeN)".
    Returns the method name and parameter types in a more human-readable format.

    Examples:
        signature = 'UserInfo createUserInfoPrompt(@NotNull SSHAuthConfiguration, @NotNull Session)'
        return -> 'createUserInfoPrompt(SSHAuthConfiguration, Session)'

        signature = 'void debug(String, Object...)'
        return -> 'debug(String, Object[])'

        signature = 'java.util.Date scanDate(char)'
        return -> 'scanDate(char)'

        signature = 'void readObject(java.io.ObjectInputStream)'
        return -> 'readObject(ObjectInputStream)'
    """
    # extrac method name and parameters
    pattern = re.compile(r'\s(\w+)\((.*)\)')
    match = pattern.search(signature)
    if not match:
        index = signature.rfind(' ')
        if index == -1:
            return signature
        else:
            return signature[index+1:]
    method_name = match.group(1)
    param_types = match.group(2)

    # deal with parameters
    param_types = re.sub(r'@\w+\s+', '', param_types)    # remove @xxx
    param_types = param_types.replace('...', '[]')       # use [] instead ...
    
    param_types = re.split(r',(?![^<>]*>)', param_types) # use commas that are not within <> for segmentation
    param_types = [removePackage(param_type) for param_type in param_types]
    
    # concat method name and parameter type
    return f'{method_name}({", ".join(param_types)})'

def simplifyMethodSignature2(signature: str) -> str:
    """
    Simplifies a method signature of the form "methodName/paramCount[paramType1,paramType2,...,paramTypeN]".
    Returns the method name and parameter types in a more human-readable format.

    Examples:
        signature = 'createUserInfoPrompt/2[org.jkiss.dbeaver.model.net.ssh.config.SSHAuthConfiguration,org.jkiss.dbeaver.ui.net.ssh.jsch.Session]'
        return -> 'createUserInfoPrompt(SSHAuthConfiguration, Session)'

        signature = 'onCommandDo/1[org.jkiss.dbeaver.model.edit.DBECommand<?>]'
        return -> 'onCommandDo(DBECommand<?>)'

        signature = 'shouldUsePassword/0'
        return -> 'shouldUsePassword()'

        signature = 'fun/2[java.util.List<java.lang.String, java.util.Set<java.io.File>>, GrammarDependencies]'
        return -> 'processGrammarFiles(List<String>, Set<File>, GrammarDependencies, File)'
    
    """
    # match method name, parameter count and parameter type
    pattern = r'^(\w+)/(\d+)\[(.+)\]$'
    match = re.match(pattern, signature)
    if match is None:
        for i in range(len(signature)):
            if signature[i] == '/':
                return signature[:i] + '()'
        return signature + '()'
    method_name = match.group(1)
    param_count = int(match.group(2))
    param_types = match.group(3)

    param_types = re.split(r',(?![^<>]*>)', param_types) # use commas that are not within <> for segmentation
    param_types = [removePackage(param_type) for param_type in param_types]

    # concat method name and parameter type
    return f'{method_name}({", ".join(param_types)})'

def test1():
    dic = {
        'UserInfo createUserInfoPrompt(@NotNull SSHAuthConfiguration, @NotNull Session)': 'createUserInfoPrompt(SSHAuthConfiguration, Session)',
        'void debug(String, Object...)': 'debug(String, Object[])',
        'java.util.Date scanDate(char)': 'scanDate(char)',
        'void readObject(java.io.ObjectInputStream)': 'readObject(ObjectInputStream)',
        'boolean shouldUsePassword(java.util.List<java.lang.String, Object>)': 'shouldUsePassword(List<String, Object>)',
        'Flowable<T> serialize()': 'serialize()',
        'List<? extends T> getKindOfOps(List<? extends RewriteOperation>, Class<T>, int)': 'getKindOfOps(List<?RewriteOperation>, Class<T>, int)',
        'void testUnescaped$InAction()': 'testUnescaped$InAction()'
    }
    for input_str, expected_output in dic.items():
        actual_output = simplifyMethodSignature1(input_str)
        if actual_output != expected_output:
            print(f'input: {input_str}')
            print(f'expect: {expected_output}')
            print(f'real: {actual_output}')

    
def test2():
    dic = {
        'createUserInfoPrompt/2[org.jkiss.dbeaver.model.net.ssh.config.SSHAuthConfiguration,org.jkiss.dbeaver.ui.net.ssh.jsch.Session]': 'createUserInfoPrompt(SSHAuthConfiguration, Session)',
        'onCommandDo/1[org.jkiss.dbeaver.model.edit.DBECommand<?>]': 'onCommandDo(DBECommand<?>)',
        'shouldUsePassword/0': 'shouldUsePassword()',
        'fun/2[java.util.List<java.lang.String>,java.util.Set<java.io.File>, GrammarDependencies]': 'fun(List<String>, Set<File>, GrammarDependencies)',
        'getKindOfOps/3[java.util.List<? extends org.antlr.v4.runtime.TokenStreamRewriter.RewriteOperation>,java.lang.Class<T>,int]': 'getKindOfOps(List<?RewriteOperation>, Class<T>, int)',
        'testUnescaped$InAction/0': 'testUnescaped$InAction()',
        'addObjectRenameActions/1[sql.edit.SQLObjectEditor<OBJECT_TYPE,CONTAINER_TYPE>.ObjectRenameCommand]': 'addObjectRenameActions(ObjectRenameCommand)'
    }
    
    for input_str, expected_output in dic.items():
        actual_output = simplifyMethodSignature2(input_str)
        if actual_output != expected_output:
            print(f'input: {input_str}')
            print(f'expect: {expected_output}')
            print(f'real: {actual_output}')


test1()
test2()

