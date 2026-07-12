const textBox = document.getElementById("text");

const resultBox = document.getElementById("result");

const statusBox = document.getElementById("status");


let timer;



textBox.addEventListener("input", () => {


    clearTimeout(timer);



    timer = setTimeout(() => {


        translate();


    }, 800);



});





async function translate() {


    const text = textBox.value.trim();



    if (text === "") {

        resultBox.innerHTML = "Translation will appear here...";

        statusBox.innerHTML = "";

        return;

    }



    const source_language =
        document.getElementById("source_language").value;


    const target_language =
        document.getElementById("target_language").value;


    const channel =
        document.getElementById("channel").value;


    const tone =
        document.getElementById("tone").value;

    const mode = 
        document.getElementById("mode").value;

    const model = 
        document.getElementById("ai_model").value;


    statusBox.innerHTML ="🤖 Gemini is thinking...";


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

                tone: tone,
                
                mode: mode,
                
                model: model
            })


        });



     const data = await response.json();




    if (data.error) {


    result.innerHTML = `
        ⚠️ ${data.error}
    `;


    statusBox.innerHTML =
        "⚠️ Gemini unavailable";


    } else {


    result.innerHTML = data.translated;


    statusBox.innerHTML =
        "✅ Translation completed";


    }

    
} 

    catch(error) {
   


        console.error(error);



        statusBox.innerHTML =
            "❌ Connection error";


    }


}







// Advanced options


const advancedBtn =
    document.getElementById("advancedBtn");


const advancedPanel =
    document.getElementById("advancedPanel");



advancedPanel.style.display = "none";



advancedBtn.addEventListener("click", () => {


    if (advancedPanel.style.display === "none") {


        advancedPanel.style.display = "block";


        advancedBtn.innerHTML =
        "⚙ Advanced Options ▲";


    }

    else {


        advancedPanel.style.display = "none";


        advancedBtn.innerHTML =
        "⚙ Advanced Options ▼";


    }


});