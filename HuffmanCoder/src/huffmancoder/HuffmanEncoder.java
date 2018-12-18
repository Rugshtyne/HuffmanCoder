/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package huffmancoder;

import huffmancoder.entities.FreqTable;
import huffmancoder.entities.LookupTable;
import huffmancoder.entities.Node;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.InputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
/**
 *
 * @author Vilys
 */
public class HuffmanEncoder {
    
    private ArrayList<FreqTable> frequencyTable;
    private ArrayList<LookupTable> lookupTable;
    private int K;
    private StringBuilder sb;
    
    public HuffmanEncoder(String fileToRead, int K) {
        try {
            this.frequencyTable = new ArrayList<FreqTable>();
            this.lookupTable = new ArrayList<LookupTable>();
            this.sb = new StringBuilder();
            this.K = K;
            FileInputStream fileInput = new FileInputStream(fileToRead);
            int i = 0;            
            while((i = fileInput.read()) != -1) {
                //this.appendFile(fileToRead, String.valueOf((char)i));
                this.CreateFreqTable(String.format("%8s", Integer.toBinaryString(i)).replace(' ', '0'));
            }
            Node root = this.CreateTree();
            //System.out.println("|"+K+"|");
            this.PrintTree(root);
            this.buildCode(root, "");
            //this.writeFile(fileToRead);
//            for(FreqTable table : this.frequencyTable) {
//                System.out.println(Integer.parseInt(table.getByteSeq(),2)+"\t"+table.getFreq());
//            }
            for(LookupTable record : this.lookupTable) {
                System.out.println(record.getCharacter()+"\t"+record.getTreePath());
            }
            System.out.println(sb.toString());
            //this.HashFile(fileToRead);
        }
        catch(Exception ex) {
            System.out.println(ex);
        }
    }
    
    public void CreateFreqTable(String byteString) {
        try {            
            if (byteString.length() == K) {
                for(FreqTable line : this.frequencyTable) {
                    if(line.getByteSeq().equals(byteString)) {
                        if (Integer.parseInt(byteString,2) == 80) {
                            System.out.println("P");
                        }
                        FreqTable lineRem = this.frequencyTable.remove(this.frequencyTable.indexOf(line));
                        lineRem.setFreq(lineRem.getFreq()+1);
                        this.frequencyTable.add(lineRem);
                        return;
                    }
                }
                this.frequencyTable.add(new FreqTable(byteString));
            }
        }
        catch(Exception ex) {
            System.out.println(ex);
        }
    }
    
    public Node CreateTree() {
        ArrayList<Node> treeArray = new ArrayList<>();
        this.frequencyTable.forEach((line) -> {
            treeArray.add(new Node(line.getByteSeq(),line.getFreq(),null,null));
        });
        
        while (treeArray.size() > 1) {
            Node left = this.removeMinFreq(treeArray);
            treeArray.remove(left);
            Node right = this.removeMinFreq(treeArray);
            treeArray.remove(right);
            Node parent = new Node(left.getFreq()+right.getFreq(),left,right);
            treeArray.add(parent);
        }
        return treeArray.get(0);
    }
    
    private Node removeMinFreq(ArrayList<Node> list) {
        
        Collections.sort(list, new Comparator<Node>() {
                @Override
                public int compare(Node node1, Node node2 )
                {
                    return  node1.getFreq() - node2.getFreq();
                }
            });
        
        Node removedNode = list.get(0);
        return removedNode;
    }
    
    private void PrintTree(Node tree) {
        if (tree != null) {
                if (tree.getLeft() == null && tree.getRight() == null) {
                        // 0 = leaf
                        sb.append(0);
                        sb.append((char)(Integer.parseInt(tree.getCharacter(), 2)));
                } else {
                        // 1 = internal node
                        sb.append(1);
                }
                PrintTree(tree.getLeft());
                PrintTree(tree.getRight());
        }
    }
    
    private String chopStringUsingK(String byteString) {
        String byteStringToReturn = byteString;
        
        if(K % 8 == 0) {
            if (K == 8) {
                byteStringToReturn = byteString;
            }
        }
        return byteStringToReturn;
    }
    
    private void HashFile(String fileToRead) {
        try {
        File file = new File(fileToRead);
        BufferedReader input = new BufferedReader(new FileReader(file));
            int i = 0;      
            while((i = input.read())!=-1) {
                String toCode = this.chopStringUsingK(String.format("%8s", Integer.toBinaryString(i)).replace(' ', '0'));
                //System.out.println((char)i);
                for(LookupTable record : this.lookupTable) {
                if(record.getCharacter().equals(toCode)) {
                    //System.out.println(record.getTreePath());
                    this.appendFile(fileToRead, record.getTreePath());
                    break;
                }
            }
            }
        }
        catch(Exception ex) {
            System.out.println(ex);
        }
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
    
    private void writeFile(String fileToRead) {
        //File file = new File(fileToRead+".hof");
        try {
            FileWriter fw = new FileWriter(fileToRead+".hof", true);
            BufferedWriter bw = new BufferedWriter(fw);
            PrintWriter writer = new PrintWriter(bw);
            for(LookupTable record : this.lookupTable) {
                writer.println((char)Integer.parseInt(record.getCharacter(),2)+" "+record.getTreePath());
            }
            writer.close();
        }
        catch(Exception ex) {
            System.out.println(ex);
        }
    }
    
    private void appendFile(String fileToRead, String data) {
        try {
            FileWriter fw = new FileWriter(fileToRead+".hof", true);
            BufferedWriter bw = new BufferedWriter(fw);
            PrintWriter writer = new PrintWriter(bw);
            writer.print(data);
            writer.close();
        }
        catch(Exception ex) {
            System.out.println(ex);
        }
    }
    
    
}
