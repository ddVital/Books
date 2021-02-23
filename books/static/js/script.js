window.addEventListener('DOMContentLoaded', (event) => {
    addMobileMenu()
})

var screenWidth = window.innerWidth;
window.addEventListener("resize", addMobileMenu);

function addMobileMenu() {
    console.log(window.innerWidth);
    const header = document.querySelector('header');
    const mobileMenu = document.querySelector('.mobile-menu');

    if (window.innerWidth <= 600) {
        if (mobileMenu === null) {

            header.innerHTML += `
                <nav class="mobile-menu">
                    <a href="{% url 'index' %}" class="mobile-menu-items {% if request.path == index %}active{% endif %}">
                        <i class="fas fa-home"></i>
                        <span>Home</span>
                    </a>
                    <a href="{% url 'books' %}" class="mobile-menu-items {% if request.path == books %}active{% endif %}">
                        <i class="fas fa-books"></i>
                        <span>Books</span>
                    </a>
                    <a href="{% url 'want_to_read' %}" class="mobile-menu-items {% if request.path == want_to_read %}active{% endif %}">
                        <i class="fas fa-list"></i>
                        <span>Wishlist</span>
                    </a>
                    <a href="{% url 'profile' %}" class="mobile-menu-items {% if request.path == profile %}active{% endif %}">
                        <i class="fas fa-user"></i>
                        <span>user</span>
                    </a>
                </nav>
            `; 
        }
    } else {
        if (mobileMenu) {
            mobileMenu.remove();
        }
    }
}