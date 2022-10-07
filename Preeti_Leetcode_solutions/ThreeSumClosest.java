package Preeti;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ThreeSumClosest {

	public int threesum (int[] s, int targetValue){
		List<List<Integer>> result = new ArrayList<>();
		Arrays.sort(s);
		int min = Math.abs(s[0]+s[1]+s[2] - targetValue);
		int dist = 0;
		for (int i=0;i<s.length-2;i++) {
			int low = i+1;
			int high = s.length-1;
			while(low<high) {
				dist = Math.abs(s[i] + s[low]+s[high] - targetValue);
			if( dist < min) {
				result.add(Arrays.asList(s[i],s[low],s[high]));
				min = dist;
				low++;
			} else {
				high--;
			}
			}
		}
		System.out.println(result.toString());
		System.out.println(min);
		return min;
	}
	
	public static void main(String[] args) {
		ThreeSumClosest t = new ThreeSumClosest();
		int[] inArray = new int[]{-4,-1,5,-5,-1,0,0,1,2,4,8} ;
		//[-4,-1,-1,0,0,1,2,4,8];
		t.threesum(inArray, 20);
	}
}

/*
-4 -1 -1 0 0 1 2 4 8

-4 -1 1 2

-5, -4, -1, -1, 0, 0, 1, 2, 4, 5, 8
*/
