package SnakeNLadderMyApproach;

import java.util.List;
import java.util.Map;
import java.util.Queue;


class GameBoard {
    private Dice dice;
    private Queue<Player> nextTurn;
    private Map<Integer,Jumper> snakes;
    private  Map<Integer,Jumper> ladders;
    private  Map<String,Integer> playersCurrentPosition;
    int boardSize;

     GameBoard(Dice dice, Queue<Player> nextTurn, Map<Integer,Jumper> snakes, Map<Integer,Jumper> ladders,Map<String,Integer> playersCurrentPosition,int boardSize) {
        this.dice = dice;
        this.nextTurn = nextTurn;
        this.snakes = snakes;
        this.ladders = ladders;
        this.playersCurrentPosition = playersCurrentPosition;
        this.boardSize = boardSize;
    }

     void startGame(){
        while(nextTurn.size()>1) {
            Player player = nextTurn.poll();
            int currentPosition = playersCurrentPosition.get(player.getPlayerName());
            int diceValue = dice.rollDice();
            int nextCell = currentPosition + diceValue;
            if (nextCell > boardSize) nextTurn.offer(player);
            else if (nextCell == boardSize) {
                System.out.println( player.getPlayerName() + " won the game");
            }else{
               int nextPosition= nextCell;
               boolean b = false;
                //nextPosition= nextCell;
				/*
				 * snakes.forEach(v-> { if(v.startPoint==nextCell) { nextPosition[0] =
				 * v.endPoint; } } );
				 */
                if (snakes.get(nextCell)!=null) {
                	nextPosition = snakes.get(nextCell).getEndPoint();
                }
				/*
				 * if(nextPosition != nextCell) System.out.println(player.getPlayerName() +
				 * " Bitten by Snake present at: "+ nextCell); ladders.forEach(v-> {
				 * if(v.startPoint==nextCell) { nextPosition[0] = v.endPoint; b[0]=true; } } );
				 */
                
                if (ladders.get(nextCell)!=null) {
                	nextPosition = ladders.get(nextCell).getEndPoint();
                	b=true;
                }
                if(nextPosition != nextCell && b) System.out.println(player.getPlayerName() + " Got ladder present at: "+ nextCell);
                if(nextPosition == boardSize){
                    System.out.println(player.getPlayerName() + " won the game");
                }else{
                    playersCurrentPosition.put(player.getPlayerName(),nextPosition);
                    System.out.println(player.getPlayerName() + " is at position "+ nextPosition);
                    nextTurn.offer(player);
                }
            }
        }
    }
}
