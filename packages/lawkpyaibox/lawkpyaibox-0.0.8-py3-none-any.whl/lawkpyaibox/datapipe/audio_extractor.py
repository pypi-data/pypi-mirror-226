import moviepy.editor as audiomp


def extract_audio_from_video(videopaths, videoext='.mp4'):
    """
    videopath list
    """
    print("Start extract audio from videos")
    for videopath in videopaths:
        print(videopath)
        # 视频所在路径
        video = audiomp.VideoFileClip(videopath)
        audio = video.audio
        audio_savepath = videopath.replace(videoext, ".wav")
        audio.write_audiofile(audio_savepath)
    print("Finish extract audio")
