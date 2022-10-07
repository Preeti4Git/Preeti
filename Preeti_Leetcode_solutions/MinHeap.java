package Preeti;

public class MinHeap {
	int[] arr;
	int size;
	int capacity;
	
	public int getParentNodeIndex(int i) {
		return (i-1)/2;
	}
	
	public int getLeftChildIndex(int i) {
		return 2*i+1;
	}
	
	public int getRightChildIndex(int i) {
		return 2*i+2;
	}
	
	public MinHeap() {
		this.capacity = 20;
		this.arr = new int[this.capacity];
		/*
		 * this.arr[0]=1; this.arr[1]=2; this.arr[2]=3; this.arr[3]=4; this.size =
		 * arr.length;
		 */
	}
	
	public int[] doubleHeapCapacity() {
		this.capacity *= 2;
		int[] newArr = new int[this.capacity];
		newArr = arr;
		return newArr;
	}
	
	public int peek() {
		return arr[0];
	}
	
	public int poll() {
		System.out.println("<-------------->");
		for(int i=0;i<this.arr.length;i++) {
			System.out.println(this.arr[i]);
		}
		System.out.println("<-------------->");
		int val = arr[0];
		arr[0] = arr[size-1];
		this.size--;
		heapifyDown();
		System.out.println("<---here----------->");
		for(int i=0;i<this.arr.length;i++) {
			System.out.println(this.arr[i]);
		}
		System.out.println("<-------------->");
		return val;
	}

	public void insertNode(int val) {
		if(size == this.capacity) {
			arr = doubleHeapCapacity();
		}
		arr[size] = val;
		size++;
		heapifyUp();
		System.out.println("<-------------->");
		for(int i=0;i<this.arr.length;i++) {
			System.out.println(this.arr[i]);
		}
		System.out.println("<-------------->");
	}
	
	public void swap(int a, int b) {
		int tmp = this.arr[a];
		this.arr[a] = this.arr[b];
		this.arr[b] = tmp;		
	}
	
	public void heapifyUp() {
		int n = size-1;
		while (getParentNodeIndex(n)>=0) {
			if(this.arr[n]<this.arr[getParentNodeIndex(n)]) {
				swap (n,getParentNodeIndex(n));
				n = getParentNodeIndex(n);
			} else break;
		}
	}
	
	public void heapifyDown() {
		int n = 0;
		while (getRightChildIndex(n)<size) {
			if(this.arr[n]>this.arr[getLeftChildIndex(n)]) {
				swap(getLeftChildIndex(n),n);
			}
			if(this.arr[n]>this.arr[getRightChildIndex(n)]) {
				swap (n,getRightChildIndex(n));
			}
			n=getRightChildIndex(n);
		}
	}
	
	public static void main(String[] args) {
		//array{1,2,3,5,6,7,8,9,10,11};
		MinHeap minHeap = new MinHeap();
		minHeap.insertNode(4);
		minHeap.insertNode(5);
		minHeap.insertNode(8);
		minHeap.insertNode(2);
		minHeap.insertNode(1);
		System.out.println(minHeap.peek());
		System.out.println("poll "+minHeap.poll());
		
	}
}
