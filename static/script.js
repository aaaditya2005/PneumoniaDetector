let resultText = document.getElementById("result-text");
let resultBox = document.getElementById("result-box");
if (resultText.innerText.includes("Pneumonia")) {
    resultBox.classList.add("bg-red-500");
} else {
    resultBox.classList.add("bg-green-500");
}