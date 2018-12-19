/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package huffmancoder;

import huffmancoder.entities.LookupTable;
import huffmancoder.entities.Node;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.InputStream;
import java.util.ArrayList;

/**
 *
 * @author Vilys
 */
public class HuffmanDecoder {
    
    int K;
    String seqToDecode = "";
    char[] seqArray ;
    int currentPointer = 0;
    private ArrayList<LookupTable> lookupTable;
    
    public HuffmanDecoder(String fileToRead) {
        try {
            this.lookupTable = new ArrayList<LookupTable>();
            FileInputStream fileInput = new FileInputStream(fileToRead);
            int i = 0;            
            while((i = fileInput.read()) != -1) {
                this.seqToDecode += String.format("%8s", Integer.toBinaryString(i)).replace(" ", "0");

            }
            
            System.out.println(this.seqToDecode);
            this.seqArray = this.seqToDecode.toCharArray();
            Node root = new Node();
            this.ReadTree(root);
            this.buildCode(root, "");
            
            for(LookupTable record : this.lookupTable) {
                System.out.println(record.getCharacter()+"\t"+record.getTreePath());
            }
            
            
        }
        catch(Exception ex) {
            System.out.println(ex);
        }
    }
    
    String getBit() {
        String bitToReturn = "";
        bitToReturn = String.valueOf((char)Integer.parseInt(this.seqToDecode.substring(0, 8), 2));
        this.seqToDecode = this.seqToDecode.substring(8);
        return bitToReturn;
    }
      
    String getByte() {
        String byteToReturn = "";
        byteToReturn = this.seqToDecode.substring(0, 8);
        this.seqToDecode = this.seqToDecode.substring(8);
        return byteToReturn;
    }
    
    private void ReadTree(Node root)
    {
        String currentBit = this.getBit();
        // 1 = internal node
        System.out.println(currentBit);
        if (currentBit.equals("1")) {
                root.setLeftNode(new Node());
                this.ReadTree(root.getLeft());
        } else {
                // 0 = leaf
                root.setLeftNode(new Node(this.getByte(), null, null));
        }

        currentBit = this.getBit();
        System.out.println(currentBit);
        // 1 = internal node
        if (currentBit.equals("1")) {
                root.setRightNode(new Node());
                this.ReadTree(root.getRight());
        } else {
                // 0 = leaf
                root.setRightNode(new Node(this.getByte(), null, null));
        }
//        boolean isLeaf = false;
//        if(currentBit.startsWith("1")) {
//            isLeaf = true;
//        }
//        else if(currentBit.startsWith("0")) {
//            isLeaf = false;
//        }
//        if (isLeaf)
//        {
//            Node nodeToReturn = new Node(this.getByte(), null, null);
//            return nodeToReturn;
//        }
//        else
//        {
//            Node leftChild = ReadTree();
//            Node rightChild = ReadTree();
//            return new Node("", leftChild, rightChild);
//        }
    }
    
    
    
    private void buildCode(Node node, String s) {
        if (!node.checkIfLeaf()) {
            buildCode(node.getLeft(),  s + '0');
            buildCode(node.getRight(), s + '1');
        }
        else {
            for(LookupTable record : this.lookupTable) {
                if(record != null && record.findRecordByCharacter(node.getCharacter())) {
                    this.lookupTable.get(this.lookupTable.indexOf(record)).appendTreePath(s);
                    return;
                }
            }
            this.lookupTable.add(new LookupTable(node.getCharacter(),s));
        }
    }
}
