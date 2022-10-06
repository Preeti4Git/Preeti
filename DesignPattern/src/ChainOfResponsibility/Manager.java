package ChainOfResponsibility;

public abstract class Manager{
	Manager manager;
	String name;
	int approvalLimit;
	
	public void approveHiring(int employeeAsk){
		if(employeeAsk < this.approvalLimit){
			processEmployment();
		} else if (manager !=null) {
			this.manager.approveHiring(employeeAsk);
		} else {
			System.out.println("Employment cannot be processed");
		}
	}
	
	public abstract void processEmployment();
	
	public void setManager(Manager manager){
		this.manager = manager;
	}
}