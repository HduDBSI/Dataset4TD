package com.hdu.sample;

import java.io.*;
import java.util.ArrayList;

public class MyCSV {
    private File csvFile;
    private String header[] = {"ID", "FilePath", "ClassName","MethodName", "Content", "CommentFor", "CommentsIn", "CommentsAssociated", "StartLine", "EndLine"};
    public MyCSV(String fileName){
        try {
            csvFile = new File(fileName);
            if (!csvFile.exists()){
                csvFile.createNewFile();
            }
        }catch (IOException e){
            System.out.println("error in creating CSVFile");
        }
    }
    public void writeCSVFile(ArrayList<CodeObject> cos){
        int normal_num = 0;
        int no_comments_num = 0;
        int no_content_num = 0;
        int total_num = 0;
        int invalid_className_num = 0;
        int invalid_methodName_num = 0;
        try{
//            BufferedWriter bw = new BufferedWriter (new OutputStreamWriter (new FileOutputStream(csvFile),"UTF-8"));
            FileWriter fw  = new FileWriter(csvFile);
            BufferedWriter bw = new BufferedWriter(fw);
            // write header
            for (int i = 0; i < header.length; i++){
                if (i < header.length-1){
                    bw.append(header[i] + ",");
                }else{
                    bw.append(header[i] + "\r\n");
                }
            }
            // write data
            for(CodeObject co: cos){
                if (co.getFilePath() == null){
                    continue;
                }
                total_num++;
                if (co.getClassName().contains("//")){
                    invalid_className_num++;
                    continue;
                }

                if (co.getMethodName().contains("//")){
                    invalid_methodName_num++;
                    continue;
                }

                if (co.getContent().trim() == ""){
                    no_content_num++;
                    continue;
                }
                if ((co.getCommentFor() == "" && co.getCommentsIn() == "") || co.getCommentsAssociated() == ""){
                    no_comments_num++;
                    continue;
                }

                bw.append(normal_num+",");
                bw.append(co.getFilePath()+",");
                bw.append(CSVFormatter(co.getClassName())+",");
                bw.append(CSVFormatter(co.getMethodName())+",");
                bw.append(CSVFormatter(co.getContent())+",");
                bw.append(CSVFormatter(co.getCommentFor())+",");
                bw.append(CSVFormatter(co.getCommentsIn())+",");
                bw.append(CSVFormatter(co.getCommentsAssociated())+",");
                bw.append(co.getStartLine()+",");
                bw.append(co.getEndLine()+"\r\n");
                normal_num++;
            }
            bw.close();
            fw.close();
            System.out.println("normal:" + normal_num+", " + "total:" + total_num + ", "
                + "noContent:" + no_content_num + ", " + "noComments:" + no_comments_num + ", "
                +  "invalidClassName:" + invalid_className_num + ", " + "invalidMethodName:" + invalid_methodName_num);
//            System.out.print(total_num+",");
        }catch (IOException e){
            System.out.println("error in writing CSVFile");
        }

    }
    public String CSVFormatter(String s){
        if (s == null) {
            return "";
        }
        if (s.contains("\"")) {
            s = s.replaceAll("\"", "\"\"");
        }
        return "\"" + s + "\"";
    }

    public static void main(String[] args){

    }
}
