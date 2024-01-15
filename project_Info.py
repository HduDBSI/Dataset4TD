project_names = [
    "ANTLR4",
    "DBeaver",
    "Elasticsearch",
    "ExoPlayer",
    "FastJSON",
    "Flink",
    "Guava",
    "Jenkins",
    "LibGDX",
    "Logstash",
    "Mockito",
    "OpenRefine",
    "Presto",
    "Quarkus",
    "QuestDB",
    "Redisson",
    "RxJava",
    "Tink"
]

# data below is obtained from 'javaparser_extract'
file_num = [518, 4742, 14234, 1493, 3121, 13198, 3039, 1716, 2317, 523, 957, 1031, 7964, 13052, 2537, 2151, 1883, 634]

class_num = [585, 5565, 18995, 2355, 5685, 20363, 6850, 3299, 3033, 681, 1682, 1207, 10014, 17114, 3492, 2424, 3008, 853]

method_num = [3705, 36469, 114135, 18496, 20187, 100994, 49181, 15361, 41115, 3575, 5728, 5261, 67558, 59449, 30736, 24849, 22116, 5226]

block_num = [11908, 73292, 403576, 65972, 49950, 284028, 131166, 46292, 73596, 9534, 13054, 16294, 187289, 132744, 61911, 59711, 72073, 20943]

all_num = [[file_num[i], class_num[i], method_num[i], block_num[i]] for i in range(len(project_names))]

projects = [
    "antlr4-4.11.0", "dbeaver-22.2.5", "elasticsearch-8.5.2", "exoplayer-2.18.2",
    "fastjson-1.2.83", "flink-1.15.3", "guava-31.1", "jenkins-2.379", "libgdx-1.11.0", 
    "logstash-8.5.2", "mockito-4.9.0", "openrefine-3.6.2", "presto-0.278", 
    "quarkus-2.14.0", "questdb-6.6", "redisson-3.18.1", "rxjava-3.1.5", "tink-1.7.0"
]

granularities = ['file', 'class', 'method', 'block']

# 49 metrics
class_feature_names = [
    'CBO', 'CBOModified', 'Fanin', 'Fanout',
    
    'DIT', 'NOC', 
    
    'LCC', 'LCOM', 'LCOM*', 'TCC',
    
    'RFC', 'WMC', 'maxNestedBlocksQty',  
    
    'LOC', 'NOSI', 
    'anonymousClassesQty', 'innerClassesQty',
    'defaultFieldsQty', 'finalFieldsQty', 'privateFieldsQty', 'protectedFieldsQty', 'publicFieldsQty', 'staticFieldsQty', 'synchronizedFieldsQty', 'totalFieldsQty',
    'abstractMethodsQty', 'defaultMethodsQty', 'finalMethodsQty', 'privateMethodsQty', 'protectedMethodsQty', 'publicMethodsQty', 'synchronizedMethodsQty', 'staticMethodsQty', 'totalMethodsQty',
    'modifiers',
    'uniqueWordsQty',
    'variablesQty',
    'visibleMethodsQty', 

    'comparisonsQty', 'lambdasQty', 'mathOperationsQty', 'numbersQty', 'parenthesizedExpsQty', 'stringLiteralsQty',
    
    'assignmentsQty', 'logStatementsQty', 'loopQty', 'returnQty', 'tryCatchQty',
]

file_feature_names = class_feature_names

# 29 metrics
method_feature_names = [
    'CBO', 'CBOModified', 'Fanin', 'Fanout',  # 4

    'RFC', 'WMC', 'hasJavaDoc', 'maxNestedBlocksQty', 'parametersQty', # 5
    
    'LOC', 
    'anonymousClassesQty', 'innerClassesQty',
    'modifiers',
    'uniqueWordsQty',
    'variablesQty', #6

    'methodsInvokedQty', 'methodsInvokedLocalQty', 'methodsInvokedIndirectLocalQty', #9
    'comparisonsQty', 'lambdasQty', 'mathOperationsQty', 'numbersQty', 'parenthesizedExpsQty', 'stringLiteralsQty',

    'assignmentsQty', 'logStatementsQty', 'loopQty', 'returnsQty', 'tryCatchQty', #5
]

# 47 metrics
block_feature_names = [
    'annotationQty',
    'basicTypeQty',
    'referenceTypeQty', # 3

    'arrayCreatorQty',
    'arrayInitializerQty',
    'arraySelectorQty', # 3

    'fieldDeclarationQty',
    'formalParameterQty',
    'inferredFormalParameterQty',
    'methodDeclarationQty',
    'localVariableDeclarationQty',
    'variableDeclarationQty',
    'variableDeclaratorQty', # 7

    'assignmentQty',
    'binaryOperationQty',
    'castQty',
    'classCreatorQty',
    'classReferenceQty',
    'lambdaExpressionQty',
    'literalQty',
    'memberReferenceQty',
    'methodInvocationQty',
    'methodReferenceQty',
    'superMethodInvocationQty',
    'ternaryExpressionQty',
    'thisQty',
    'typeArgumentQty',
    'voidClassReferenceQty',   # 15

    'assertStatementQty',
    'blockStatementQty',
    'breakStatementQty',
    'catchClauseQty',
    'continueStatementQty',
    'doStatementQty',
    'enhancedForControlQty',
    'forControlQty',
    'forStatementQty',
    'ifStatementQty',
    'returnStatementQty',
    'statementExpressionQty',
    'switchStatementQty',
    'switchStatementCaseQty',
    'synchronizedStatementQty',
    'throwStatementQty',
    'tryResourceQty',
    'tryStatementQty',
    'whileStatementQty',
    'LOC'                      # 20 

    # 'annotationDeclarationQty',
    # 'annotationMethodQty',
    # 'catchClauseParameterQty',
    # 'classDeclarationQty',
    # 'compilationUnitQty',
    # 'constantDeclarationQty',
    # 'constructorDeclarationQty',
    # 'creatorQty',
    # 'declarationQty',
    # 'documentedQty',
    # 'elementArrayValueQty',
    # 'elementValuePairQty',
    # 'enumBodyQty',
    # 'enumConstantDeclarationQty',
    # 'enumDeclarationQty',
    # 'explicitConstructorInvocationQty',
    # 'expressionQty',
    # 'importQty',
    # 'innerClassCreatorQty',
    # 'interfaceDeclarationQty',
    # 'invocationQty',
    # 'memberQty',
    # 'nodeQty',
    # 'packageDeclarationQty',
    # 'primaryQty',
    # 'statementQty',
    # 'superConstructorInvocationQty',
    # 'superMemberReferenceQty',
    # 'typeQty',
    # 'typeDeclarationQty',
    # 'typeParameterQty',
]

file_feature_names_lowercase = [s.lower() for s in file_feature_names]
class_feature_names_lowercase = [s.lower() for s in class_feature_names]
method_feature_names_lowercase = [s.lower() for s in method_feature_names]
block_feature_names_lowercase = [s.lower() for s in block_feature_names]
