package com.hdu.sample;

import java.util.ArrayList;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class CommentStack extends Stack<String>{
    @Override
    public String push(String comment){
        if (this.isEmpty()){
            return super.push(comment);
        } else {
            String firstComment = this.get(0);
            firstComment += comment;
            this.set(0, firstComment);
            return comment;
        }
    }
}
public class MyJoinner {

    private String[] lines;
    private ArrayList<String> comments = new ArrayList<>();
    private ArrayList<Integer> lineNum = new ArrayList<>();
    private String totalComment = "";

    public MyJoinner(String JavaCode){
        setLines(JavaCode);
        setComments(JavaCode);
        if (comments.isEmpty()){
            return;
        }
        setLineNum();
        commentJoiner();
        setTotalComment();
    }

    public String getTotalComment(){ return totalComment;}

    private void setTotalComment(){
        this.totalComment = String.join("[[SEP]]", this.comments);
    }

    private void setLines(String JavaCode){
        this.lines = JavaCode.split("\r\n|\r|\n");
    }

    private void setComments(String JavaCode){
        Pattern p = Pattern.compile("(//.*?$|/\\*.*?\\*/)", Pattern.MULTILINE | Pattern.DOTALL);
        Matcher m = p.matcher(JavaCode);
        while (m.find()) {
            this.comments.add(m.group());
        }
    }

    private boolean isOccupyASingleLine(String comment, int lineNumber) {
        String line = lines[lineNumber-1].trim();
        return line.equals(comment);
    }

    private void commentJoiner(){
        ArrayList<String> newComments = new ArrayList<>();
        CommentStack cs = new CommentStack();
        int lineNum = -1;
        for (int i = 0; i < this.comments.size(); i++){
            String current_comment = this.comments.get(i).trim();
            int current_lineNum = this.lineNum.get(i);
            boolean isOccupying = isOccupyASingleLine(current_comment, current_lineNum);
            boolean isLineComment = current_comment.startsWith("//");

            if ((isLineComment && !isOccupying) || !isLineComment){
                if (!cs.empty()){
                    newComments.add(cs.pop().replaceAll("[\n\r]", ""));
                }
                newComments.add(current_comment.replaceAll("[\n\r]", ""));
            }
            if (isLineComment && isOccupying){
                if (current_lineNum != lineNum + 1 && !cs.isEmpty()){
                    newComments.add(cs.pop().replaceAll("[\n\r]", ""));
                }
                cs.push(current_comment);
            }

            lineNum = current_lineNum; //update
        }
        if (!cs.empty()){
            newComments.add(cs.pop().replaceAll("[\n\r]", ""));
        }
        comments = newComments;
    }
    private String getFirstLine(String s){
        int index = s.indexOf("\n");
        if (index == -1){
            return s;
        }else{
            return s.substring(0, index);
        }
    }
    private int getNumberOfLine(String s){
        return s.split("\r\n|\r|\n").length;
    }

    private int searchLineNum(String comment, int startLine){
        String firstLine = getFirstLine(comment);
        for (int i = startLine; i < lines.length; i++){
            if (lines[i].contains(firstLine)){
                return i+1;
            }
        }
        return 0;
    }

    private void setLineNum(){
        int startLine = 0;
        for (String comment : comments){
            int commentLine = searchLineNum(comment, startLine);
            lineNum.add(commentLine);
            if (commentLine == 0){
                startLine = startLine + getNumberOfLine(comment);
            } else {
                startLine = commentLine - 1 + getNumberOfLine(comment);
            }

        }

        ArrayList<Integer> indexesOfZero = new ArrayList<>();
        for (int i = 0; i < lineNum.size(); i++) {
            if (lineNum.get(i) == 0) {
                indexesOfZero.add(i);
            }
        }

        for (int i = indexesOfZero.size() - 1; i >= 0; i--) {
            int index = indexesOfZero.get(i);
            comments.remove(index);
            lineNum.remove(index);
        }

    }

    // for test
    public static void main(String[] args) {
        MyJoinner mj;
        String code1 = "// Ensure that the output directory path is all in tact so that\n" +
            "// ANTLR can just write into it.\n"+
            "// \n"+
        "File outputDir = getOutputDirectory();//fff\n";
        mj = new MyJoinner(code1);
        System.out.println(mj.getTotalComment());

        String code2 = "// This is a single-line comment\n" +
                "public class Main {\n" +
                "    /* This is a\n" +
                "       multi-line\n" +
                "       comment */\n" +
                "    public static void main(String[] args) {\n" +
                "        System.out.println(\"Hello, world!\"); // This is another single-line comment\n" +
                "    }\n" +
                "}";
        mj = new MyJoinner(code2);
        System.out.println(mj.getTotalComment());
    }
}

