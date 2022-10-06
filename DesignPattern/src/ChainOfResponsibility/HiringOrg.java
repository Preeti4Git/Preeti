package ChainOfResponsibility;

public class HiringOrg{
public static void main (String[] args){
	BuildManagerChain buildManagerChain = new BuildManagerChain();
	Manager hiringManager = buildManagerChain.buildChain();
	hiringManager.approveHiring(5000);
	hiringManager.approveHiring(15000);
	hiringManager.approveHiring(40000);
	hiringManager.approveHiring(5000000);
	}
}
