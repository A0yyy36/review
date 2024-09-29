import os
import PySimpleGUI as sg

# レビューを保存するファイル
review_file = 'review_list.txt'

# ユーザーが選べる選択肢
choices = ['追加', '表示', '編集', '削除', '終了']

# GUIレイアウト
layout = [
    [sg.Text("書籍の評価システム")], 
    [sg.Listbox(choices, size=(15, len(choices)), key='choice')], 
    [sg.Button('実行', key='btn')],
    [sg.Multiline(size=(100, 15), key='output', disabled=True)]  # 出力用のテキストボックス
]

# ウィンドウの作成
win = sg.Window('書籍評価アプリ', layout, font=(None, 14), size=(850, 500))

# レビューをファイルから読み込む関数
def load_reviews():
    if os.path.exists(review_file):
        with open(review_file, 'r') as file:
            reviews = file.readlines()
        reviews = [review.strip() for review in reviews if review.strip() != "------------------------------------------------------------------------"]
    else:
        reviews = []
    return reviews

# レビューをファイルに保存する関数
def save_reviews(reviews):
    with open(review_file, 'w') as file:
        for review in reviews:
            file.write(review + '\n')
            file.write("------------------------------------------------------------------------\n")

# レビューを追加する関数
def add_review(reviews, date, name, rating, comment):
    review = f"日時： {date}｜名前： {name}｜評価： {rating}｜感想： {comment}"
    reviews.append(review)
    save_reviews(reviews)

# レビューを編集する関数
def edit_review(reviews, index, date, name, rating, comment):
    if 0 <= index < len(reviews):  # インデックスが有効か確認
        review = f"日時： {date}｜名前： {name}｜評価： {rating}｜感想： {comment}"
        reviews[index] = review  # 指定したインデックスのレビューを更新
        save_reviews(reviews)    # 更新後のリストを保存
    else:
        print("指定されたインデックスは無効です")


# レビューを削除する関数
def delete_review(reviews, index):
    if 0 <= index < len(reviews):
        reviews.pop(index)
        save_reviews(reviews)

# メインのGUIイベントループ
reviews = load_reviews()

