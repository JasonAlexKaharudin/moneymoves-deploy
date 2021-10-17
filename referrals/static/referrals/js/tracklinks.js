fieldSV = document.getElementById("field-Sunday-Valley");
inputSV = document.getElementById("uniqueLink-Sunday-Valley");
copySV = document.getElementById("copyBtn-Sunday-Valley");

fieldJ = document.getElementById("field-Jemaime");
inputJ = document.getElementById("uniqueLink-Jemaime");
copyJ = document.getElementById("copyBtn-Jemaime");

fieldDNC = document.getElementById("field-Do-Not-Cross");
inputDNC = document.getElementById("uniqueLink-Do-Not-Cross");
copyDNC = document.getElementById("copyBtn-Do-Not-Cross");

const myInp = document.getElementById("inputRef");
const username = myInp.getAttribute("username");
const btnCopy = document.getElementById("copyBtnRef");

let numOfClicks = 0;

//functions
function copyToClipboard(field, input, copy){
    copy.onclick = ()=>{
        input.select(); //select input value
        if(document.execCommand("copy")){ //if the selected text copy
            field.classList.add("active");
            copy.innerText = "Copied";
            setTimeout(()=>{
            window.getSelection().removeAllRanges(); //remove selection from document
            field.classList.remove("active");
            copy.innerText = "Copy";
            }, 3000);
        }
        
        trackClicks();
    }
}

function trackClicks(){
    numOfClicks = numOfClicks + 1;
    console.log(numOfClicks)
}

async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return response.json();
}

// Event listeners
btnCopy.onclick = function(){
    myInp.select();
    trackClicks();
    document.execCommand("Copy");
}

window.addEventListener('beforeunload', function(){
    if (numOfClicks == 0){
    ;
    } else{
        try {
            postData('https://moneymoves.app/api/links/', { 
            clicks: numOfClicks,
            username: username
        })
            .then(data => {
                console.log(data);
            });
        } catch (err) {
            console.log(err)
        }
    }
})

//function calls
copyToClipboard(fieldJ, inputJ, copyJ);
copyToClipboard(fieldDNC, inputDNC, copyDNC);
copyToClipboard(fieldSV, inputSV, copySV);