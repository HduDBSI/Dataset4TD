import com.github.javaparser.ParseProblemException;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.hdu.sample.CodeObject;
import com.sun.istack.internal.NotNull;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Map;

public class testClass {
    public testClass(int a){

    }
    public void say(@NotNull /* */ File file, Object... a, Map<Integer, Map<String,String>> S, ArrayList<?> K) {
        try { // parse a class
            this.cu = StaticJavaParser.parse(file);
        } catch (IOException | ParseProblemException e) {
//            System.out.println("error in:"+file.toString());
            return;
        }
    }

    public void say(File file, int  [] a) {
        try { // parse a class
            this.cu = StaticJavaParser.parse(file);
        } catch (IOException | ParseProblemException e) {
//            System.out.println("error in:"+file.toString());
            return 1;
        }
    }
}