while True:
    event, values = win.read()
    
    #windowを閉じる方法
    if event == sg.WIN_CLOSED or (event == 'btn' and values['choice'][0] == '終了'):
        break

    elif event == 'btn':
        choice = values['choice'][0]
        
        if choice == '追加':
            # 新しいレビューを追加
            date = sg.popup_get_text("読み終えた日時(YYYY/MM/DD)： ", title="Date")
            if date is None:  # キャンセルが押されたら選択画面に戻る
                continue
            
            name = sg.popup_get_text("本の名前： ", title="Name")
            if name is None:  # キャンセルが押されたら選択画面に戻る
                continue

            # 星評価の選択ボックスをコンボボックスで表示
            stars = ['☆1', '☆2', '☆3', '☆4', '☆5']
            layout_rating = [
                [sg.Text("評価を選んでください")],
                [sg.Combo(stars, key='star', size=(42, 1), readonly=True)],  # コンボボックスに変更
                [sg.Button('Ok', size=(6, 1), key='confirm'), sg.Button('Cancel', size=(6, 1), key='cancel')]
            ]

            rating_win = sg.Window('Rate', layout_rating)

            # 星評価の入力処理
            while True:
                event_rating, values_rating = rating_win.read()
                
                if event_rating == sg.WIN_CLOSED or event_rating == 'cancel':
                    rating_win.close()
                    rating = None  # キャンセルが押されたらNoneにする
                    break

                elif event_rating == 'confirm' and values_rating['star']:
                    rating = values_rating['star']  # 選択された評価を取得
                    rating_win.close()
                    break

            if rating is None:  # キャンセルが押されたら選択画面に戻る
                continue

            comment = sg.popup_get_text("感想: ", title="Comment")
            if comment is None:  # キャンセルが押されたら選択画面に戻る
                continue

            if date and name and rating and comment:
                add_review(reviews, date, name, rating, comment)
                win['output'].update("レビューが追加されました。")
            else:
                win['output'].update("全てのフィールドを入力してください。")


        elif choice == '表示':
            # 全てのレビューを表示
            display_text = "\n------------------------------------------------------------------------------\n".join([f"{i}： {review}" for i, review in enumerate(reviews, start=1)])  # 1から始める
            win['output'].update(display_text)


        elif choice == '編集':
            if reviews:  # レビューが存在するか確認
                index_str = sg.popup_get_text("編集するレビュー番号を入力してください: ")
                if index_str and index_str.isdigit():
                    index = int(index_str) - 1  # 1から始まる番号を0から始まるインデックスに変換
                    if 0 <= index < len(reviews):  # 有効なインデックスか確認
                        
                        # 編集対象のレビューをパース
                        current_review = reviews[index]
                        # 仮のフォーマットから情報を分割して取得 (元のフォーマットに合わせてパースする)
                        parts = current_review.split('｜')
                        date = parts[0].replace("日時： ", "")
                        name = parts[1].replace("名前： ", "")
                        rating = parts[2].replace("評価： ", "")
                        comment = parts[3].replace("感想： ", "")

                        # 日時入力 (元の内容を初期値として表示)
                        date = sg.popup_get_text("読み終えた日時(YYYY/MM/DD)： ", title="Date", default_text=date)
                        if date is None:  # キャンセルが押されたら選択画面に戻る
                            continue
                        
                        # 名前入力 (元の内容を初期値として表示)
                        name = sg.popup_get_text("本の名前： ", title="Name", default_text=name)
                        if name is None:  # キャンセルが押されたら選択画面に戻る
                            continue

                        # 星評価の選択ボックスをコンボボックスで表示 (元の評価を初期値として設定)
                        stars = ['☆1', '☆2', '☆3', '☆4', '☆5']
                        layout_rating = [
                            [sg.Text("評価を選んでください")],
                            [sg.Combo(stars, key='star', size=(42, 1), readonly=True, default_value=rating)],  # デフォルト値に元の評価をセット
                            [sg.Button('Ok', size=(6, 1), key='confirm'), sg.Button('Cancel', size=(6, 1), key='cancel')]
                        ]

                        rating_win = sg.Window('Rate', layout_rating)

                        # 星評価の入力処理
                        while True:
                            event_rating, values_rating = rating_win.read()
                            
                            if event_rating == sg.WIN_CLOSED or event_rating == 'cancel':
                                rating_win.close()
                                rating = None  # キャンセルが押されたらNoneにする
                                break

                            elif event_rating == 'confirm' and values_rating['star']:
                                rating = values_rating['star']  # 選択された評価を取得
                                rating_win.close()
                                break

                        if rating is None:  # キャンセルが押されたら選択画面に戻る
                            continue

                        # 感想入力 (元の内容を初期値として表示)
                        comment = sg.popup_get_text("感想： ", title="Comment", default_text=comment)
                        if comment is None:  # キャンセルが押されたら選択画面に戻る
                            continue

                        # 全てのフィールドが入力されている場合、レビューを編集する
                        if date and name and rating and comment:
                            # ここで編集されたレビューを保存する
                            edit_review(reviews, index, date, name, rating, comment)
                            win['output'].update("レビューが編集されました。")
                        else:
                            win['output'].update("全てのフィールドを入力してください。")
                    else:
                        win['output'].update("無効な番号です。")
                else:
                    win['output'].update("有効な番号を入力してください。")
            else:
                win['output'].update("編集できるレビューが存在しません。")



        elif choice == '削除':
            # 指定したレビューを削除
            if reviews:
                index_str = sg.popup_get_text("削除するレビュー番号を入力してください: ")
                if index_str and index_str.isdigit():
                    index = int(index_str) - 1  # 1から始まる番号を0から始まるインデックスに変換
                    if 0 <= index < len(reviews):
                        delete_review(reviews, index)
                        win['output'].update(f"レビュー {index + 1} が削除されました。")  # 表示は1から始まるように
                    else:
                        win['output'].update("無効な番号です。")
                else:
                    win['output'].update("有効な番号を入力してください。")
            else:
                win['output'].update("削除できるレビューがありません。")


# ウィンドウを閉じる
win.close()
