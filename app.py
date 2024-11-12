import os
import csv
from flask import Flask, request, render_template, redirect, url_for
from model import predict
from graph import prepare_graph_data
from advice import get_gpt_response

# 定数定義
CSV_FILE_PATH = './static/new_texts/user_inputs.csv'



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])



def upload_user_files():
    if request.method == 'POST':
        try:
            combined_text = request.form.get('combined_text', '')
            text1 = request.form.get('text1', '')
            text2 = request.form.get('text2', '')

            # テキストをCSVに保存
            save_to_csv(text1, text2)

            # モデル予測
            result, probabilities, labels, top_index = predict(combined_text)
            graph_data = prepare_graph_data(probabilities, labels)

            # 最も高い確率の感情ラベル
            top_label = labels[probabilities.index(max(probabilities))]


            adviced_text = combined_text + "と言った彼女は" + result + "私はどのような対応をすべきですか。"
            advice = get_gpt_response(adviced_text)

            # 結果をテンプレートに渡す
            return render_template(
                'result.html', text = combined_text, result=result, graph_data=graph_data, top_label=top_label, top_index = top_index, advice=advice
            )
        except Exception as e:
            return render_template('result.html', result=f"エラー: {str(e)}")

    return render_template('index.html')



@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        # モーダルのフォームから取得
        correctness = request.form.get('correctness')
        emotion = request.form.get('emotion')
        top_index = request.form.get('top_label')  # 予測時のラベル

        # 「大丈夫かどうか」列に追加する値を決定
            
        if correctness == '間違い':
            feedback_value = emotion
        elif correctness == '分からない':
            feedback_value = 10
        else:
            feedback_value = top_index

        # CSVの最後の行にフィードバックを追加
        append_feedback_to_last_row(feedback_value)

        # トップページにリダイレクト
        return redirect(url_for('index'))
    except Exception as e:
        print(f"フィードバックエラー: {str(e)}")
        return redirect(url_for('index'))

def save_to_csv(text1, text2):
    try:
        file_exists = os.path.isfile(CSV_FILE_PATH)

        with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['どのような時', '何と言ったか', '大丈夫かどうか'])
            writer.writerow([text1, text2, ''])
    except IOError as e:
        print(f"CSV保存エラー: {str(e)}")
        raise

def append_feedback_to_last_row(feedback_value):
    try:
        # CSVの内容をすべて読み込み
        with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as file:
            rows = list(csv.reader(file))

        # 最後の行の「大丈夫かどうか」列にフィードバックを追加
        if len(rows) > 1:
            rows[-1][-1] = feedback_value

        # 修正した内容を再度CSVに書き込む
        with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    except IOError as e:
        print(f"CSV更新エラー: {str(e)}")
        raise

if __name__ == "__main__":
    app.run(debug=True)
