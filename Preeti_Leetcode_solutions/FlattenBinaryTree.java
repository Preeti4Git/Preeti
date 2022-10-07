package Preeti;

/*public class TreeNode{
	int val;
	TreeNode left;
	TreeNode right;
	TreeNode(){};
	TreeNode(int val){
		this.val = val;		
	}
	TreeNode(int val, TreeNode left, TreeNode right){
		this.val = val;		
		this.left = left;
		this.right = right;
	}
	
}*/

public class FlattenBinaryTree {
	public void flatten(TreeNode root) {
		if(root == null) return;
		TreeNode right = root.right;
		flatten(root.left);
		root.right = root.left;
		root.left = null;
		while(root.right!=null)root = root.right;
		flatten(right);
		root.right = right;
		System.out.println(root);
		
	}
	
	public static void main(String[] args) {
		FlattenBinaryTree f = new FlattenBinaryTree();
		TreeNode n3 = new TreeNode(3);
		TreeNode n4 = new TreeNode(4);
		TreeNode n2 = new TreeNode(2,n3,n4);
		TreeNode n6 = new TreeNode(6);
		TreeNode n5 = new TreeNode(5,null,n6);
		TreeNode n1 = new TreeNode(1,n2,n5);
		
		
		f.flatten(n1);
	}
}
