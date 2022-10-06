package ChainOfResponsibility;

public class HiringManager extends Manager{
	public HiringManager(String name, int approvalLimit){
		this.name = name;
		this.approvalLimit = approvalLimit;
	}

	@Override
	public void processEmployment() {
		System.out.println("Employment processed by Hiring manager");
	}
		
	}
	
