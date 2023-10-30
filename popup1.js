
const addResponseElement = (element) => {
    const newSearchResponse = document.createElement("div");
    newSearchResponse.textContent = "yo";
    newSearchResponse.className = "searchResponse";
    response.appendChild(newSearchResponse);
}
const addResponse = (data, resultElement) => {
    for(let  i = 0; i<jsonSize; i++){
        addResponseElement(data[i], resultElement);
    }
}

document.getElementById("search-button").addEventListener("click", () =>{
    const responseElement = document.getElementById("response");
    while(responseElement.firstChild){
        responseElement.removeChild(response.firstChild);
    }
    const newSearchResponse = document.createElement("div");
    newSearchResponse.textContent = "awaiting fetch response...";
    newSearchResponse.className = "wait message";
    responseElement.appendChild(newSearchResponse);

    fetch('http://localhost:5000/data')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text(); 
    })
    .then(data => {
        console.log(data);
        const jsonData = JSON.parse(data);
        addResponses(jsonData, responseElement);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});