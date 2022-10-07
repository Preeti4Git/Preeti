package Preeti;

public class PruneTree {
	public TreeNode pruneTree(TreeNode root) {
		if(root==null) return null;
		if(root.left==null && root.right == null && root.val ==0) return null;
		root.left = pruneTree(root.left);
		root.right = pruneTree(root.right);
		return root;
	}
	
	public static void main(String[] args) {
		PruneTree f = new PruneTree();
		TreeNode n3 = new TreeNode(0);
		TreeNode n4 = new TreeNode(1);
		TreeNode n2 = new TreeNode(0,n3,n4);
		//TreeNode n6 = new TreeNode(6);
		//TreeNode n5 = new TreeNode(5,null,n6);
		TreeNode n1 = new TreeNode(1,null,n2);
		
		
		System.out.println(f.pruneTree(n1));
	}
}

/*
	1
		0
	 0		1	
*/