/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package huffmancoder.entities;

/**
 *
 * @author Vilys
 */
public class Node {
    private String character;
    private int freq;
    private Node left, right;
    
    public Node(String character, int freq, Node left, Node right) {
        this.character = character;
        this.freq = freq;
        this.left = left;
        this.right = right;
    }
    
    public Node(int freq, Node left, Node right) {
        this.freq = freq;
        this.left = left;
        this.right = right;
    }
    
    public Node(String character, Node left, Node right) {
        this.character = character;
        this.left = left;
        this.right = right;
    }

    public Node() {
    }
    
    public boolean checkIfLeaf() {
        return (left == null && right == null);
    }
    
    public int compareFreq(Node otherNode) {
        return this.freq - otherNode.freq;
    }
    
    public void setFreq(int freq) {
        this.freq = freq;
    }
    
    public void setLeftNode(Node left) {
        this.left = left;
    }
    
    public void setRightNode(Node right) {
        this.right = right;
    }
    
    public int getFreq() {
        return freq;
    }
    
    public String getCharacter() {
        return character;
    }

    public Node getLeft() {
        return left;
    }
    
    public Node getRight() {
        return right;
    }
}
