let commentSocket = null;
const openCommentSocket = () => {
    if (!username || !is_authenticated) return;
    commentSocket = new WebSocket(`ws://${window.location.host}/ws/comment/c/test/`);

    commentSocket.onopen = e => {
        console.log(`ws opened for comment`);
    }

    commentSocket.onclose = e => {
        setTimeout(function () {
            console.log("Reconnecting...");
            openCommentSocket();
        }, 2000);
    }

    commentSocket.onmessage = e => {
        const data = JSON.parse(e.data);
        console.log(data);
        switch (data.type) {
            case 'comment':
                console.log(data.comment);
                break;
            default:
                break;
        }
    }

    commentSocket.onerror = e => {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        commentSocket.close();
    }
}

openCommentSocket();
