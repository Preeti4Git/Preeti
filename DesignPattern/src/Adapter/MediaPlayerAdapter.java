package Adapter;

public class MediaPlayerAdapter implements MediaPlayer {
	AdvanceMediaPlayer advanceMediaPlayer;
	AdvancedFormat advancedFormat;
	
	public MediaPlayerAdapter(AdvancedFormat advancedFormat) {
		advanceMediaPlayer = new AVIMediaPlayer();
		this.advancedFormat = advancedFormat;
	}

	@Override
	public void play(String song, String format) {
		advancedFormat.setFormat(format);
		advancedFormat.setSong(song);
		advanceMediaPlayer.play(advancedFormat);
	}

	
	
	
}
