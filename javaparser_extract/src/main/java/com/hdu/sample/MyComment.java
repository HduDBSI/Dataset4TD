package com.hdu.sample;

import com.github.javaparser.ParseProblemException;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.comments.Comment;
import com.github.javaparser.ast.stmt.Statement;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

// all comment for a java file
public class MyComment {
    private CodeObject file = new CodeObject();
    private ArrayList<CodeObject> classes = new ArrayList<>();
    private ArrayList<CodeObject> methods = new ArrayList<>();
    private ArrayList<CodeObject> blocks = new ArrayList<>();
    private CompilationUnit cu;
    private String filePath;

    public MyComment(File file){
        try { // parse a class
            this.cu = StaticJavaParser.parse(file);
        }catch (IOException | ParseProblemException e){
//            System.out.println("error in:"+file.toString());
            return;
        }
        this.filePath = file.toString();
        this.setComment();
    }

    public CodeObject getFile() { return file; }

    public ArrayList<CodeObject> getClass_() {
        return classes;
    }

    public ArrayList<CodeObject> getMethods() {
        return methods;
    }

    public ArrayList<CodeObject> getBlocks() {
        return blocks;
    }

    public void setComment(){
        file.setFilePath(filePath);
        file.setClassName("FileDoesNotHaveClassName");
        file.setMethodName("FileDoesNotHaveMethodName");
        file.setContent(cu.toString());
        if (cu.getComment().isPresent()) file.setCommentFor(cu.getComment().get().toString());
        cu.getComment().ifPresent(comment -> file.setCommentFor(comment.toString()));
        file.setCommentsIn(commentJoiner(cu.getAllContainedComments(), file.getCommentFor()));
        file.setCommentsAssociated(new MyJoinner(file.getContent()).getTotalComment());
        file.setStartLine(cu.getBegin().get().line);
        file.setEndLine(cu.getEnd().get().line);

        for (ClassOrInterfaceDeclaration coid: cu.findAll(ClassOrInterfaceDeclaration.class)) {
            CodeObject class_ = new CodeObject();
            class_.setFilePath(filePath);
            if (coid.getFullyQualifiedName().isPresent()) class_.setClassName(coid.getFullyQualifiedName().get());
            else class_.setClassName(coid.getName().toString());
            class_.setMethodName("ClassDoesNotHaveMethodName");
            class_.setContent(coid.toString());
            if (coid.getComment().isPresent()) class_.setCommentFor(coid.getComment().get().toString());
//            else class_.setCommentFor("NoCommentFor");
            class_.setCommentsIn(commentJoiner(coid.getAllContainedComments(), class_.getCommentFor()));
            class_.setCommentsAssociated(new MyJoinner(class_.getContent()).getTotalComment());
            class_.setStartLine(coid.getBegin().get().line);
            class_.setEndLine(coid.getEnd().get().line);
            classes.add(class_);

            for (MethodDeclaration md: coid.getMethods()) {
                CodeObject method = new CodeObject();
                method.setFilePath(filePath);
                method.setClassName(class_.getClassName());
                method.setMethodName(md.clone().getDeclarationAsString(false, false, false));
//                method.setMethodName(md.getName().toString());
                method.setContent(md.toString());
                if (md.getComment().isPresent()) method.setCommentFor(md.getComment().get().toString());
//                else method.setCommentFor("NoCommentFor");
                method.setCommentsIn(commentJoiner(md.getAllContainedComments(), method.getCommentFor()));
                method.setCommentsAssociated(new MyJoinner(method.getContent()).getTotalComment());
                method.setStartLine(md.getBegin().get().line);
                method.setEndLine(md.getEnd().get().line);
                methods.add(method);

                if (!md.getBody().isPresent()){
                    continue;
                }
                for (Statement s: md.getBody().get().findAll(Statement.class, Node.TreeTraversal.DIRECT_CHILDREN)){
                    CodeObject block = new CodeObject();
                    block.setFilePath(filePath);
                    block.setClassName(class_.getClassName());
                    block.setMethodName(method.getMethodName());
                    block.setContent(s.toString());
                    if (s.getComment().isPresent()) block.setCommentFor(s.getComment().get().toString());
//                    else block.setCommentFor("NoCommentFor");
                    block.setCommentsIn(commentJoiner(s.getAllContainedComments(), block.getCommentFor()));
                    block.setCommentsAssociated(new MyJoinner(block.getContent()).getTotalComment());
                    block.setStartLine(s.getBegin().get().line);
                    block.setEndLine(s.getEnd().get().line);
                    blocks.add(block);
                }

            }
        }

//        List<ClassOrInterfaceDeclaration> coids = cu.findAll(ClassOrInterfaceDeclaration.class);
//        for (ClassOrInterfaceDeclaration coid: coids){
//            CodeObject class_ = new CodeObject();
//
//            class_.setFilePath(filePath);
//            class_.setClassName(coid.getName().toString());
//            class_.setContent(coid.toString());
//            if (coid.getComment().isPresent()){
//                class_.setCommentFor(coid.getComment().get().toString());
//            }
//            class_.setCommentsIn(commentJoiner(coid.getAllContainedComments(), class_.getCommentFor()));
//            class_.setCommentsAssociated(new MyJoinner(class_.getContent()).getTotalComment());
//            this.classes.add(class_);
//
//            List<MethodDeclaration> mds = coid.getMethods();
//            for (MethodDeclaration md: mds){
//                CodeObject method = new CodeObject();
//
//                method.setFilePath(filePath);
//                method.setClassName(coid.getName().toString());
//                method.setMethodName(md.getName().toString());
//                method.setContent(md.toString());
//                if (md.getComment().isPresent()){ // has comment
//                    method.setCommentFor(md.getComment().get().toString());
//                }
//                method.setCommentsIn(commentJoiner(md.getAllContainedComments(), method.getCommentFor()));
//                method.setCommentsAssociated(new MyJoinner(method.getContent()).getTotalComment());
//                this.methods.add(method);
//
//                if (md.getBody().isPresent()){
//                    List<Statement> ss = md.getBody().get().findAll(Statement.class, Node.TreeTraversal.DIRECT_CHILDREN);
//                    for (Statement s: ss){
//                        CodeObject block = new CodeObject();
//
//                        block.setFilePath(filePath);
//                        block.setMethodName(md.getName().toString());
//                        block.setContent(s.toString());
//                        if (s.getComment().isPresent()){
//                            block.setCommentFor(s.getComment().get().toString());
//                        }
//                        block.setCommentsIn(commentJoiner(s.getAllContainedComments(), block.getCommentFor()));
//                        block.setCommentsAssociated(new MyJoinner(block.getContent()).getTotalComment());
//                        blocks.add(block);
//                    }
//                }
//            }
//        }




    }

    public static String commentJoiner(List<Comment> comments){
        String joiner = "";
        String separator = "[[SEP]]";
        for (Comment comment: comments){
            joiner += comment.toString() + separator;
        }
        if (joiner.length() > 0){
            joiner = joiner.substring(0, joiner.length() - separator.length());
        }
        return joiner;
    }

    public static String commentJoiner(List<Comment> comments, String removeComment){
        String joiner = "";
        String separator = "[[SEP]]";
        for (Comment comment: comments){
            if (!removeComment.equals(comment.toString())){
                joiner += comment.toString() + "[[SEP]]";
            }
        }
        if (joiner.length() > 0){
            joiner = joiner.substring(0, joiner.length() - separator.length());
        }
        return joiner;
    }

}
