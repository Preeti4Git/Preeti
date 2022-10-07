package Preeti;

import java.util.LinkedList;
import java.util.Queue;

public class CheckTreeCompletion {
	public boolean checkIfComplete(TreeNode t) {
	Queue<TreeNode> q = new LinkedList<>();
	q.offer(t);
	boolean flag = true;
	
	while (!q.isEmpty()) {
		t = q.poll();
		if(t.left == null) {flag = false;} else {
		q.offer(t.left);}
		if(t.right!=null) {
			if (flag == false) { return false;}
			else {
				q.offer(t.right);
		}
		
		}
	}
	return true;
	}
	
	
	public static void main(String[] args) {
		CheckTreeCompletion f = new CheckTreeCompletion();
		TreeNode n3 = new TreeNode(3);
		TreeNode n4 = new TreeNode(4);
		TreeNode n2 = new TreeNode(2,n3,n4);
		TreeNode n6 = new TreeNode(6);
		TreeNode n5 = new TreeNode(5,null,n6);
		TreeNode n1 = new TreeNode(1,n2,n5);
		
		
		System.out.println(f.checkIfComplete(n1));
	}
}

/*
 	1
   2   5
 3  4 6*/
