let commentSocket = null;
const openCommentSocket = () => {
    if (!requestUsername || !is_authenticated) return;
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
                    <div class="comment-container deepth-${comment.deepth}"
                        data-id="${comment.id}" data-parent="${comment.parent || ''}" data-deepth="${comment.deepth}"
                        data-time="${comment.created_on}" data-username="${comment.username}"
                        data-display-name="${comment.author.display_name}" data-avatar="${comment.author.avatar}"
                        data-content="${comment.content}" data-media="${comment.media_url}"
                        data-bind="comment_node"
                    >
                    </div>
                    <ul class="comment-list" comment-id="${comment.id}"></ul>
                    <div class="comment-box-container" comment-id="${comment.id}"></div>
                    `;
                if(comment.parent){
                    const parent = document.querySelector(`ul.comment-list[comment-id="${comment.parent}"]`);
                    parent.appendChild(commentElement);
                }else{
                    const wrapper = document.querySelector("ul.comment-list[comment-id='-1']");
                    wrapper.prepend(commentElement);
                }
                new CommentNode(commentElement.querySelector("[data-bind='comment_node']"));
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
