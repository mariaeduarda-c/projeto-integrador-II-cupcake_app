// Funções globais para o carrinho de compras
function getCart() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}

function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

function updateCartCount() {
    const cart = getCart();
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const cartCountElements = document.querySelectorAll('#cart-count');
    cartCountElements.forEach(element => {
        element.textContent = totalItems;
    });
}

function addToCart(productId, productName, productPrice) {
    const id = parseInt(productId)
    let cart = getCart();
    const existingItemIndex = cart.findIndex(item => item.id === id);

    if (existingItemIndex > -1) {
        cart[existingItemIndex].quantity++;
    } else {
        cart.push({
            id: id,
            name: productName,
            price: productPrice,
            quantity: 1
        });
    }
    saveCart(cart);
    alert(`${productName} adicionado ao carrinho!`);
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('cart');
    // Redireciona para a página inicial e força um recarregamento para limpar a navegação
    window.location.href = 'index.html';
    location.reload();
}

// Inicializa a contagem do carrinho quando o script é carregado
document.addEventListener('DOMContentLoaded', updateCartCount);