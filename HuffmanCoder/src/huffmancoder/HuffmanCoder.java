/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package huffmancoder;

import java.io.FileInputStream;

/**
 *
 * @author leonas
 */
public class HuffmanCoder {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        //TODO code application logic here
        //String command = args[0];
        //String filePath = args[1];
        //int K = Integer.parseInt(args[2]);
        String command = "Encode";
        switch (command) {
            case "Encode": {
                //Encoder class
                HuffmanEncoder encoder = new HuffmanEncoder("reikalavimai.txt",8);
                break;
            }
            case "Decode": {
                //Decoder class
                HuffmanDecoder decoder = new HuffmanDecoder("test4");
                break;
            }
            default: {
                System.out.println("Unrecognized command");
                break;
            }
        }

    }
}
//        try(FileInputStream fileInput = new FileInputStream("/home/leonas/Desktop/INFOCODEs/tekstas.txt")) {
//             int K = Integer.parseInt("24");
//             int data;
//             String tail = "";
//             int remaining = 0;
//             int compareTo;
//             String currentWord = "";
//             while ( (data = fileInput.read()) != -1){
//                while ( !tail.isEmpty() ){
//                        if (tail.length() >= K){
//                            currentWord = tail.substring(0, K);
//                            System.out.println("WORD: "+currentWord);
//                            currentWord = "";
//                            tail = tail.substring(K, tail.length());
//                            System.out.println("TAIL: "+tail);
//                        }
//                        else{
//                            currentWord = tail;
//                            System.out.println("PARTIAL WORD: "+currentWord);
//                            remaining = K - tail.length();
//                            tail = "";
//                        }
//                }
//                 String formated = String.format("%8s", Integer.toBinaryString(data)).replace(" ", "0");
//                 System.out.println("READ: "+formated);
//                 compareTo = remaining == 0 ? K : remaining;
//                 if (8 >= compareTo){
//                     currentWord += formated.substring(0, compareTo);
//                     System.out.println("WORD: "+currentWord);
//                     tail = formated.substring(compareTo, 8);
//                     System.out.println("TAIL: "+tail);
//                     currentWord = "";
//                        if (remaining != 0) {
//                            remaining = 0;
//                        }
//                 }
//                 else{
//                    currentWord += formated;
//                    System.out.println("PARTIAL WORD: "+currentWord);
//                    remaining = compareTo - 8;
//                 }
//             }
//             while ( !tail.isEmpty() ){
//                    if(remaining == 0){
//                        if (tail.length() >= K){
//                            currentWord = tail.substring(0, K);
//                            System.out.println("WORD: "+currentWord);
//                            currentWord = "";
//                            tail = tail.substring(K, tail.length());
//                            System.out.println("TAIL: "+tail);
//                        }
//                        else{
//                            currentWord = tail;
//                            System.out.println("PARTIAL WORD: "+currentWord);
//                            remaining = K - tail.length();
//                            tail = "";
//                        }
//                    }
//            }
//            if (!currentWord.isEmpty()){
//                System.out.println("WORD: "+currentWord);
//            }
//             
//         }
//         catch(Exception e){
//             System.out.println("Error message: "+ e.getMessage());
//         }
//    }
//    
//}
