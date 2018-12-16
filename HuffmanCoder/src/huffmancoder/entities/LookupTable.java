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
public class LookupTable {
    private String character;
    private String treePath;
    
    public LookupTable(String character, String treePath) {
        this.character = character;
        this.treePath = treePath;
    }
    
    public boolean findRecordByCharacter(String character) {
        return this.getCharacter().equals(character);
    }
    
    public void appendTreePath(String appendPath) {
        this.setTreePath(this.getTreePath().concat(appendPath));
    }

    /**
     * @return the character
     */
    public String getCharacter() {
        return character;
    }

    /**
     * @param character the character to set
     */
    public void setCharacter(String character) {
        this.character = character;
    }

    /**
     * @return the treePath
     */
    public String getTreePath() {
        return treePath;
    }

    /**
     * @param treePath the treePath to set
     */
    public void setTreePath(String treePath) {
        this.treePath = treePath;
    }
}
