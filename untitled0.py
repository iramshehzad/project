import requests
from pexelsapi.pexels import Pexels
import json
import pandas as pd
#import pafy

def get_video_link(querytext):
    pexel = Pexels('ViE8iveSR7T9rpjXUZa9pUCIjVc9YAGGzFMQjjM5pcC0ByBU3XIGphNF')
    video_list = pexel.search_videos(query=querytext, orientation='', size='', color='', locale='', page=1, per_page=15)
    video_list
    df =pd.DataFrame.from_dict(video_list["videos"])
    # df=pd.DataFrame.from_dict(df["video_files"])
    # df=pd.DataFrame.from_dict(df["link"])
    
    id_list=df[["id","duration","video_files","image"]]
    selected_list=[]
    for index, row in id_list.iterrows():
      if row["duration"]>30:
        selected_list.append([row["id"],row["video_files"]])
    
    return selected_list[0][1][0]["link"]
def download_video(querytext):
    url=get_video_link(querytext)
    file_path="static/video.mp4"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print('Video downloaded successfully.')
    else:
        print('Failed to download video.')


download_video("data science")