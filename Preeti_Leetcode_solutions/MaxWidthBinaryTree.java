package Preeti;

import java.util.ArrayList;
import java.util.List;

public class MaxWidthBinaryTree {
	
	public int WidthOfBinaryTree(TreeNode root) {
		List<Integer> l = new ArrayList<>();
		int width = dfs(root,0,1,l);
		System.out.println(width);
		return width; 
	}
	
	public int dfs(TreeNode root, int level, int id, List<Integer> l) {
		if(root == null) return 0;
		if(level == l.size()) l.add(id);
		
		int curr = id-l.get(level)+1;
		int left = dfs(root.left,level+1,2*id,l);
		int right = dfs(root.right,level+1,2*id+1,l);
		
		return Math.max(curr, Math.max(left, right));
		
	}

	public static void main(String[] args) {
		MaxWidthBinaryTree f = new MaxWidthBinaryTree();
		TreeNode n3 = new TreeNode(3);
		TreeNode n4 = new TreeNode(4);
		TreeNode n2 = new TreeNode(2,null,n4);
		TreeNode n6 = new TreeNode(6);
		TreeNode n5 = new TreeNode(5,null,n6);
		TreeNode n1 = new TreeNode(1,n2,n5);
		
		
		f.WidthOfBinaryTree(n1);
	}
}
