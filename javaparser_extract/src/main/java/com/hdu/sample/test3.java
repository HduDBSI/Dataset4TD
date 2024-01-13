package com.hdu.sample;

public class test3 {
    private String separator = "[[SEP]]";

    public static void main(String[] args) {
        String list1[] = {"1,,", "2\\/\\", "3:,fg"};
        System.out.println("----原始字符串----");
        for (String ss: list1){
            System.out.println(ss);
        }

        test3 t = new test3(); // 初始化对象
        System.out.println("----拼接后----");
        String s = t.joiner(list1); // 连结字符串
        System.out.println(s);

        System.out.println("----切分后----");
        String list2[] = t.splitter(s);
        for (String ss: list2){
            System.out.println(ss);
        }
        int a = 1;
        String b = null;

        System.out.println("bb:"+a);


    }

    public String[] splitter(String s){
        return s.split("\\[\\[SEP\\]\\]");
    }

    public String joiner(String list[]){
        return String.join(separator, list);
    }
}
