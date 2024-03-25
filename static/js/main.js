document.addEventListener('DOMContentLoaded', function () {
const hamburger = document.querySelector('.hamburger');
const navItems = document.querySelector('.navbar-nav');

hamburger.addEventListener('click', function () {
    // Toggle the 'active' class instead of changing the style directly
    navItems.classList.toggle('active');
});

// Function to handle the resize event
function handleResize() {
    // If the window width is more than 768px and navItems contains the 'active' class
    if (window.innerWidth > 768 && navItems.classList.contains('active')) {
        // Remove the 'active' class and the inline 'display' style
        navItems.classList.remove('active');
        navItems.style.display = '';
    }
}

// Add event listener for the window resize event
window.addEventListener('resize', handleResize);
});

