let baseURL = window.location.origin;
const addToCartURL = baseURL + '/cart/add/';
const decreaseItemCountURL = baseURL + '/cart/decrease/'
const removeFromCartURL = baseURL + '/cart/remove/';


function addItemToCart(id){
    let url = addToCartURL + id;
    sendRequest(url);
}


function decreaseItemInCart(id){
    let url = decreaseItemCountURL + id;
    sendRequest(url);
}


function removeItemFromCart(id){
    let url = removeFromCartURL + id;
    sendRequest(url);
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


function removeForm(){
    form = document.getElementById('form');
    p = document.createTextNode('Корзина пока пуста');
    parent = form.parentNode;
    form.remove();
    parent.append(p);
}


function decreaseFromCard(cardId){
    let card = document.getElementById(cardId);
    let btnInc = card.querySelector('[name="inc"]');
    if (btnInc.hasAttribute('disabled')) btnInc.removeAttribute('disabled');
    getCartData()
        .then(cart => {
            getTotalPrice();
            curCount = cart[cardId];
            if (curCount == 0) return;

            let btnDec = card.querySelector('[name="dec"]');
            let counter = card.querySelector('[name="counter"]');
            let total_price_field = document.getElementById('total_price');

            if (curCount - 1 == 0){
                if (confirm("Товар будет удален из корзины")) {
                    removeItemFromCart(cardId);
                    card.remove();
                    delete cart[cardId];
                    if (Object.keys(cart).length === 0 && cart.constructor === Object) {
                        removeForm();
                    }
                } else {
                    return;
                }
            }
            decreaseItemInCart(cardId);
            counter.innerText = curCount - 1;
            getTotalPrice()
                .then(total_price => total_price_field.innerText = 'Итоговая цена ' + total_price['total_price'] + ' руб.')
                .catch(err => console.log(err));
        })
        .catch(err => console.log(err));
}



function increaseFromCard(cardId, maxCount){
    let card = document.getElementById(cardId);
    let btnDec = card.querySelector('[name="dec"]');
    if (btnDec.hasAttribute('disabled')) btnDec.removeAttribute('disabled');

    getCartData()
        .then(cart => {
            getTotalPrice();
            let curCount = cart[cardId];
            if (maxCount == curCount) return;

            let btnInc = card.querySelector('[name="inc"]');
            let counter = card.querySelector('[name="counter"]');
            let total_price_field = document.getElementById('total_price');

            if (maxCount == curCount + 1){
                btnInc.setAttribute('disabled', '');
            }
            addItemToCart(cardId)
            counter.innerText = curCount + 1;
            getTotalPrice()
                .then(total_price => total_price_field.innerText = 'Итоговая цена ' + total_price['total_price'] + ' руб.')
                .catch(err => console.log(err));
        })
        .catch(err => console.log(err));

}


function getCartData(){
    let url = baseURL + '/cart/get_json';
    return getJson(url)
}


function getTotalPrice(){
    let url = baseURL + '/cart/get_total_price';
    return getJson(url);
}


async function getJson(url){
    const response = await fetch(url)
    return await response.json()
}


//function getJson(url){
//    return new Promise( (resolve, reject) => {
//        const xhr = new XMLHttpRequest();
//        xhr.open('GET', url);
//        xhr.responseType = 'json';
//
//        xhr.onload = () => {
//            if (xhr.status >= 400) {
//                reject(xhr.response);
//            } else {
//                resolve(xhr.response);
//            }
//        };
//
//        xhr.onerror = () => {
//            reject(xhr.response);
//        };
//
//        xhr.send();
//    });
//}