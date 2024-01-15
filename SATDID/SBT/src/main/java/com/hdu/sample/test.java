package com.hdu.sample;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Modifier;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.expr.SimpleName;
import com.github.javaparser.ast.type.ClassOrInterfaceType;

import java.util.ArrayList;
import java.util.List;

public class test {

    public static void main(String[] args) {
        String code = "public class Test {\n" +
                "    public String extractFor(Integer id){\n" +
                "        LOG.debug(\"Extracting method with ID:{}\", id);\n" +
                "        return requests.remove(id);\n" +
                "    }" +
                "}";
        SBT sbt = new SBT(code);
        System.out.println(sbt.getSequence());
    }
}
