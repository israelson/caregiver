// Custom JavaScript functionality can be added here
document.addEventListener("DOMContentLoaded", function() {
    // Example: Highlighting active menu item
    let currentPath = window.location.pathname;
    let menuItems = document.querySelectorAll('.navbar-nav .nav-item .nav-link');

    menuItems.forEach(item => {
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
        }
    });
});
