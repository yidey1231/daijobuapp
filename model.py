import torch
from transformers import BertJapaneseTokenizer,BertForSequenceClassification

# モデルとトークナイザーの読み込み
model_path = "saved_model_1"
tokenizer = BertJapaneseTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval()  # モデルを評価モードに切り替え

def predict(new_text):
    # 入力テキストのトークン化
    inputs = tokenizer(
        new_text,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )

    # 予測の実行
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits  # ロジットを取得
        probabilities = torch.softmax(logits, dim=-1).squeeze()  # Tensorのまま処理

    labels = {
        0: "本当に大丈夫みたいです。",
        1: "怒っています。",
        2: "悲しんでいるはず。",
        3: "呆れています。",
        4: "寂しいと感じています。",
        5: "嫉妬しています。",
        6: "放っておいて欲しいみたいです。",
        7: "疲れているはずです。",
        8: "戸惑っているみたいです。",
        9: "感情を予測できませんでした。"
    }

    emothion = {
        0: "本当に大丈夫",
        1: "怒り",
        2: "悲しみ",
        3: "呆れ",
        4: "寂しい",
        5: "嫉妬",
        6: "放っておいて",
        7: "疲れ",
        8: "戸惑い",
        9: "その他"
    }

    # 最も高いスコアのラベルを選択
    result = labels[torch.argmax(probabilities).item()]
    #最も高いスコアのキーを取得
    top_index = torch.argmax(probabilities).item()

    # 感情ラベルのリストを作成
    emotion_labels = list(emothion.values())

    # 確率をリストに変換して返す
    return result, probabilities.tolist(), emotion_labels , top_index
