var userSocket = null;
const openUserSocket = () => {
    if (!requestUsername) return;
    userSocket = new WebSocket(`ws://${window.location.host}/ws/${requestUsername}/`);

    userSocket.onopen = e => {
        console.log(`ws opened for ${requestUsername}`);
    }

    userSocket.onclose = e => {
        setTimeout(function () {
            console.log("Reconnecting...");
            openUserSocket();
        }, 2000);
    }

    userSocket.onmessage = e => {
        const data = JSON.parse(e.data);
        switch (data.type) {
            case 'notify':
                notification = data.notification;
                node = document.createElement('li');
                node.innerHTML = `
                <a href="/user/${notification.username}" class="noti-link">
                    <img src="${notification.author.avatar}"
                        class="rounded-circle user-avatar-lg" alt="user">
                    <div class="noti-body">
                        <div class="noti-content">
                            <span class="user-fullname">${notification.author.display_name}</span>
                            ${notification.content}
                        </div>
                        <span class="noti-time">5 phút trước</span>
                        <i class="not-read"></i>
                    </div>
                </a>
                `;
                document.querySelector('.list-group.list-noti ul').prepend(node);
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
