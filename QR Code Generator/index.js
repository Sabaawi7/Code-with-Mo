let content = document.getElementById("content");
let searchBtn = document.getElementById("generate-button")
let result = document.getElementById("result")

console.log(content)
let getQR =  () =>{
    let contentToBeSearched = content.value;
    let url = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=' + str(content);


    result.innerHTML = '<img src=${url}></img>'
    
}

let printContetn = () => {
    result.innerHTML = "<h3>${contenst}<\h3>"
}
searchBtn.addEventListener("click", printContetn);
window.addEventListener("load", getQR);