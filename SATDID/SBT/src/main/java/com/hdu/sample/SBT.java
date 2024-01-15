package com.hdu.sample;

import com.github.javaparser.ParseResult;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Modifier;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.comments.Comment;
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import org.apache.commons.io.FileUtils;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.*;

public class SBT {
    private String sequence;

    public SBT (String code) {
        try{
            CompilationUnit cu = StaticJavaParser.parse(code);
            Node root = cu.getChildNodes().get(0);
            ArrayList<String> seq_list = Structure_base_Traversal(root);
            this.sequence = String.join(" ", seq_list).replaceAll("[\r\n]", "");
        } catch (Exception e) {
            this.sequence = "PARSE ERROR";
        }
    }

    public String getSequence() {
        return sequence;
    }

    private ArrayList<String> Structure_base_Traversal(Node node){
        ArrayList<String> seq_list = new ArrayList<>();
        List<Node> children = node.getChildNodes();

        String node_full_name = getNodeFullName(node);
        seq_list.add("(");
        seq_list.add(node_full_name);

        if (children.isEmpty()){
            seq_list.add(")");
            seq_list.add(node_full_name);
        } else {
            for (Node child: children){
                if (child instanceof Comment) {
                    continue;
                }
                seq_list.addAll(Structure_base_Traversal(child));
            }
            seq_list.add(")");
            seq_list.add(node_full_name);
        }
        return seq_list;
    }

    private String getNodeFullName(Node node){
        String node_class = ((Object) node).getClass().getSimpleName();
        String node_name;
        if (node instanceof Modifier){
            node_name = node.toString();
        } else if (node instanceof MethodDeclaration){
            node_name = ((MethodDeclaration) node).getType() + "_" + ((MethodDeclaration) node).getName().toString();
        } else if (node instanceof ClassOrInterfaceDeclaration){
            node_name = ((ClassOrInterfaceDeclaration) node).getName().toString();
        } else if (node instanceof SimpleName) {
            node_name = ((SimpleName) node).getIdentifier();
        } else if (node instanceof Parameter) {
            node_name = ((Parameter) node).getType() + "_" + ((Parameter)node).getName();
        } else if (node instanceof ClassOrInterfaceType) {
            node_name = ((ClassOrInterfaceType) node).getName().toString();
        } else if (node instanceof NameExpr) {
            node_name = ((NameExpr) node).getName().toString();
        } else if (node instanceof MethodCallExpr) {
            node_name = ((MethodCallExpr) node).getName().toString();
        } else if (node instanceof BooleanLiteralExpr) {
            node_name = String.valueOf(((BooleanLiteralExpr) node).getValue());
        } else if (node instanceof IntegerLiteralExpr || node instanceof DoubleLiteralExpr) {
            return "<NUM>";
        } else if (node instanceof StringLiteralExpr || node instanceof CharLiteralExpr) {
            return "<STR>";
        } else {
            node_name = "null";
        }
        String full_name = node_class + "_" + node_name;
        return full_name.replaceAll("[\\s/]", "");
    }

    public static String CSVFormatter(String s){
        if (s == null) {
            return "";
        }
        if (s.contains("\"")) {
            s = s.replaceAll("\"", "\"\"");
        }
        return "\"" + s + "\"";
    }

    public static void main(String[] args) {
        String base_dir = args[0];
        String output_file = args[1];
//        String base_dir = "../data/java_files/antlr4-4.11.0";
//        String output_file = "a.csv";
        File base_path = new File(base_dir);
        Collection<File> fileCollection = FileUtils.listFiles(base_path, new String[]{"java"}, true);

        String remove_str1 = "( ClassOrInterfaceDeclaration_A ( Modifier_public ) Modifier_public ( SimpleName_A ) SimpleName_A ( MethodDeclaration_void_B ( Modifier_public ) Modifier_public ( SimpleName_B ) SimpleName_B ( VoidType_null ) VoidType_null ";
        String remove_str2 = " ) MethodDeclaration_void_B ) ClassOrInterfaceDeclaration_A";

        File csvFile = null;
        try {
            csvFile = new File(output_file);
            if (!csvFile.exists()){
                csvFile.createNewFile();
            }
        } catch (IOException e){
            System.out.println("error in creating CSVFile");
        }
        try {
            FileWriter fw  = new FileWriter(csvFile);
            BufferedWriter bw = new BufferedWriter(fw);
            bw.append("ID" + "," + "label" + "," + "seq" + "\r\n");
            for (File file : fileCollection) {
                String[] parts = file.getName().split("_");
                String id = parts[0].replace("Test", "");
                String label = parts[1].replace(".java", "");

                byte[] fileBytes = Files.readAllBytes(file.toPath());
                String code = new String(fileBytes);
                String seq = new SBT(code).getSequence();
                seq = seq.replace(remove_str1, "").replace(remove_str2, "");

                bw.append(id + "," + label + "," + CSVFormatter(seq) + "\r\n");
            }
            bw.close();
            fw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
