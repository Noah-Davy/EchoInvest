document.addEventListener('DOMContentLoaded', function () {
  const hamburger = document.querySelector('.hamburger');
  const navItems = document.querySelector('.navbar-nav');

  // Find the FAQ link and attach a click event listener for smooth scrolling
  const faqLink = document.querySelector('a[href$="#faq"]'); // Select the link that ends with #faq
  if (faqLink) {
    faqLink.addEventListener('click', function (e) {
      // Prevent the default action
      e.preventDefault();

      // Get the href attribute of the link
      const href = this.getAttribute('href');

      // Use the history API to push the new hash onto the URL without page jump
      history.pushState(null, null, href);

      // Smooth scroll to the FAQ section
      const faqSection = document.getElementById('faq');
      if (faqSection) {
        faqSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  hamburger.addEventListener('click', function () {
    // Toggle the 'active' class instead of changing the style directly
    navItems.classList.toggle('active');
  });

  // Function to handle the resize event
  function handleResize() {
    // If the window width is more than 768px and navItems contains the 'active' class
    if (window.innerWidth > 768 && navItems.classList.contains('active')) {
      // Remove the 'active' class
      navItems.classList.remove('active');
    }
  }

  // Add event listener for the window resize event
  window.addEventListener('resize', handleResize);
});
