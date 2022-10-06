package Adapter;

public class MainImplementer {
	public static void main(String[] args) {
		MediaPlayer mediaPlayer = new MediaPlayerImpl();
		mediaPlayer.play("test", "AVI");
	}
}
