package BridgeDesignPattern;

public class TextMessage implements Message{
	String message;

	public TextMessage(String message) {
		this.message = message;
	}



	@Override
	public void sendMessage() {
		System.out.println("This is text message");
		
	}

}
