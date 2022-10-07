package SnakeNLadderMyApproach;

import java.util.*;

public class PlaySnakeAndLadder {
    public static void main(String[] args) {
        Dice dice = new Dice(1);
        Player p1 = new Player("Alberts",1);
        Player p2 = new Player("Pintoss",2);
        Queue<Player> allPlayers = new LinkedList<>();
        allPlayers.offer(p1);
        allPlayers.offer(p2);
        Jumper snake1 = new Jumper(10,2);
        Jumper snake2 = new Jumper(99,12);
        Map<Integer,Jumper> snakes = new HashMap<>();
        snakes.put(snake1.getStartPoint(),snake1);
        snakes.put(snake2.getStartPoint(),snake2);
        //snakes.add(snake2);
        Jumper ladder1 = new Jumper(5,25);
        Jumper ladder2 = new Jumper(40,89);
        //List<Jumper> ladders = new ArrayList<>();
        //ladders.add(ladder1);
        //ladders.add(ladder2);
        Map<Integer,Jumper> ladders = new HashMap<>();
        ladders.put(ladder1.getStartPoint(),ladder1);
        ladders.put(ladder2.getStartPoint(),ladder2);
        Map<String,Integer> playersCurrentPosition = new HashMap<>();
        playersCurrentPosition.put("Alberts",0);
        playersCurrentPosition.put("Pintoss",0);
        GameBoard gb=new GameBoard(dice,allPlayers,snakes,ladders,playersCurrentPosition,100);
        gb.startGame();
    }
}
