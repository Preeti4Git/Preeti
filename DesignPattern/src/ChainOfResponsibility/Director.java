package ChainOfResponsibility;

public class Director extends Manager{
	public Director(String name, int approvalLimit){
		this.name = name;
		this.approvalLimit = approvalLimit;
	}
	public void processEmployment(){
		System.out.println("Employment processed by Director");
	}
}