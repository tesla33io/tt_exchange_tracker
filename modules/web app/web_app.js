import { sendData } from 'https://telegram.org/js/telegram-web-app.js'

function send() {
    pair = document.getElementById('currency').value;
    ui = document.getElementById('up_interval').value;
    console.log(pair + ui);
    sendData('pair-ui');
}
