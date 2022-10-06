package BridgeDesignPattern;

public class SMS implements NotificationService{

	@Override
	public void sendNotification(Message message) {
		System.out.println("Sending via SMS");
		
	}

}
