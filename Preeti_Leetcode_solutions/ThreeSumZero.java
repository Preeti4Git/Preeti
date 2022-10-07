package Preeti;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ThreeSumZero {

	public List<List<Integer>> threesum (int[] s, int targetValue){
		List<List<Integer>> result = new ArrayList<>();
		Arrays.sort(s);
		
		for (int i=0;i<s.length-2;i++) {
			int target = targetValue-s[i];
			int low = i+1;
			int high = s.length-1;
			if(i>0 && s[i] == s[i-1]) continue;
			
			while(low<high) {
			if(s[low]+s[high] == target) {
				result.add(Arrays.asList(s[i],s[low],s[high]));
				if(s[low]==s[low+1]) low++;
				if(s[high]==s[high-1])high--;
				low++;
				high--;
			} else if (s[low]+s[high] < target) {
				low++;
			} else {
				high--;
			}
			}
		}
		System.out.println(result.toString());
		return result;
	}
	
	public static void main(String[] args) {
		ThreeSumZero t = new ThreeSumZero();
		int[] inArray = new int[] {-4,-1,5,-5,-1,0,0,1,2,4,8} ;
		//[-4,-1,-1,0,0,1,2,4,8];
		t.threesum(inArray, 6);
	}
}

/*
-4 -1 -1 0 0 1 2 4 8

-4 -1 1 2
*/
