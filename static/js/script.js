document.getElementById("generateBtn").addEventListener("click", function () {
    const code = document.getElementById("codeInput").value;

    if (!code.trim()) {
        alert("Please enter some code!");
        return;
    }

    fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: code }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("dotOutput").textContent = "Error: " + data.error;
            document.getElementById("diagramOutput").innerHTML = "";
        } else {
            document.getElementById("dotOutput").textContent = data.dot_code;
            document.getElementById("diagramOutput").innerHTML = data.diagram;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong!");
    });
});
