const aside = document.getElementById('aside');
function toggleMenu(){
 aside.classList.toggle('menu-open')
}
function closeMenu(){
 aside.classList.remove('menu-open')
}

//functionality of controllers in tables
const scrollContainer = document.getElementById('scrollContainer');
const content = document.getElementById('content');
const scrollLeftButton = document.getElementById('scrollLeftButton');
const scrollRightButton = document.getElementById('scrollRightButton');
const scrollAmount = 780; // Adjust the scroll distance as needed

scrollLeftButton.addEventListener('click', function () {
    scrollContainer.scrollLeft -= scrollAmount;
});

scrollRightButton.addEventListener('click', function () {
    scrollContainer.scrollLeft += scrollAmount;
});