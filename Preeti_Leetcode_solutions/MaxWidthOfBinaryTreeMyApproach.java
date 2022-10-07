package Preeti;

import java.util.LinkedList;
import java.util.Queue;

public class MaxWidthOfBinaryTreeMyApproach {
	public int findMaxWidth(TreeNode tree) {
		int maxWidth = 0;
		Queue<TreeNode> q = new LinkedList<>();
		q.offer(tree);
		
		while (!q.isEmpty()) {
			int size = q.size();
			if (size>maxWidth) maxWidth = size;
			for(int i =0;i<size;i++) {
				TreeNode t = q.poll();
				if(t.left!=null) q.offer(t.left);
				if(t.right!=null) q.offer(t.right);
			}
			
		}
		return maxWidth;
	}
	
	public static void main(String[] args) {
		MaxWidthOfBinaryTreeMyApproach f = new MaxWidthOfBinaryTreeMyApproach();
		TreeNode n3 = new TreeNode(3);
		TreeNode n4 = new TreeNode(4);
		TreeNode n2 = new TreeNode(2,n3,n4);
		TreeNode n6 = new TreeNode(6);
		TreeNode n5 = new TreeNode(5,null,n6);
		TreeNode n1 = new TreeNode(1,n2,n5);
		
		
		System.out.println(f.findMaxWidth(n1));
}
}

/*
 	1
  2   5
   4    6
 */
