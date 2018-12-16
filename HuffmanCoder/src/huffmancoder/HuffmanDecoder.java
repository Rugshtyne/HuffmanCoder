/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package huffmancoder;

import huffmancoder.entities.Node;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.InputStream;

/**
 *
 * @author Vilys
 */
public class HuffmanDecoder {
    
    int K;
    String seqToDecode;
    
    public HuffmanDecoder(String fileToRead) {
        File file = new File(fileToRead);
        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            while(br.ready()) {
                line = br.readLine();
                if (line.matches("\\|\\d*\\|")) {
                    K = Integer.parseInt(line.replace("|", ""));
                    //System.out.println(K);
                }
                else {
                    this.seqToDecode = line;
                    Node root = ReadTree();
                    int length = line.replace("0", "").replace("1", "").replace("true", "1").replace("false", "1").length();
                    this.seqToDecode = line.replace("0", "").replace("1", "");
                    for(int i = 0; i < length; i ++) {
                        //
                        Node node = root;
                        while (!node.checkIfLeaf()) {
                            boolean isLeaf = false;
                            if(this.seqToDecode.startsWith("true")) {
                                isLeaf = true;
                                this.seqToDecode = this.seqToDecode.substring(4);
                            }
                            else if(this.seqToDecode.startsWith("false")) {
                                isLeaf = false;
                                this.seqToDecode = this.seqToDecode.substring(5);
                            }
                            else {
                                if(this.seqToDecode.length() > 0) this.seqToDecode = this.seqToDecode.substring(K);
                            }
                            if(isLeaf) node = node.getRight();
                            else node = node.getLeft();
                        }
                        System.out.println((char)Integer.parseInt(node.getCharacter(), 2));
                    }
                }
            }
        }
        catch(Exception ex) {
            System.out.println(ex);
        }
    }
      
    
    Node ReadTree()
    {
//        String currentBit = this.seqToDecode.substring(0, 1);
//        this.seqToDecode = this.seqToDecode.substring(1);
        boolean isLeaf = false;
        if(this.seqToDecode.startsWith("true")) {
            isLeaf = true;
            this.seqToDecode = this.seqToDecode.substring(4);
        }
        else if(this.seqToDecode.startsWith("false")) {
            isLeaf = false;
            this.seqToDecode = this.seqToDecode.substring(5);
        }
        if (isLeaf)
        {
            Node nodeToReturn = new Node(this.seqToDecode.substring(0, K), null, null);
            this.seqToDecode = this.seqToDecode.substring(K);
            //System.out.println(nodeToReturn.getCharacter());
            return nodeToReturn;
        }
        else
        {
            Node leftChild = ReadTree();
            Node rightChild = ReadTree();
            return new Node("", leftChild, rightChild);
        }
    }
}
