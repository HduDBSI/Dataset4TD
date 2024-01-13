import pandas as pd
import sys
sys.path.append('../')
from project_Info import projects, granularities

seperator = "[[SEP]]"
noLacation = "NoLacation"
encoding = 'utf-8-sig'
def CommentToCodeObject_slow(CodeObjectFile, CommentFile, CodeObjectFileLabeled, level):
    CodeObject = pd.read_csv(CodeObjectFile, encoding=encoding)
    Comment = pd.read_csv(CommentFile, encoding=encoding)
    CodeObject.fillna(' ', inplace=True)

    def makeEmptyList(comments_list):
        codeSnippet_commentLabel = []
        for comments in comments_list:
            size = comments.count(seperator) + 1
            codeSnippet_commentLabel.append([0]*size)
        return codeSnippet_commentLabel

    def fillLabel(locations_list, commentLabel, codeSnippet_commentLabel):
        for i in range(len(locations_list)):
            locations_list[i] = str(locations_list[i])
            lst = locations_list[i].split(";")
            if lst == [noLacation]:
                continue
            for item in lst:
                ID = int(item.split('$')[0])
                No = int(item.split('$')[1])
                codeSnippet_commentLabel[ID][No] = commentLabel[i]
        return codeSnippet_commentLabel

    def list_stringify(lst):
        return [str(item) for item in lst]
    
    def process_column(columnName):
        codeSnippet_commentLabel = makeEmptyList(CodeObject[columnName].tolist())
        codeSnippet_commentLabel = fillLabel(Comment[columnName+level.capitalize()].tolist(), Comment['label'].tolist(), codeSnippet_commentLabel)
        codeSnippetLabel = []
        for i in range(len(codeSnippet_commentLabel)):
            if sum(codeSnippet_commentLabel[i]) > 0:
                codeSnippetLabel.append(1)
            else:
                codeSnippetLabel.append(0)
        return codeSnippetLabel, list_stringify(codeSnippet_commentLabel)

    columns = ["CommentFor", "CommentsIn", "CommentsAssociated"]
    for column in columns:
        codeSnippetLabel, codeSnippet_commentLabel = process_column(column)
        CodeObject['eachLabel'+column] = codeSnippet_commentLabel
        CodeObject[column+'Label'] = codeSnippetLabel

    # CodeObject.drop(['Content', 'CommentFor', 'CommentsIn', 'CommentsAssociated'], axis=1, inplace=True)
    CodeObject.to_csv(CodeObjectFileLabeled, index=False, encoding=encoding)


def removeLine(s:str):
    s = s.replace("\r\n", "")
    s = s.replace("\n", "")
    return s

# faster_one
def CodeObjectToComment_fast(CodeObjectFile, CommentFile):
    CodeObject = pd.read_csv(CodeObjectFile, encoding=encoding)
    CodeObject[['CommentFor', 'CommentsIn', 'CommentsAssociated']] = CodeObject[['CommentFor', 'CommentsIn', 'CommentsAssociated']].apply(removeLine)
    # print(len(CodeObject))

    def constructDF(commentType):
        comment_list, location_list = [], []
        tmp = CodeObject.dropna(subset=[commentType])
        tmp.reset_index(drop=True, inplace=True)

        for i in range(len(tmp)):
            comments = tmp[commentType][i].strip().split(seperator)
            for j in range(len(comments)):
                # comment_list.append(comments[j])
                comment_list.append(removeLine(comments[j]))
                location_list.append(str(tmp['ID'][i])+'$'+str(j))

        return pd.DataFrame({'comment':comment_list, 'location':location_list})

    df_CommentFor, df_CommentsIn, df_CommentsAssociated = constructDF('CommentFor'), constructDF('CommentsIn'), constructDF('CommentsAssociated')

    def merge_locations(locations):
        locations = locations.tolist()
        return ';'.join(locations) if len(locations) > 0 else noLacation

    location_CommentFor = df_CommentFor.groupby('comment')['location'].apply(merge_locations).reset_index(name='location_CommentFor')
    location_CommentsIn = df_CommentsIn.groupby('comment')['location'].apply(merge_locations).reset_index(name='location_CommentsIn')
    location_CommentsAssociated = df_CommentsAssociated.groupby('comment')['location'].apply(merge_locations).reset_index(name='location_CommentsAssociated')
    
    df = pd.merge(location_CommentFor, location_CommentsIn, on='comment', how='outer')
    df = pd.merge(df, location_CommentsAssociated, on='comment', how='outer')
    df.fillna(noLacation, inplace=True)
    df.to_csv(CommentFile, index=False, encoding=encoding)

