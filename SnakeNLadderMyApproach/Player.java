package SnakeNLadderMyApproach;


class Player {
    private String playerName;
    private int id;

    Player(String playerName, int id) {
        this.playerName = playerName;
        this.id = id;
    }
    
    public void setPlayerName(String playerName) {
    	this.playerName = playerName;    	
    }
    
    public String getPlayerName() {
    	return this.playerName;    	
    }
    
    public void setPlayerId(int id) {
    	this.id = id;    	
    }
    
    public int getPlayerId() {
    	return this.id;  
    }
}
