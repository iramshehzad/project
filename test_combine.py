import pandas as pd 
import openai
import os
import random
import datetime 
import glob
from pydub import AudioSegment
from moviepy.editor import AudioFileClip
from moviepy.audio.fx import all as afx
import pysrt
import boto3
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from pysrt import open as open_srt
from nltk.tokenize import sent_tokenize  
import subprocess
import json
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

def combine_audio_video(bg_video_file, bg_audio_file, speech_audio_file, output_file, aspect_ratio='9:16'):
    # load video clip
    video = VideoFileClip(bg_video_file)
    
    # load background audio clip and adjust its duration to match speech audio's duration
    bg_audio = AudioFileClip(bg_audio_file).fx(afx.volumex, 0.2)
    
    # load speech audio clip
    speech_audio = AudioFileClip(speech_audio_file)

    # loop video until it matches the speech audio's duration
    video = video.fx(vfx.loop, duration=speech_audio.duration)
    
    # adjust background audio's duration to match video's (new) duration
    bg_audio = bg_audio.fx(vfx.loop, duration=video.duration)

    # Resize video according to aspect ratio
    if aspect_ratio == '16:9':
        video = video.fx(vfx.resize, width=video.size[1]*16/9) if video.size[0]/video.size[1] < 16/9 else video.fx(vfx.resize, height=video.size[0]*9/16)
    elif aspect_ratio == '9:16':
        video = video.fx(vfx.resize, width=video.size[1]*9/16) if video.size[0]/video.size[1] > 9/16 else video.fx(vfx.resize, height=video.size[0]*16/9)

    # Combine background audio and speech audio
    combined_audio = CompositeAudioClip([bg_audio, speech_audio])

    # set audio of video to combined audio
    final_clip = video.set_audio(combined_audio)

    # write to file
    final_clip.write_videofile(output_file, codec='libx264')

    return final_clip

def time_to_seconds(time_obj):
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000

def create_subtitle_clips(subtitles, videosize, fontsize=80, font='Futura', color='black', debug = False):
    subtitle_clips = []

    for subtitle in subtitles:
        start_time = time_to_seconds(subtitle.start)
        end_time = time_to_seconds(subtitle.end)
        duration = end_time - start_time

        video_width, video_height = videosize
        
        text_clip = TextClip(subtitle.text, fontsize=fontsize, font=font, color=color,stroke_color='yellow', stroke_width=3,size=(video_width*3/4, None), method='caption').set_start(start_time).set_duration(duration)
        subtitle_x_position = 'center'
        subtitle_y_position = video_height*0.6

        text_position = (subtitle_x_position, subtitle_y_position)                    
        subtitle_clips.append(text_clip.set_position(text_position))

    return subtitle_clips


# Example usage
def render_video():
    combine_audio_video('static/video.mp4','static/bg_audio.mp3', 'static/voice.mp3',  'static/output.mp4',aspect_ratio='16:9')
    
    #subtitles('static/final_subtittle.srt','static/final_subtittle.srt')
    
    
    srtfilename =  'static/final_subtittle.srt'
    mp4filename =  'static/output.mp4'
    video = VideoFileClip(mp4filename)
    subtitles = pysrt.open(srtfilename, encoding='iso-8859-1')
    
    begin,end= mp4filename.split(".mp4")
    output_video_file = begin+'_subtitled'+".mp4"
    
    print ("Output file name: ",output_video_file)
    
        # Create subtitle clips
    subtitle_clips = create_subtitle_clips(subtitles,video.size)
    
        # Add subtitles to the video
    final_video = CompositeVideoClip([video] + subtitle_clips)
    
        # Write output video file
    final_video.write_videofile(output_video_file)