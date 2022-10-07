package Preeti;

public class MaxProductSubarray {
	private int maxProduct(int[] num) {
		int result = num[0];
		int maxProd = num[0];
		int minProd = num[0];
		boolean negFlag = false;
		
		for(int i=0;i<num.length;i++) {
			
			if(num[i]<0) {
				//if(negFlag = true) {negFlag = false;
				int tmp = maxProd;
				maxProd = minProd;
				minProd = tmp;
				//} else {
				//	negFlag = true;
				//}
			}
			
			maxProd = Math.max(maxProd*num[i], num[i]);
			minProd = Math.min(minProd*num[i], num[i]);
		}
		result = Math.max(maxProd, result);
		
		return result;
	}
	
	public static void main(String[] args) {
		int[] num = new int[] {1,-2,3,-4,-5};
		MaxProductSubarray m = new MaxProductSubarray();
		System.out.println(m.maxProduct(num));
		
	}
	
}
