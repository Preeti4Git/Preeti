package BridgeDesignPattern;

public class Email implements NotificationService{

	@Override
	public void sendNotification(Message message) {
		System.out.println("Sending via Email");
		
	}

}
