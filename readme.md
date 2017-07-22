# ninnin

画像解析用スクリプト

## How to Use.

簡易画像スクレイピング

```
python web_crawler.py "https://search.yahoo.co.jp/image/search?ei=UTF-8&fr=sfp_as&aq=-1&oq=&ts=1609&p=%E9%A3%9F%E3%81%B9%E7%89%A9&meta=vc%3D" .jpeg,.jpg
```

スクレイピングで得た画像は
trainpic/XXX/ディレクトリを作成しその中に画像入れる



```
conda install -c conda-forge tensorflow
gem install rmagick
```

画像データからCSVデータを作成する

```
python gen_data_csv.py trainpic > train.csv
```

CSVからデータを作成

```
ruby gen_binary.rb train
```
