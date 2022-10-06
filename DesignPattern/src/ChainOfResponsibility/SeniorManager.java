package ChainOfResponsibility;

public class SeniorManager extends Manager{
	public SeniorManager(String name, int approvalLimit){
		this.name = name;
		this.approvalLimit = approvalLimit;
	}
	public void processEmployment(){
		System.out.println("Employment processed by Senior Manager");
	}

}
