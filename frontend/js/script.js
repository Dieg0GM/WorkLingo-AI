const translateBtn = document.getElementById("translateBtn");

translateBtn.addEventListener("click", async () => {

    const message = document.getElementById("message").value;
    const source = document.getElementById("source").value;
    const target = document.getElementById("target").value;
    const channel = document.getElementById("channel").value;
    const tone = document.getElementById("tone").value;

    const response = await fetch("/translate", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            text: message,
            source_language: source,
            target_language: target,
            channel: channel,
            tone: tone

        })

    });

    const data = await response.json();

    document.getElementById("result").innerText = data.translated;

});