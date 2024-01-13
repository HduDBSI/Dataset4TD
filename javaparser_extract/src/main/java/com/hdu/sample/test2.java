package com.hdu.sample;

import org.apache.commons.io.FileUtils;
import java.io.File;
import java.util.ArrayList;
import java.util.Collection;

public class test2 {
    public static void main(String[] args) {
        ArrayList<CodeObject> methods = new ArrayList<>();
        File projectDir = new File("E:/DownLoad/projects/emf-2.4.1");
        Collection<File> files = FileUtils.listFiles(projectDir, new String[]{"java"}, true);
        for (File file: files){
            MyComment mc = new MyComment(file);
            methods.addAll(mc.getMethods());
        }
        long startTime = System.currentTimeMillis();
        String header[] = {"FilePath", "MethodName", "Content"};
        MyCSV m = new MyCSV("a.csv");
        m.writeCSVFile(methods);
        long endTime = System.currentTimeMillis();
        System.out.println("mycsv运行时间：" + (endTime - startTime) + "ms");
    }
}
