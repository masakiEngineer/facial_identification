import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from googleapiclient.discovery import build
import requests
from io import BytesIO
import webbrowser

# YouTube Data APIのAPIキー
API_KEY = ''

# YouTube Data APIを使うためのセットアップ
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_info(channel_id):
    response = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    ).execute()

    channel_info = response['items'][0]
    channel_title = channel_info['snippet']['title']
    subscriber_count = channel_info['statistics'].get('subscriberCount', 'N/A')

    return channel_title, subscriber_count

def get_latest_videos(channel_id, max_results=5):
    response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()
    
    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    playlist_response = youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_playlist_id,
        maxResults=max_results
    ).execute()

    videos = []
    for item in playlist_response['items']:
        video_title = item['snippet']['title']
        video_id = item['snippet']['resourceId']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        thumbnail_url = item['snippet']['thumbnails']['high']['url']
        
        video_response = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()
        
        statistics = video_response['items'][0]['statistics']
        like_count = statistics.get('likeCount', 'N/A')
        view_count = statistics.get('viewCount', 'N/A')
        
        videos.append({
            'title': video_title,
            'url': video_url,
            'like_count': like_count,
            'view_count': view_count,
            'thumbnail': thumbnail_url
        })
    
    return videos

# GUIアプリケーションのセットアップ
def open_video(url):
    webbrowser.open(url)

def create_gui(channel_id):
    root = tk.Tk()
    root.title('YouTube Channel Info')
    root.geometry('800x600')  # ウィンドウサイズを設定

    # スクロールバーを設定
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # チャンネル情報を取得
    channel_title, subscriber_count = get_channel_info(channel_id)
    
    # チャンネル名と登録者数を表示
    tk.Label(scrollable_frame, text=f'チャンネル名: {channel_title}', font=('Helvetica', 18, 'bold')).pack(pady=10)
    tk.Label(scrollable_frame, text=f'チャンネル登録者数: {subscriber_count}', font=('Helvetica', 14)).pack(pady=5)
    
    # 最新動画情報を取得
    latest_videos = get_latest_videos(channel_id)

    for video in latest_videos:
        frame = ttk.Frame(scrollable_frame, padding=10)
        frame.pack(fill='x', padx=10, pady=5)
        
        # サムネイル画像の表示
        response = requests.get(video['thumbnail'])
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((160, 90), Image.LANCZOS)  # LANCZOSを使用してリサイズ
        img_tk = ImageTk.PhotoImage(img)
        
        img_label = tk.Label(frame, image=img_tk, cursor="hand2")
        img_label.image = img_tk
        img_label.grid(row=0, column=0, rowspan=3, padx=5, pady=5)
        
        # 動画タイトル
        tk.Label(frame, text=f'タイトル: {video["title"]}', font=('Helvetica', 12, 'bold')).grid(row=0, column=1, sticky='w')
        
        # 高評価数
        tk.Label(frame, text=f'高評価数: {video["like_count"]}', font=('Helvetica', 12)).grid(row=1, column=1, sticky='w')
        
        # 再生数
        tk.Label(frame, text=f'再生数: {video["view_count"]}', font=('Helvetica', 12)).grid(row=2, column=1, sticky='w')
        
        # サムネイルクリックで動画を開く
        img_label.bind("<Button-1>", lambda e, url=video['url']: open_video(url))

    root.mainloop()

# チャンネルIDを指定
channel_id = 'UCTW2tw0Mhho72MojB1L48IQ'
create_gui(channel_id)
