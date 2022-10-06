package singleton;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class SingletonBreaker{
	public static void main(String[] args) throws ClassNotFoundException, NoSuchMethodException, SecurityException, FileNotFoundException, IOException, CloneNotSupportedException, InstantiationException, IllegalAccessException, IllegalArgumentException, InvocationTargetException {
		Singleton singleton = Singleton.getInstance();
		Singleton singleton2 = Singleton.getInstance();
		System.out.println(" singleton hashcode :"+singleton.hashCode());
		System.out.println(" singleton2 hashcode :"+singleton2.hashCode());
		
		System.out.println(" Singleton pattern break through Reflection");
		/*Class<?> sing = Class.forName("singleton.Singleton");
		Constructor<Singleton> k = (Constructor<Singleton>) sing.getDeclaredConstructor();
		k.setAccessible(true);
		Singleton singleton3 = new Singleton();
		System.out.println(" singleton3 hashcode :"+singleton3.hashCode());*/
				
		Class<?> sing2 = Class.forName("singleton.Singleton");
		Constructor<Singleton> cons = (Constructor<Singleton>) sing2.getDeclaredConstructor();
		cons.setAccessible(true);
		Singleton singleton4 = cons.newInstance();
		System.out.println(" singleton4 hashcode :"+singleton4.hashCode());
		
		
		//Below will work only if we convert constuctor to a normal method with return type as void
		
		/*Method s = Singleton.class.getDeclaredMethod("Singleton");
		s.setAccessible(true);
		Singleton singletonBreakerThroughReflection = new Singleton();
		System.out.println(" singletonBreakerThroughReflection hashcode :"+singletonBreakerThroughReflection.hashCode());*/
		
		System.out.println(" SIngleton pattern break through serialization");
		ObjectOutputStream objectOutputStream = new ObjectOutputStream(new FileOutputStream("C:\\Users\\ezaggpr\\eclipse-workspace\\DesignPattern\\src\\singleton\\singleton.ser"));
		objectOutputStream.writeObject(singleton);
		objectOutputStream.close();
		
		ObjectInputStream objectInputStream = new ObjectInputStream(new FileInputStream("C:\\Users\\ezaggpr\\eclipse-workspace\\DesignPattern\\src\\singleton\\singleton.ser"));
		Singleton singletonBreakThroughSerialization = (Singleton) objectInputStream.readObject();
		objectInputStream.close();
		System.out.println(" singletonBreakThroughSerialization hashcode :"+singletonBreakThroughSerialization.hashCode());
		
		System.out.println(" SIngleton pattern break through Cloning");
		Singleton singleBreakThroughCloning = (Singleton)singleton.clone();
		System.out.println(" singleBreakThroughCloning hashcode :"+singleBreakThroughCloning.hashCode());
		
		
		
	}
	
}
