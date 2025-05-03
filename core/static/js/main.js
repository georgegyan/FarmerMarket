// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            alert(`Added product ${productId} to cart!`);
            // Here you would typically make an AJAX call to your backend
        });
    });
});