const fileInput = document.getElementById("fileInput");
const browseBtn = document.getElementById("browseBtn");
const preview = document.getElementById("preview");
const predictBtn = document.getElementById("predictBtn");
const loader = document.getElementById("loader");
const result = document.getElementById("result");
const diseaseText = document.getElementById("disease");
const progress = document.getElementById("progress");
const confidenceText = document.getElementById("confidenceText");

let selectedFile = null;

browseBtn.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
    selectedFile = fileInput.files[0];
    showPreview(selectedFile);
});

function showPreview(file) {
    const reader = new FileReader();
    reader.onload = () => {
        preview.innerHTML = `<img src="${reader.result}" />`;
    };
    reader.readAsDataURL(file);
}

predictBtn.addEventListener("click", async () => {
    if (!selectedFile) return alert("Upload image first!");

    const formData = new FormData();
    formData.append("file", selectedFile);

    loader.classList.remove("hidden");
    result.classList.add("hidden");

    try {
        const response = await fetch("http://localhost:5000/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        loader.classList.add("hidden");

        diseaseText.innerText = `Disease: ${data.prediction}`;
        confidenceText.innerText = `Confidence: ${data.confidence}%`;

        result.classList.remove("hidden");

        setTimeout(() => {
            progress.style.width = data.confidence + "%";
        }, 200);

    } catch (error) {
        alert("Backend not running!");
        loader.classList.add("hidden");
    }
});