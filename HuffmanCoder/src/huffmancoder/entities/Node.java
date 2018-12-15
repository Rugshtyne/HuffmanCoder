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
    private final String character;
    private final float freq;
    private final Node left, right;
    
    public Node(String character, float freq, Node left, Node right) {
        this.character = character;
        this.freq = freq;
        this.left = left;
        this.right = right;
    }
    
    public boolean checkIfLeaf() {
        return (left == null && right == null);
    }
    
    public float compareFreq(Node otherNode) {
        return this.freq - otherNode.freq;
    }
}
