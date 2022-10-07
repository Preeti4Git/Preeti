package Preeti;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class LogConsecutivePageVisited {
	public static void main(String[] args) {
		List<List> logList = new ArrayList<>();
		//logList.add((0,"C1","A"));
		//,{0,"C2","E"}};
		logList = Arrays.asList(Arrays.asList(0,"C1","A"),Arrays.asList(0,"C2","E"),Arrays.asList(1,"C1","B"),
				Arrays.asList(1,"C2","B"),Arrays.asList(2,"C1","C"),Arrays.asList(2,"C2","C"),
				Arrays.asList(3,"C1","D"),Arrays.asList(3,"C2","D"),Arrays.asList(4,"C1","E"),Arrays.asList(4,"C2","A"));
		
		Map<String, String> userMap = new HashMap<>();
		List<String> l = new ArrayList<>();
		String set;
		List<String> pageSets = new ArrayList<>();
		for(int i=0;i<logList.size();i++) {
			l = logList.get(i);
			if(userMap.get(l.get(1))==null) {
				userMap.put(l.get(1).toString(),l.get(2).toString());
			} else {
				String pagesVisisted = userMap.get(l.get(1));
				userMap.put(l.get(1).toString(), pagesVisisted+l.get(2).toString());
			}
		}
		for(String k : userMap.values()) {
			System.out.println(k);
			for(int j=0;j<k.length()-2;j++) {
				pageSets.add(k.substring(j, j+3));
			}
		}
		System.out.println(pageSets);
	}
}
