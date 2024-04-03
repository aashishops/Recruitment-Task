from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def animate_text(text, duration, start_time, position=('center', 'center'), fontsize=50, color='white'): 
    # the text to be animated, duration of the text, start time and position of the text, font size and font color
  
  
    return TextClip(text, fontsize=fontsize, color=color).set_position(position).set_duration(duration).set_start(start_time)

def add_text_to_video(video_path, text_script, output_path):
    # Loading the video file and disable audio processing
    video_clip = VideoFileClip(video_path, audio=False)
    # Generate text clips based on the provided script
    text_clips = [animate_text(text, duration, start_time) for text, start_time, duration in text_script]
    
    # Overlay text clips onto the video
    final_clip = CompositeVideoClip([video_clip] + text_clips)
    
    # Writing the final video with overlaid text to the specified output path
    final_clip.write_videofile(output_path, codec='libx264')

# Example usage
if __name__ == "__main__":
    video_path = "E:/Career/internship/recruitment task/Text into Video/video/video.mp4"
    text_script = [("Hello ", 2, 3), ("Text", 6, 4)]  # Format: (text, start_time, duration)
    output_path = "E:/Career/internship/recruitment task/Text into Video/output/output.mp4"
    add_text_to_video(video_path, text_script, output_path)
