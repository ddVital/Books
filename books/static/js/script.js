window.addEventListener('DOMContentLoaded', (event) => {
    addMobileMenu()
})

var screenWidth = window.innerWidth;
window.addEventListener("resize", addMobileMenu);

function addMobileMenu() {
    const header = document.querySelector('header');
    const mobileMenu = document.querySelector('.mobile-menu');

    if (window.innerWidth <= 600) {
        if (mobileMenu === null) {

            header.innerHTML += mobileMenuContent 
        }
    } else {
        if (mobileMenu) {
            mobileMenu.remove();
        }
    }
}