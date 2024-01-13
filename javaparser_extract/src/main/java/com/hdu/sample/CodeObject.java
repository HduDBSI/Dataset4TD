package com.hdu.sample;

public class CodeObject {
    private String filePath;
    private String className = "";
    private String methodName = "";
    private String content = "";
    private String commentFor = "";
    private String commentsIn = "";
    private String commentsAssociated = "";
    private int startLine = 0;
    private int endLine = 0;

    public void setFilePath(String filePath){
        this.filePath = filePath;
    }

    public void setClassName(String className) {
        this.className = className;
    }

    public void setMethodName(String methodName) {
        this.methodName = methodName;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public void setCommentFor(String commentFor) {
        this.commentFor = commentFor;
    }

    public void setCommentsAssociated(String commentsAssociated) {
        this.commentsAssociated = commentsAssociated;
    }

    public void setCommentsIn(String commentsIn) {
        this.commentsIn = commentsIn;
    }

    public void setStartLine(int startLine) {
        this.startLine = startLine;
    }

    public void setEndLine(int endLine) {
        this.endLine = endLine;
    }

    public String getFilePath() {
        return filePath;
    }

    public String getClassName() {
        return className;
    }

    public String getMethodName() {
        return methodName;
    }

    public String getContent() {
        return content;
    }

    public String getCommentFor() {
        return commentFor;
    }

    public String getCommentsIn() {
        return commentsIn;
    }

    public String getCommentsAssociated() {
        return commentsAssociated;
    }

    public int getStartLine() {
        return startLine;
    }

    public int getEndLine() {
        return endLine;
    }
}
