function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

async function fetchLanguages() {
    const sourceResponse = await fetch('/translate/source-languages');
    const targetResponse = await fetch('/translate/target-languages');

    const sourceLanguages = await sourceResponse.json();
    const targetLanguages = await targetResponse.json();

    const sourceSelect = document.getElementById('sourceLanguage');
    sourceLanguages.forEach(lang => {
        const option = document.createElement('option');
        option.value = lang.code;
        option.textContent = lang.name;
        sourceSelect.appendChild(option);
    });

    const targetSelect = document.getElementById('targetLanguage');
    targetLanguages.forEach(lang => {
        const option = document.createElement('option');
        option.value = lang.code;
        option.textContent = lang.name;
        targetSelect.appendChild(option);
    });
}

document.getElementById('detectionForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const text = document.getElementById('detectText').value;

    const response = await fetch('/detect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
    });

    const result = await response.json();

    document.getElementById('detectedLanguage').textContent = `Detected Language: ${result.detected_language}`;
});

document.getElementById('translationForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const text = document.getElementById('translateText').value;
    const targetLanguage = document.getElementById('targetLanguage').value;
    const sourceLanguage = document.getElementById('sourceLanguage').value;

    const response = await fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'text': text, 'source_language': sourceLanguage, 'target_language': targetLanguage })
    });

    const result = await response.json();

    document.getElementById('detectedLanguageTranslation').textContent = result.detected_language ? `Detected Language: ${result.detected_language}` : '';
    document.getElementById('translation').textContent = `Translation: ${result.translation}`;
});

// Open the default tab and fetch languages
document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('.tablink').click();
    fetchLanguages();
});
