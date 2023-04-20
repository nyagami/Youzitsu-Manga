let commentSocket = null;
const openCommentSocket = () => {
    if (!username || !is_authenticated) return;
    commentSocket = new WebSocket(`ws://${window.location.host}/ws/comment/c/${article}/`);

    commentSocket.onclose = e => {
        setTimeout(function () {
            console.log("Reconnecting...");
            openCommentSocket();
        }, 2000);
    }

    commentSocket.onmessage = e => {
        const data = JSON.parse(e.data);
        switch (data.type) {
            case 'comment':
                const comment = data.comment;
                const commentElement = document.createElement('li');
                    commentElement.innerHTML = `
                    <div class="comment-container deepth-${comment.deepth}">
                        <div class="comment-avt">
                            <a href="/user/${comment.username}">
                                <img src="${comment.author.avatar}" alt="avatar" class="comment-img">
                            </a>
                        </div>
                        <div class="comment-content">
                            <span class="comment-username">
                                ${comment.author.display_name}
                            </span>
                            <p>${comment.content}</p>
                            ${is_authenticated 
                                ?
                                `<div class="comment-bottom">
                                    <h5 class="comment-reply" parent="${comment.parent}" comment-id="${comment.id}" 
                                    deepth="${comment.deepth}" username="${comment.username}" 
                                    display-name="${comment.author.display_name}" onclick="replyHandler(this, event)">
                                        trả lời
                                    </h5>
                                    <span class="time"> ${convertTime(comment.created_on)} </span>
                                </div>
                                ` 
                                : 
                                ''}
                        </div>
                    </div>
                    <ul></ul>
                    <div class="reply-comment-box" comment-id="${comment.id}"></div>
                    `;
                if(comment.parent){
                    const parent = document.querySelector(`.comment-container[comment-id="${comment.parent}"]`).nextElementSibling;
                    parent.appendChild(commentElement);
                }else{
                    const wrapper = document.querySelector(".comment-wrapper[data-bind='comment_section'] > ul");
                    wrapper.prepend(commentElement);
                }
                break;
            default:
                break;
        }
    }

    commentSocket.onerror = err => {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        commentSocket.close();
    }
}

openCommentSocket();
