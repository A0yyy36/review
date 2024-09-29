# 書籍記録プログラム
## 概要
このプログラムは，書籍の記録を簡単に追加・表示・削除できるコンソールアプリケーションです．評価は指定されたテキストファイルに保存され，プログラムの再起動後も保持されます．

## 使用方法
### 必要環境
- Python: Python 3.11.0がインストールされていることを確認してください．
- ライブラリ: os

### 使用方法
1. 必要なファイル
このプログラムは，記録を保存するために'review_list.txt'というファイルを使用します．プログラムが初めて実行されるとき，このファイルが存在しない場合は自動的に作成されます．
2. 実行手順
   1. プログラムの起動: 
      ```bash
      python your_program.py
      ```
   2. コマンド入力:
   プログラムが起動すると，コマンドを入力するプロンプトが表示されます．利用できるコマンドは以下の通りです：
      - '追加': 新しい記録を追加します．
      - '表示': 保存されたすべての記録を表示します．
      - '削除': 特定の記録を削除します．
      - '終了': プログラムを終了します．
   3. コマンドの詳細
      - 追加: '追加'コマンドを入力すると，以下の情報を順に入力する必要があります．
        - '読み終えた日時': YYYY/MM/DD形式で入力します．
        - '本の名前': 書籍のタイトルを入力します．
        - '評価': ☆1~☆5の範囲で入力します．
        - '感想': 書籍に関する感想を入力します．
      
        ![element](add.png)
      - 表示: '表示'コマンドを入力すると，すべての記録がインデックス番号付きで表示されます．
        ![element](print.png)
      - 削除: '削除'コマンドを入力すると，削除したい記録のインデックス番号を入力するように求められます．番号を入力すると，その記録がリストから削除されます．
        ![element](delete.png)
      - 終了: '終了'コマンドを入力すると，プログラムが終了します．
   4. ファイルの構造
   記録は'review_list.txt'に以下の形式で保存されます．
   ```markdown
   日時: YYYY/MM/DD｜名前: 書籍名｜評価: ☆1~5｜感想: 感想文
   ----------------------------------------------------------
   ```

## コードの説明
1. 記録の読み込み: 'review_list.txt'ファイルが孫座愛する場合，その内容を読み込みます．
```python
def load_reviews():
    if os.path.exists(review_file):
        with open(review_file, 'r') as file:
            reviews = file.readlines()
        reviews = [review.strip() for review in reviews if review.strip() != "------------------------------------------------------------------------"]
    else:
        reviews = []
    return reviews
```
2. 記録の保存: リストに保存された記録を review_list.txt ファイルに書き込みます．
```python
def save_reviews(reviews):
    with open(review_file, 'w') as file:
        for review in reviews:
            file.write(review + '\n')
            file.write("------------------------------------------------------------------------\n")
```
3. 記録の追加・削除: 記録の追加・削除コマンドを作ります．
```python
def add_review(reviews, date, name, rating, comment):
    review = f"日時: {date}｜名前: {name}｜評価: {rating}｜感想: {comment}"
    reviews.append(review)
    save_reviews(reviews)

def delete_review(reviews, index):
    if 0 <= index < len(reviews):
        reviews.pop(index)
        save_reviews(reviews)
```
4. メインプログラム: ユーザーからのコマンドを受け取り、それに応じて適切な処理を行います．
```python
def main():
    reviews = load_reviews()

    while True:
        command = input("コマンドを入力してください(追加，表示，削除，終了): ")
        if command == '終了':
            break

        elif command == '追加':
            date = input("読み終えた日時(YYYY/MM/DD): ")
            name = input("本の名前: ")
            rating = input("評価(☆ 1~5): ☆ ")
            comment = input("感想: ")
            add_review(reviews, date, name, rating, comment)

        elif command == '表示':
            for i, review in enumerate(reviews):
                print(f"{i}: {review}")

        elif command == '削除':
            index = int(input("削除するreviewの番号を入力してください: "))
            delete_review(reviews, index)

        else:
            print("無効なコマンドです．")
```

## 使用用途
### 読書記録の管理
本を読み終えた後，その本のタイトル，読了日，放火，感想を記録することで，自分が読んだ本の履歴を管理できます．これにより，どの本をいつ読んだかを簡単に振り返ることが出来ます．
### 読書習慣の追跡
読書の習慣を持っている人が，日々の読書活動を継続的に記録するのに便利です．読んだ本のリストを時系列で保存し，読書の進捗や傾向を把握することが出来ます．
### 感想の整理
読んだ本に対する感想や評価を記録しておくことで，将来的にその本について誰かと話すときや再読する際に参考にできます．また，記録しておくことで，自分の読書に対する理解や意見の変遷を追跡することもできます．

## 今後の展望
### 評価順ソート機能
保存された評価で評価点が良かった順・悪かった順にソートして，評価の良かった・悪かった本をすぐに見つけられるようにしたいです．
### 記録の編集機能
- [x] 一度保存した記録に対して，内容の修正や評価の変更が簡単に行えるように，既存の記録を編集する機能を追加したいです．
### GUI
- [x] プログラムにGUIを導入して，コマンドラインではなく視覚的に操作できるインタフェースを提供したいです．これにより，操作が直観的になり，さらに使いやすくなると考えます．
### 記録のタグ付けとカテゴリ分け
記録にタグを付けたり，ジャンルやテーマごとにカテゴリ分けを行う機能を追加したいです．これによって，記録の整理や特定のジャンルの本の記録を簡単に参照できるようになります．
