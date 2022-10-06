package singleton;

import java.io.Serializable;

public class Singleton implements Serializable, Cloneable{
 /**
	 * 
	 */
	private static final long serialVersionUID = 1L;
private static Singleton singletonObject;
 
 private Singleton() {
		
		/*
		 * if (singletonObject != null) { throw new
		 * IllegalStateException("ALready exists"); }
		 */
		
 }
 
 public static Singleton getInstance() {
	 if (singletonObject == null) {
		 singletonObject = new Singleton();
	 }
	 return singletonObject;
 }
 
 public Singleton clone() throws CloneNotSupportedException {
	 return (Singleton) super.clone();
 }
 
 //to prevent singleton pattern break through cloning
	/*
	 * public Singleton clone() throws CloneNotSupportedException { throw new
	 * CloneNotSupportedException(); }
	 */
 
//to prevent singleton pattern break through serialization
	/*
	 * public Object readResolve() { return singletonObject;
	 * 
	 * }
	 */
 

 }
