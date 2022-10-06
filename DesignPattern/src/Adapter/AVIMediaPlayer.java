package Adapter;

public class AVIMediaPlayer implements AdvanceMediaPlayer {

	@Override
	public void play(AdvancedFormat advancedFormat) {
		System.out.println("Playing wtih AVIMediaPlayer "+advancedFormat.song+" with format "+advancedFormat.format+" with resolution "+advancedFormat.resolution);
		
	}

}
