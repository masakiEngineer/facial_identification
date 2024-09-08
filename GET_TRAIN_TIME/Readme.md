# GetTrainTime.py について
## 目的(利用例)
会社から帰宅する前に、次の電車の発車時刻を取得することを目的  
どのくらいのスピードで歩けば次の電車に間に合うか、を把握することができる

## 前提
Chromeを使用してスクレイピングを行います。

## 手順

### ① Seleniumのインストール
以下のコマンドを使用してSeleniumをインストールします。

```bash
pip install selenium
```

### ②chrome ver.114のダウンロード
現在使用しているchromeのverが114出ない際は、chromeをダウンロード  
githubにchromev ver.114を掲載

### ③chrome ver.114に対応したchrome driverをダウンロード
githubにchrome driverを掲載

### ④GetTrainTime.pyの定義値を変更
- **driver = "chrome_driver_path"**  # chrome_driver ver.114  
  ダウンロードしたChrome Driverが格納されているパスを指定します。

- **出発駅 / 到着駅の指定**
  - `START_STATION`：出発駅名を指定します。
  - `END_STATION`：到着駅名を指定します。

- **最寄り駅までの所要時間を指定**
  - `COMPANY_TO_STATION`：最寄り駅までの所要時間（分）を指定します。

### ⑤GetTrainTime.pyを実行
```bash
python GetTrainTime.py
```

### ⑥ターミナル上に電車時刻を表示