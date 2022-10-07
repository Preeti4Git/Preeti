package Preeti;

public class InvertBinaryTreeMyApproach {

	public TreeNode invertBinaryTree(TreeNode n) {
		if(n==null) return null;
		TreeNode t = new TreeNode();
		t = n.left;
		n.left = n.right;
		n.right = t;
		n.left = invertBinaryTree(n.left);
		n.right = invertBinaryTree(n.right);
		//below 2 lines also works instead of above 2 lines
		//invertBinaryTree(n.left);
		//invertBinaryTree(n.right);
		return n;
	}
	
	public static void main(String[] args) {
		InvertBinaryTreeMyApproach f = new InvertBinaryTreeMyApproach();
		TreeNode n3 = new TreeNode(3);
		TreeNode n4 = new TreeNode(4);
		TreeNode n2 = new TreeNode(2,n3,n4);
		TreeNode n6 = new TreeNode(6);
		TreeNode n5 = new TreeNode(5,null,n6);
		TreeNode n1 = new TreeNode(1,n2,n5);
		
		
		f.invertBinaryTree(n1);
	}
}


/*
 		 1
 	  2     5
 	3   4      6 
 */
