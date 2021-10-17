// get modal 

var modal = document.getElementById("simpleModal");
var modalBtn = document.getElementById("modelBtn-tm");
var closeBtn = document.getElementsByClassName("closeBtn-tm")[0];

modalBtn.addEventListener('click', openModal);
closeBtn.addEventListener('click', closeModal);
window.addEventListener('click', clickOutside);

function openModal(){
    modal.style.display = 'block';
}

function closeModal(){
    modal.style.display = 'none';
}

function clickOutside(e){
    if(e.target == modal){
        modal.style.display = 'none';
    }
}