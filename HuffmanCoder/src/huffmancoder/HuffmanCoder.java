/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package huffmancoder;

/**
 *
 * @author leonas
 */
public class HuffmanCoder {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
//        String command = args[0];
//        String filePath = args[1];
//        int K = Integer.parseInt(args[2]);
        String command = "Encode";
        switch (command) {
            case "Encode": {
                //Encoder class
                HuffmanEncoder encoder = new HuffmanEncoder("foto.png",8);
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
