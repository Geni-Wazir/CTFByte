document.addEventListener('DOMContentLoaded',() => {
    var socket = io.connect('http://' + location.hostname + ':' + location.port);
    
    socket.on('connect',() => {
        // socket.send("I am Connected to the Socket!")
    })

    socket.on('message', data => {
        const p = document.createElement('p')
        const span_username = document.createElement('span')
        const br = document.createElement('br')
        span_username.innerHTML = data.username
        p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML
        document.querySelector('#display-message-section').append(p)
    })

    socket.on('some-event', data => {
        console.log(data)
    })

    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg':document.querySelector('#user_message').value,'username':username})
        document.querySelector('#user_message').value = ""
    }
})