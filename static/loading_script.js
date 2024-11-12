function combineTexts() {
    const text1 = document.getElementById('text1').value;
    const text2 = document.getElementById('text2').value;
    const combinedText = text1 + " " + "「" + text2 + "」";
    document.getElementById('combined_text').value = combinedText;
}

function submitForm(event) {
    event.preventDefault();
    combineTexts();

    document.getElementById('loading').style.display = 'flex';

    const form = event.target;
    const formData = new FormData(form);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(html => {
        document.open();
        document.write(html);
        document.close();
    })
    .catch(error => {
        console.error('エラー:', error);
        alert('診断に失敗しました');
        document.getElementById('loading').style.display = 'none';
    });
}
