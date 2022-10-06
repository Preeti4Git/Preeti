package Adapter;

public class MP3MediaPlayer implements MediaPlayer {

	@Override
	public void play(String song, String format) {
		System.out.println("Playing with DefaultMediaPlayer "+song+" in format "+format);
		
	}

}
