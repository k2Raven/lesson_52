function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


async function makeRequest(url, options, method) {
    if (options) {
        options.method = method || "GET";
    } else {
        options = {method: method || "GET"};
    }
    let headers = options.headers || {};
    if(options.method !== "GET") {
        headers['X-CSRFToken'] = getCookie('csrftoken');
    }
    options.headers = headers;

    let response = await fetch(url, options);

    if (response.ok) {
        return await response.json();
    } else {
        let error = new Error(response.statusText);
        error.response = response;
        throw error;
    }
}


async function onClick(event) {
    event.preventDefault();
    let a = event.target;
    let url = a.href;
    try {
        let data = await makeRequest(url);
        console.log(data);
        let div = a.parentElement;
        let p = document.createElement('p');
        p.innerHTML = `id = ${data.pk} test=${data.test} number =${data.number}`;
        div.append(p);
    } catch (e) {
        console.log(e);
    }
}


async function onFormSubmit(event) {
    event.preventDefault();
    let form = event.target;
    let url = form.action;
    let test_input = document.querySelector('input[name="test_input"]');
    let text = test_input? test_input.value: '';
    try{
        let data = await makeRequest(url, {body: JSON.stringify({'test': text})}, 'POST');
        console.log(data)
    } catch (e) {
        console.log(e);
    }

}

function onLoad() {
    let urls = document.getElementsByClassName('test_url');
    for (let url of urls) {
        url.addEventListener('click', onClick);
    }

    let test_form = document.getElementById('test_form');
    if (test_form) {
        test_form.addEventListener('submit', onFormSubmit);
    }

}

window.addEventListener('load', onLoad);