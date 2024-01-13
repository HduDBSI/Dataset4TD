package com.hdu.sample;

import com.github.javaparser.JavaParser;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.comments.BlockComment;
import com.github.javaparser.ast.comments.Comment;
import com.github.javaparser.ast.stmt.Statement;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Predicate;

public class test {
    public static void main(String[] args) {
        methodTest();
    }
    static void classTest() {
        File file = new File("src\\main\\resources\\Nullable.java");
        CompilationUnit cu;
        try{
            cu = StaticJavaParser.parse(file);
        }catch (IOException e){
            System.out.println(e);
            return;
        }

        System.out.println("========classContent=========");
        String classContent = cu.toString();
        System.out.println(classContent);

        System.out.println("========commentFor=========");
        String commentFor = "";
//        if (cu.getChildNodes().get(0).getComment().isPresent())
//            commentFor = cu.getChildNodes().get(0).getComment().get().toString();
//        System.out.println();
//        List <Node> nodes = cu.getChildNodes();
//        for (Node n: nodes){
//            n.
//        }
        List<ClassOrInterfaceDeclaration> coids = cu.findAll(ClassOrInterfaceDeclaration.class);
        if (!coids.isEmpty()){
            commentFor = coids.get(0).getComment().get().toString();
        }

        System.out.println(commentFor);

        System.out.println("========commentsIn=========");
        List<Comment> commentsInMethod = cu.getAllContainedComments();
        for (Comment comment: commentsInMethod){
            if (!comment.toString().equals(commentFor))
                System.out.println(comment);
        }

//        System.out.println("========orphanComments=========");
//        String orphanComments = cu.getChildNodes().get(0).getOrphanComments().toString();
//        System.out.println(orphanComments);

    }
    static void methodTest() {
        File file = new File("src/main/resources/testClass.java");
        CompilationUnit cu;
        try{
            cu = StaticJavaParser.parse(file);
        }catch (IOException e){
            System.out.println(e);
            return;
        }

        List<MethodDeclaration> mds = cu.findAll(MethodDeclaration.class);
        for (MethodDeclaration md: mds){
            System.out.println(md.getDeclarationAsString(false, false, false));
            System.out.println(md.getParameters());
//            System.out.println(md.getDeclarationAsString());
//            System.out.println(md.);
//            System.out.println("========methodContent=========");
//            String methodContent = md.toString();
//            System.out.println(methodContent);
//
//            System.out.println("========commentForMethod=========");
//            String commentForMethod = md.getComment().get().toString();
//            System.out.println(commentForMethod);
//
//            System.out.println("========commentsInMethod=========");
//            List<Comment> commentsInMethod = md.getAllContainedComments();
//            for (Comment comment: commentsInMethod){
//                System.out.println(comment.toString());
//            }

//            System.out.println("========orphanComments=========");
//            String orphanComments = md.getParentNode().get().getOrphanComments().toString();
//            System.out.println(orphanComments);
        }
    }
    static void blockTest() {
        File file = new File("src/main/resources/test1.java");
        CompilationUnit cu;
        try{
            cu = StaticJavaParser.parse(file);
        }catch (IOException e){
            System.out.println(e);
            return;
        }
        MethodDeclaration md = cu.findFirst(MethodDeclaration.class).get();
        List<Statement> ss = md.getBody().get().findAll(Statement.class, Node.TreeTraversal.DIRECT_CHILDREN);
        for (Statement s: ss){
            System.out.println("========statementContent=========");
            String statementContent = s.toString();
            System.out.println(statementContent);

            System.out.println("========commentForStatement=========");
            s.getComment().ifPresent(comment -> System.out.println(comment.toString()));
        }

    }
    static void testTogether(){
        File file = new File("src/main/resources/test1.java");
        CompilationUnit cu;
        try{
            cu = StaticJavaParser.parse(file);
        }catch (IOException e){
            System.out.println(e);
            return;
        }
        List<MethodDeclaration> mds = cu.findAll(MethodDeclaration.class);
        for (MethodDeclaration md: mds){
            System.out.println("========methodContent=========");
            String methodContent = md.toString();
            System.out.println(methodContent);

            System.out.println("========commentForMethod=========");
            String commentForMethod = md.getComment().get().toString();
            System.out.println(commentForMethod);

            System.out.println("========commentsInMethod=========");
            List<Comment> commentsInMethod = md.getAllContainedComments();
            for (Comment comment: commentsInMethod){
                System.out.println(comment.toString());
            }



        }
    }
    static CodeObject getMethodComment(MethodDeclaration  md, String filePath){
        CodeObject method = new CodeObject();

        method.setFilePath(filePath);
        method.setMethodName(md.getName().toString());
        method.setContent(md.toString());
        if (md.getComment().isPresent()){
            method.setCommentFor(md.getComment().get().toString());
        }

        System.out.println("========commentsInMethod=========");
        List<Comment> commentsInMethod = md.getAllContainedComments();
        for (Comment comment: commentsInMethod){
            System.out.println(comment.toString());
        }
        return method;
    }
    static void test(){
        CompilationUnit cu = StaticJavaParser.parse("public class test1 {\n" +
                "    public void method1(String   name) {\n" +
                "        String a = \"1\"; // comment for statement\n" +
                "        \n" +
                "        int b = 2;\n" +
                "        // comment for if-else block\n" +
                "        if(b == 1){\n" +
                "            b = 2;\n" +
                "        }else{\n" +
                "            b = 3;\n" +
                "        }\n" +
                "        \n" +
                "        /*\n" +
                "            comment for loop block\n" +
                "         */\n" +
                "        for(int i = 0; i < 10; i++) {\n" +
                "            i = i+1;\n" +
                "        }\n" +
                "    }\n" +
                "}");
        List<Statement> ss = cu.findAll(Statement.class, Node.TreeTraversal.POSTORDER);
        for (Statement s: ss){
            System.out.println("========statementContent=========");
            String statementContent = s.toString();
            System.out.println(statementContent);

            System.out.println("========commentForStatement=========");
            String commentForStatement = s.getComment().get().toString();
            System.out.println(commentForStatement);
        }
    }
}
