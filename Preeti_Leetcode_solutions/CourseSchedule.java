package Preeti;

import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;


//import javax.sound.sampled.AudioFormat.Encoding;

public class CourseSchedule {

	public boolean checkCourseCompletion(int numCourses, int[][] dependencies) {
		
		Map<Integer, List<Integer>> courseMap = new HashMap<>();
		int[] ingress = new int[numCourses];
		Queue<Integer> courseCompletion = new LinkedList<>();
		int count = numCourses;
		
		for(int i=0;i<numCourses;i++) {
			courseMap.put(i, new ArrayList<Integer>());
		}
		
		for(int i=0;i<dependencies.length;i++) {
			int dependency = dependencies[i][1];
			int course = dependencies[i][0];
			
			List<Integer> dependencyList = courseMap.get(dependency);
			dependencyList.add(course);
			
			ingress[course]++;
		}
		
		
		for(int j=0;j<numCourses;j++) {
			if(ingress[j] == 0) {
				courseCompletion.offer(j);
			} 
		}
			if(courseCompletion.isEmpty()) 
				return false;
			/*
			 * if(courseMap.get(j).isEmpty()) { courseCompletion.offer(j); }
			 */
		
		
		while(!courseCompletion.isEmpty()) {
			int courseTodo = courseCompletion.poll();
			count--;
			//List<Integer> courseReleased = courseMap.get(courseTodo);
			for (int i:courseMap.get(courseTodo)) {
				ingress[i]--;
				if(ingress[i] == 0) courseCompletion.offer(i);
			}
			/*for(int j=0;j<numCourses;j++) {
				if(ingress[j] == 0) {
					courseCompletion.offer(j);
				}*/
		}
		
		
			
		
		return count==0;
	}
	
	public static void main(String[] args) {
		
		String encodeBytes = Base64.getEncoder().encodeToString(("du" + ":" + "VW2sa6uS5p53wiqsq65Coe4wdkuC7E").getBytes());
		//System.out.println(encodeBytes);
		System.out.println(encodeBytes);
		//String basicAuthenticationHeader = Convert.ToBase64String(Encoding.GetEncoding("ISO-8859-1").GetBytes($"{username}:{password}"));
		//System.out.println(basicAuthenticationHeader);
		
		int[][] prerequisites = {{1,0},{2,1},{3,2},{3,1}};
		CourseSchedule c = new CourseSchedule();
		System.out.println(c.checkCourseCompletion(4, prerequisites));
		
		
	}
	
}

/*
[1,0]
[2,1]
[3,2]
[3,1]

0-->1
1-->2,3
2-->3
3

[0,0,1,2]
*/