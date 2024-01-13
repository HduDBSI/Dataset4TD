package com.hdu.sample;

/*
 * comment 1
*/
public class GreetingApp{
    // comment 2
    public static void main(String[] args){
        /* comment 3*/
        Greeting greeting = new Greeting("Hello!");
        if (true){
            greeting.greet();
        }
    }
}

// comment 4
class Greeting{
    private String message;
    public Greeting(String message){ this.message = message; }
    public void greet(){ System.out.println(message); }
}

