function makeRequest(url, onload, method) {
    let xhr = new XMLHttpRequest();
    xhr.onload = onload;
    xhr.open(method || "GET", url);
    xhr.send();
}


function onClick(event) {
    event.preventDefault();
    let a = event.target;
    let url = a.href;
    console.log(url);
    makeRequest(url,(event)=>{
        let status = event.target.status;
        if (status === 200) {
            let data = JSON.parse(event.target.response);
            console.log(data);
            let div = a.parentElement;
            // 'pk': pk, 'test': 'text', 'number': 123
            div.innerHTML += `<p>id = ${data.pk} test=${data.test} number =${data.number}</p>`;

        }
    });
}

function onLoad() {
    let urls = document.getElementsByClassName('test_url');
    for (let url of urls) {
        url.addEventListener('click', onClick);
    }
    let urlParams = new URLSearchParams(window.location.search);
    let param = urlParams.get('paramName');
    console.log(param);
}

window.addEventListener('load', onLoad);