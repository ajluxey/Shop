let baseURL = window.location.origin;
const addToCartURL = baseURL + '/cart/add/';
const removeFromCartURL = baseURL + '/cart/remove/';


function addItemToCart(id){
    let url = addToCartURL + id;
    sendRequest(url);
}


function removeItemFromCart(id){
    let url = removeFromCartURL + id;
    sendRequest(url)
}


function sendRequest(url) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.send();
}


function addItemFromButton(button){
    addItemToCart(button.value);
    deactivateButton(button);
}


function removeItemFromButton(button, count=null){
    removeItemFromCart(button.value);
    activateButton(button);
}


function deactivateButton(button){
    button.classList.remove('btn-primary');
    button.classList.add('btn-secondary');
    button.setAttribute('onclick', 'removeItemFromButton(this)');
    button.innerText = 'убрать из корзины';
}

function activateButton(button){
    button.classList.remove('btn-secondary');
    button.classList.add('btn-primary');
    button.setAttribute('onclick', 'addItemFromButton(this)');
    button.innerText = 'В корзину';
}


function increaseFromCart(cardId, curCount, maxCount){
    let card = document.getElementById(cardId);
    let btnInc = card.querySelector('[name="inc"]');
    let counter = card.querySelector('[name="counter"]');
    if (maxCount == curCount) return;
    if (maxCount == curCount + 1){
        btnInc.setAttribute('disabled', '');
    }
    addItemToCart(btnInc.value)
    counter.innerText = curCount + 1;
}
