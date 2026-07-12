const button = document.getElementById("translateBtn");

const resultBox = document.getElementById("result");


button.addEventListener("click", async () => {


    const text = document.getElementById("text").value;

    const source_language = document.getElementById("source_language").value;

    const target_language = document.getElementById("target_language").value;

    const channel = document.getElementById("channel").value;

    const tone = document.getElementById("tone").value;



    resultBox.innerHTML = "⏳ Connecting with AI...";



    try {


        const response = await fetch("/translate", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },


            body: JSON.stringify({

                text: text,

                source_language: source_language,

                target_language: target_language,

                channel: channel,

                tone: tone

            })

        });



        const data = await response.json();


        resultBox.innerHTML = data.translated;



    } catch(error) {


        resultBox.innerHTML =
        "❌ Error connecting with server";


        console.error(error);

    }


});