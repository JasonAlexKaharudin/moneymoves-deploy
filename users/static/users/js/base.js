console.log("here I am at the beach")

//navbar animations, responsive navbar
const toggleBtn = document.getElementsByClassName('toggle-button')[0]
const navbarLinks = document.getElementsByClassName('navbar-links')[0]
const menuBtn = document.querySelector('.burgerbuns');
const navbar = document.querySelector('.navbar');
let menuOpen = false

toggleBtn.addEventListener('click', () => {
    if (!menuOpen){
        menuBtn.classList.add('open');
        navbarLinks.classList.remove('hidden');
        navbarLinks.classList.add('border-t-2');
        navbar.classList.remove('border-b-2');
        menuOpen = true;
    } else {
        menuBtn.classList.remove('open');
        navbarLinks.classList.add('hidden');
        navbarLinks.classList.remove('border-t-2');
        navbar.classList.add('border-b-2');
        menuOpen = false;
    }
})