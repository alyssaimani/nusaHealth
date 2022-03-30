function Dropdown() {
    var content = document.getElementById("dropdown-content");
    if(content.style.display === "none") {
        content.style.display = "block";
    }
    else {
        content.style.display = "none";
    }
}

const searchBox = document.querySelector(".search-box input");
const optionList = Array.from(document.getElementsByClassName("option"));



searchBox.addEventListener("keyup", function(e){
    filterList(e.target.value);
});


const filterList = searchTerm => {
    searchTerm = searchTerm.toLowerCase();
    optionList.forEach(option=>{
        if(option.querySelector(`input[type='checkbox']`).value.toLowerCase().search(searchTerm) < 0){
            option.style.display = 'none';
        }
        else{
            option.style.display = 'block';
        }
    });
}

