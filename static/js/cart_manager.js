let baseURL = window.location.origin;
const addToCartURL = baseURL + '/cart/add/';
const removeFromCartURL = baseURL + '/cart/remove/';

// получаем кнопку, парсим её валуе, кидаем запрос, если всё ок то меняем её на неактивную + пишем что добавлен в корзину
function addItemToCart(button){
    let url = addToCartURL + button.value;
    deactivateButton(button);
    sendRequest(url);
}


function removeItemFromCart(button){
    let url = removeFromCartURL + button.value;
    sendRequest(url)
}


function sendRequest(url) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.send();
}


function deactivateButton(button){
    button.classList.remove('btn-primary');
    button.classList.add('btn-secondary');
    button.innerText = 'В корзине';
    button.setAttribute('disabled', '');
}