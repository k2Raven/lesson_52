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
    if (localStorage.getItem('authToken')) {
            headers['Authorization'] = 'Token ' + localStorage.getItem('authToken');
    }
    if (options.method !== "GET") {
        headers['X-CSRFToken'] = getCookie('csrftoken');
    }
    headers['Content-Type'] = 'application/json';
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


async function onLoginFormSubmit(event) {
    event.preventDefault();
    let form = event.target;
    let formData = new FormData(form);
    let username = formData.get('username');
    let password = formData.get('password');
    let response = await makeRequest('/api/v3/login/', {
        'body': JSON.stringify({
            'username': username,
            'password': password
        })
    }, "POST");
    if(response.token) {
        localStorage.setItem('authToken', response.token);
    }
    event.target.submit();
}

function onLoad() {
    let loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', onLoginFormSubmit);
    }
    let logoutForm = document.getElementById('logout-form');
    if(logoutForm) logoutForm.addEventListener('submit',
        () => localStorage.removeItem('authToken')
    )
}

window.addEventListener('load', onLoad);