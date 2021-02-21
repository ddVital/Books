function addMobileMenu() {
    var screenSize = window.matchMedia("(max-width: 600px)")
    const header = document.querySelector('header');
            
    if (screenSize.matches) { // If media query matches
        header.innerHTML += `
            <nav class="mobile-menu">
                <a href="">
                    <i class="fas fa-home"></i>
                    <span>Home</span>
                </a>
                <a href="">
                    <i class="fas fa-books"></i>
                    <span>Books</span>
                </a>
                <a href="" class="mobile-menu-items">
                    <i class="fas fa-list"></i>
                    <span>Wishlist</span>
                </a>
                <a href="" class="mobile-menu-items">
                    <i class="fas fa-user"></i>
                    <span>user</span>
                </a>
            </nav>
        `;
    } else {
        const mobileMenu = document.querySelector('.mobile-menu');
        mobileMenu.remove()
    }
}