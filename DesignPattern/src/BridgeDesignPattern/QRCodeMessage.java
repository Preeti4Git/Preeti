package BridgeDesignPattern;

public class QRCodeMessage implements Message {
	//NotificationService notificationService;
	
	/*
	 * public QRCodeMessage(NotificationService notificationService) {
	 * this.notificationService = notificationService; }
	 */


	@Override
	public void sendMessage() {
		System.out.println("This is QR Code message");
		//notificationService.sendNotification();
	}

}
