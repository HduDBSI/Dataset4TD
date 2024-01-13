package com.hdu.sample;

import org.apache.commons.io.FileUtils;
import java.io.File;
import java.util.*;

public class Extractor {

    static String baseDirString = "../projects/";
    static String projectList[] = {"antlr4-4.11.0", "dbeaver-22.2.5", "elasticsearch-8.5.2", "exoplayer-2.18.2",
            "fastjson-1.2.83", "flink-1.15.3", "guava-31.1", "jenkins-2.379", "libgdx-1.11.0", "logstash-8.5.2",
            "mockito-4.9.0", "openrefine-3.6.2", "presto-0.278", "quarkus-2.14.0", "questdb-6.6", "redisson-3.18.1",
            "rxjava-3.1.5", "tink-1.7.0"
    };
    static ArrayList<CodeObject> file_list = new ArrayList<>();
    static ArrayList<CodeObject> class_list = new ArrayList<>();
    static ArrayList<CodeObject> method_list = new ArrayList<>();
    static ArrayList<CodeObject> block_list = new ArrayList<>();

    public static void main(String[] args){
        for (String project: projectList){
            File projectDir = new File(baseDirString+project);
            Collection<File> fileCollection = FileUtils.listFiles(projectDir, new String[]{"java"}, true);
            List<File> fileList = new ArrayList<>(fileCollection);
            Collections.sort(fileList, Comparator.comparing(File::getAbsolutePath));

            file_list.clear();
            class_list.clear();
            method_list.clear();
            block_list.clear();
            for (File file: fileList){
                MyComment mc = new MyComment(file);
                file_list.add(mc.getFile());
                class_list.addAll(mc.getClass_());
                method_list.addAll(mc.getMethods());
                block_list.addAll(mc.getBlocks());
            }
//            Collections.sort(file_list, Comparator.comparing(CodeObject::getFilePath));
//            Collections.sort(class_list, Comparator.comparing(CodeObject::getFilePath));
//            Collections.sort(method_list, Comparator.comparing(CodeObject::getFilePath));
//            Collections.sort(class_list, Comparator.comparing(CodeObject::getFilePath));

            new MyCSV("../code snippets-without-labels/file/"+project+"_fileLevel.csv").writeCSVFile(file_list);
            new MyCSV("../code snippets-without-labels/class/"+project+"_classLevel.csv").writeCSVFile(class_list);
            new MyCSV("../code snippets-without-labels/method/"+project+"_methodLevel.csv").writeCSVFile(method_list);
            new MyCSV("../code snippets-without-labels/block/"+project+"_blockLevel.csv").writeCSVFile(block_list);

            System.out.println(project+" has been extracted.");
            System.out.println(" ");
        }
    }
}
