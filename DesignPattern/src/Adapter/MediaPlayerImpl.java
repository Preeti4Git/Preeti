package Adapter;

public class MediaPlayerImpl implements MediaPlayer {
	MediaPlayer mediaPlayer;
	MediaPlayerAdapter mediaPlayerAdapter;
	AdvancedFormat advancedFormat;

	@Override
	public void play(String song, String format) {
		if(format == "MP3") {
			mediaPlayer = new MP3MediaPlayer();
			mediaPlayer.play(song, format);
		} else {
			advancedFormat = new AdvancedFormat();
			advancedFormat.setResolution("1080p");
			mediaPlayerAdapter = new MediaPlayerAdapter(advancedFormat);
			mediaPlayerAdapter.play(song, format);
		}
		
	}
	

}
