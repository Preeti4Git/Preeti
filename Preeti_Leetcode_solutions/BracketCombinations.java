package Preeti;

import java.util.LinkedList;
import java.util.List;

public class BracketCombinations {
	List<String> result = new LinkedList<String>();
	
	public List<String> getCombinations(int n){
		/*
		 * if (n==0) { return new LinkedList<String>(); }
		 */
		//String str="";
		generateString(result,0,0,n,"");
		return result;
		
	}
	
	public void generateString(List<String> result, int open, int close, int n, String str) {
		if (str.length() == 2*n) {
			result.add(str);
			return;
		}
		if(open<n) {
			generateString(result,open+1,close,n,str+"(");
		}
		if(close<open) {
			generateString(result,open, close+1,n,str+")");
		}
		
	}
	
	public static void main(String[] args) {
		BracketCombinations b = new BracketCombinations();
		List<String> l = b.getCombinations(3);
		System.out.println(l);
		
		
	}
}
