# 概要

このプロジェクトは、YouTubeチャンネルの情報と最新動画を表示するGUIアプリケーションです。サムネイル、タイトル、高評価数、再生数を表示します。サムネイルをクリックすると、動画がブラウザで開きます。

## 必要なもの

- Python 3.x
- YouTube Data APIキー

## Pythonパッケージ

- `google-api-python-client`
- `Pillow`

```bash
pip install google-api-python-client pillow
```

## セットアップ手順
1. YouTube Data APIキーの取得  
Google Cloud ConsoleからYouTube Data APIキーを取得します。

2. APIキーの設定  
プロジェクトの main.py ファイルを開き、API_KEY 変数に取得したAPIキーを設定します。

3. コードの実行  
ターミナルまたはコマンドプロンプトを開き、以下のコマンドでPythonスクリプトを実行します

```bash
python main.py
```

4. アプリケーションの操作
- GUIが表示され、指定したYouTubeチャンネルの情報と最新の動画が表示されます。
- 動画のサムネイルをクリックすると、ブラウザで動画が開きます。


