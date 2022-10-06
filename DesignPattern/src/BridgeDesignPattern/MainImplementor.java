package BridgeDesignPattern;

public class MainImplementor {
	public static void main(String[] args) {
		NotificationService notificationService = new SMS();
		Message textMessage = new TextMessage("hi");
		notificationService.sendNotification(textMessage);
		QRCodeMessage qrMessage = new QRCodeMessage();
		notificationService.sendNotification(qrMessage);
		
		NotificationService emailNotificationService = new Email();
		emailNotificationService.sendNotification(qrMessage);
	}
}