# run slowly, but easy to read
def CodeObjectToComment_slow(CodeObjectFile, CommentFile):
    CodeObject = pd.read_csv(CodeObjectFile, encoding=encoding)
    print(len(CodeObject))

    def constructDF(commentType):
        comment_list, location_list = [], []
        tmp = CodeObject.dropna(subset=[commentType])
        tmp.reset_index(drop=True, inplace=True)

        for i in range(len(tmp)):
            comments = tmp[commentType][i].strip().split(seperator)
            for j in range(len(comments)):
                comment_list.append(removeLine(comments[j]))
                # comment_list.append(comments[j])
                location_list.append(str(tmp['ID'][i])+'$'+str(j))

        return pd.DataFrame({'comment':comment_list, 'location':location_list})
    
    df_CommentFor, df_CommentsIn, df_CommentsAssociated = constructDF('CommentFor'), constructDF('CommentsIn'), constructDF('CommentsAssociated')

    all_comments = set(df_CommentFor['comment'].tolist()) | set(df_CommentsIn['comment'].to_list()) | set(df_CommentsAssociated['comment'].to_list())
    all_comments = list(all_comments)

    location_CommentFor, location_CommentsIn, location_CommentsAssociated = [], [], []

    for comment in all_comments:
        location1 = df_CommentFor['location'][df_CommentFor['comment'] == comment].tolist()
        location_CommentFor.append(';'.join(location1) if len(location1) > 0 else noLacation)

        location2 = df_CommentsIn['location'][df_CommentsIn['comment'] == comment].tolist()
        location_CommentsIn.append(';'.join(location2) if len(location2) > 0 else noLacation)

        location3 = df_CommentsAssociated['location'][df_CommentsAssociated['comment'] == comment].tolist()
        location_CommentsAssociated.append(';'.join(location3) if len(location3) > 0 else noLacation)
    
    df = pd.DataFrame({
        'comment': all_comments, 
        'location_CommentFor': location_CommentFor, 
        'location_CommentsIn': location_CommentsIn, 
        'location_CommentsAssociated': location_CommentsAssociated
    })
    df.to_csv(CommentFile, index=False, encoding=encoding)
    


# code snippets-without-labels -> comments-without-labels
def split():
    for project in projects:
        for granularity in granularities:
            CodeObjectFile = f'../code snippets-without-labels/{granularity}/{project}_{granularity}Level.csv'
            CommentFile = f'../comments-without-labels/{granularity}/{project}_{granularity}Level_comment.csv'
            CodeObjectToComment_fast(CodeObjectFile, CommentFile)
            print(project+'-'+granularity+' done.')
    
    for project in projects:
        fileCommentFile = f'../comments-without-labels/file/{project}_fileLevel_comment.csv'
        classCommentFile = f'../comments-without-labels/class/{project}_classLevel_comment.csv'
        methodCommentFile = f'../comments-without-labels/method/{project}_methodLevel_comment.csv'
        blockCommentFile = f'../comments-without-labels/block/{project}_blockLevel_comment.csv'
        mergedFile = f'../comments-without-labels/all/{project}_allLevel_comment.csv'
        mergeAllLevel(fileCommentFile, classCommentFile, methodCommentFile, blockCommentFile, mergedFile)
        print(project + ' has been merged.')


def mergeAllLevel(fileCommentFile, classCommentFile, methodCommentFile, blockCommentFile, mergedFile):
    df_file, df_class = pd.read_csv(fileCommentFile, encoding=encoding), pd.read_csv(classCommentFile, encoding=encoding)
    df_method, df_block = pd.read_csv(methodCommentFile, encoding=encoding), pd.read_csv(blockCommentFile, encoding=encoding)

    df_file.rename(columns={'location_CommentFor': 'CommentForFile', 'location_CommentsIn': 'CommentsInFile', 'location_CommentsAssociated': 'CommentsAssociatedFile'}, inplace=True)
    df_class.rename(columns={'location_CommentFor': 'CommentForClass', 'location_CommentsIn': 'CommentsInClass', 'location_CommentsAssociated': 'CommentsAssociatedClass'}, inplace=True)
    df_method.rename(columns={'location_CommentFor': 'CommentForMethod', 'location_CommentsIn': 'CommentsInMethod', 'location_CommentsAssociated': 'CommentsAssociatedMethod'}, inplace=True)
    df_block.rename(columns={'location_CommentFor': 'CommentForBlock', 'location_CommentsIn': 'CommentsInBlock', 'location_CommentsAssociated': 'CommentsAssociatedBlock'}, inplace=True)

    merged = pd.merge(df_file, df_class, on='comment', how='outer')
    merged = pd.merge(merged, df_method, on='comment', how='outer')
    merged = pd.merge(merged, df_block, on='comment', how='outer')

    merged.fillna(noLacation, inplace=True)
    merged.to_csv(mergedFile, index=False, encoding=encoding)


# comments-with-labels -> code snippets-with-labels
def combine():
    for project in projects:
        for granularity in granularities:
            CodeObjectFile = f'../code snippets-without-labels/{granularity}/{project}_{granularity}Level.csv'
            CommentFile = f'../comments-with-labels-checked/Final/{project}_allLevel_comment.csv'
            CodeObjectFileLabeled = f'../code snippets-with-labels/{granularity}/{project}_{granularity}Level.csv'
            CommentToCodeObject_slow(CodeObjectFile, CommentFile, CodeObjectFileLabeled, granularity)
        print(project + ' has been combined.')


# split()
combine()