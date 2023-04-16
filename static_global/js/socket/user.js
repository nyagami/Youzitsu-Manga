var userSocket = null;
const openUserSocket = () => {
    if (!username) return;
    userSocket = new WebSocket(`ws://${window.location.host}/ws/${username}/`);

    userSocket.onopen = e => {
        console.log(`ws opened for ${username}`);
    }

    userSocket.onclose = e => {
        setTimeout(function () {
            console.log("Reconnecting...");
            openUserSocket();
        }, 2000);
    }

    userSocket.onmessage = e => {
        const data = JSON.parse(e.data);
        console.log(data);
        switch (data.type) {
            case 'notification':
                console.log(data.notification);
                break;
            default:
                break;
        }
    }
    userSocket.onerror = e => {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        userSocket.close();
    }
}

openUserSocket();
