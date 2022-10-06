package ChainOfResponsibility;

public class BuildManagerChain{
	public Manager buildChain(){
		Manager hiringManager = new HiringManager("Alex",10000);
		Manager seniorManager = new SeniorManager("Bob",25000);
		Manager director = new Director("Charlie",50000);
		hiringManager.setManager(seniorManager);
		seniorManager.setManager(director);
		return hiringManager;
	}
}
