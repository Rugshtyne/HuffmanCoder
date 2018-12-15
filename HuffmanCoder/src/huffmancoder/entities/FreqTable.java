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
public class FreqTable {
    private String byteSeq;
    private int freq = 1;
    
    public FreqTable(String byteSeq) {
        this.byteSeq = byteSeq;
    }
    
    public String getByteSeq() {
        return this.byteSeq;
    }
    public void setByteSeq(String byteSeq) {
        this.byteSeq = byteSeq;
    }
    
    public void increaseFreq() {
        this.freq++;
    }
    
    public int getFreq() {
        return this.freq;
    }
}
