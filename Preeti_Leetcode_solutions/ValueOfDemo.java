package Preeti;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.stream.Collectors;

public class ValueOfDemo {
	
	public void add(String s1, String s2) {
        // this program requires two 
        // arguments on the command line 
        // convert strings to numbers
            float a = Float.valueOf(s1); 
            float b = (Float.valueOf(s2)).floatValue();

            // do some arithmetic
            System.out.println("a + b = " +
                               (a + b));
            System.out.println("a - b = " +
                               (a - b));
            System.out.println("a * b = " +
                               (a * b));
            System.out.println("a / b = " +
                               (a / b));
            System.out.println("a % b = " +
                               (a % b));
        
	}
	
    public static void main(String[] args) {
		/*
		 * ValueOfDemo v = new ValueOfDemo(); v.add("2","3"); String s =
		 * "837836 58ywdiuhsejfgjhsdfgb"; //CharSequence c = new CharSequence();
		 * System.out.println(s.subSequence(3,9));
		 */
    	
    	      List<String> arrList = Arrays.asList("John", "Jacob", "Kevin", "Katie", "Nathan");
    	      System.out.println("ArrayList = " + arrList);
    	      List<String> myList = arrList.stream().collect(Collectors.toCollection(LinkedList::new));
    	      System.out.println("LinkedList (ArrayList to LinkedList) = " + myList);
    	      
    	      int[][] test = new int[][]{{1,2,3},{1,2,3}};
    	   
    }
    
}