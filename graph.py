import json

def prepare_graph_data(probabilities, labels):
    # 確率とラベルを大きい順にソート
    sorted_data = sorted(zip(probabilities, labels), reverse=True)
    sorted_probabilities, sorted_labels = zip(*sorted_data)

    # サイトのデザインに合わせた新しい色設定
    colors = [
        "rgba(255, 105, 180, 0.8)",  # HotPink
        "rgba(255, 20, 147, 0.8)",   # DeepPink
        "rgba(219, 112, 147, 0.8)",  # PaleVioletRed
        "rgba(255, 69, 0, 0.8)",     # Red
        "rgba(255, 99, 71, 0.8)",    # Tomato
        "rgba(255, 127, 80, 0.8)",   # Coral
        "rgba(255, 140, 0, 0.8)",    # DarkOrange
        "rgba(255, 215, 0, 0.8)",    # Gold
        "rgba(218, 165, 32, 0.8)",   # GoldenRod
        "rgba(240, 128, 128, 0.8)"   # LightCoral
    ]

    # Chart.js用のデータを作成
    data = {
        "labels": sorted_labels,
        "datasets": [{
            "label": "感情の確率分布",
            "data": sorted_probabilities,
            "backgroundColor": colors[:len(sorted_probabilities)],
            "borderColor": colors[:len(sorted_probabilities)],
            "borderWidth": 1
        }]
    }
    return json.dumps(data)
