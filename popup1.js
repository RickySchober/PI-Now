
const addResponse = () => {
    const response = document.getElementById("response");
    const newSearchResponse = document.createElement("div");
    newSearchResponse.textContent = "yo";
    newSearchResponse.className = "searchResponse";
    response.appendChild(newSearchResponse);
}

document.getElementById("search-button").addEventListener("click", () =>{
    const response = document.getElementById("response");
    while(response.firstChild){
        response.removeChild(response.firstChild);
    }
    const newSearchResponse = document.createElement("div");
    newSearchResponse.textContent = "awaiting fetch response...";
    newSearchResponse.className = "searchResponse";
    response.appendChild(newSearchResponse);

    fetch('http://localhost:5000/data')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text(); 
    })
    .then(data => {
        console.log(data);
        addResponse();
    })
    .catch(error => {
        console.error('Error:', error);
    });
});