/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package huffmancoder;

import huffmancoder.entities.FreqTable;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.ArrayList;
/**
 *
 * @author Vilys
 */
public class HuffmanEncoder {
    
    private ArrayList<FreqTable> frequencyTable;
    private int K;
    private String byteStringLeftover = "";
    
    public HuffmanEncoder(String fileToRead, int K) {
        try {
            this.frequencyTable = new ArrayList<FreqTable>();
            this.K = K;
            File a = new File(fileToRead);
            InputStream input = new FileInputStream(a);
            int i = 0;            
            while((i = input.read())!=-1) {
                this.CreateFreqTable(String.format("%8s", Integer.toBinaryString(i)).replace(' ', '0'));
            }
            this.frequencyTable.forEach((line) -> {
            System.out.println(line.getByteSeq()+"\t"+line.getFreq());
        });
        }
        catch(Exception ex) {
            System.out.println(ex);
        }
    }
    
    public void CreateFreqTable(String byteString) {
        try {
            final String byteStringToOperate;
            if (byteString.length() == K) {
                this.frequencyTable.forEach((line) -> {
                    if (line.getByteSeq().equals(byteString)) {
                        line.increaseFreq();
                    }
                });
                this.frequencyTable.add(new FreqTable(byteString));
            }
            else {
                if(K < 8) {
                    if (byteStringLeftover.length() == 0) {
                        byteStringToOperate = byteString.substring(0,K);
                        byteStringLeftover = byteString.substring(K-1);
                        
                        
                        this.frequencyTable.forEach((line) -> {
                            if (line.getByteSeq().equals(byteStringToOperate)) {
                                line.increaseFreq();

                            }
                        });
                        this.frequencyTable.add(new FreqTable(byteStringToOperate));
                    }
                    else {
                        byteStringToOperate = this.byteStringLeftover + 
                                byteString.substring(0,K-this.byteStringLeftover.length());
                        System.out.println(K-this.byteStringLeftover.length());
                        System.out.println(byteString);
                        this.byteStringLeftover = byteString.substring(this.byteStringLeftover.length());
                        
                        this.frequencyTable.forEach((line) -> {
                            if (line.getByteSeq().equals(byteStringToOperate)) {
                                line.increaseFreq();

                            }
                        });
                        this.frequencyTable.add(new FreqTable(byteStringToOperate));
                    }
                    
                    if (K == byteStringLeftover.length()) {
                        
                        this.frequencyTable.forEach((line) -> {
                            if (line.getByteSeq().equals(byteStringLeftover)) {
                                line.increaseFreq();
                            }
                        });
                        this.frequencyTable.add(new FreqTable(byteStringLeftover));
                        
                        byteStringLeftover = "";
                    }
                }
                else if (K > 8) {                  
                    if ((byteStringLeftover.length() + byteString.length()) == K) {
                        byteStringToOperate = this.byteStringLeftover + byteString;
                        this.frequencyTable.forEach((line) -> {
                            if (line.getByteSeq().equals(byteStringToOperate)) {
                                line.increaseFreq();
                            }
                        });
                        this.frequencyTable.add(new FreqTable(byteStringToOperate));
                    }
                    if ((byteStringLeftover.length() + byteString.length()) > K) {
                        String byteStringToOperate2 = this.byteStringLeftover + byteString.substring(0, K-this.byteStringLeftover.length());
                        this.byteStringLeftover = byteString.substring(K-this.byteStringLeftover.length());
                        
                        this.frequencyTable.forEach((line) -> {
                            if (line.getByteSeq().equals(byteStringToOperate2)) {
                                line.increaseFreq();
                            }
                        });
                        this.frequencyTable.add(new FreqTable(byteStringToOperate2));
                    }
                    if ((byteStringLeftover.length() + byteString.length()) < K) {
                        this.byteStringLeftover = this.byteStringLeftover+byteString;
                    }
                    
                    if (K == byteStringLeftover.length()) {
                        
                        this.frequencyTable.forEach((line) -> {
                            if (line.getByteSeq().equals(byteStringLeftover)) {
                                line.increaseFreq();
                            }
                        });
                        this.frequencyTable.add(new FreqTable(byteStringLeftover));
                        
                        byteStringLeftover = "";
                    }
                }
            }
        }
        catch(Exception ex) {
            System.out.println(ex);
        }
    }
    
}
