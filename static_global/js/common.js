function escapeHtml(unsafe)
{
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function UI_CommmentView(o){
	o=be(o);
	UI.call(this, {
		node: o.node,
		kind: ['CommentView'].concat(o.kind || []),
	});
	Linkable.call(this);
	this.active = false;

	this.close = () => {
		this.active = false;
		this.$.classList.add('hidden');
	};

	this.open = () => {
		this.active = true;
		this.$.classList.remove('hidden');
	}
    this.reverse = () => {
        const wrapper = this.$.querySelector("ul");
        wrapper.append(...Array.from(wrapper.childNodes).reverse());
    }
    this.init = () => {
        this.reverse();
        this.commentList = this.$.querySelector(".comment-list[comment-id='-1']");
        this.commentBoxCtn = this.$.querySelector('.comment-box-container');
        // Comment box data
        const CBD = {
            parent: '-1',
            deepth: '0',
        }
        new CommentBox(this.commentBoxCtn, CBD, true);
        this.nodes = {};
        this.$.querySelectorAll("[data-bind='comment_node']").forEach(node => {
            commentNode = new CommentNode(node);
            this.nodes[commentNode.id] = commentNode;
        });
    }
    // receive data from socket
    this.receive = (data) => {
        const comment = data.comment;
        const container = document.createElement('li');
        container.innerHTML = `
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
            const parent = this.nodes[comment.parent].commentList;
            parent.appendChild(container);
        }else{
            const wrapper = this.commentList;
            wrapper.prepend(container);
        }
        const commentNode = new CommentNode(container.querySelector("[data-bind='comment_node']"));
        this.nodes[commentNode.id] = commentNode;
    }

    this.init();
}

function CommentNode(node){
    this.$ = node;
    this.init = () => {
        this.$.classList.add('CommentNode');
        this.container = this.$.parentElement;
        this.id = this.$.getAttribute('data-id');
        this.parent = this.$.getAttribute('data-parent');
        this.time = this.$.getAttribute('data-time');
        this.deepth = Number(this.$.getAttribute('data-deepth'));
        this.username = this.$.getAttribute('data-username');
        this.display_name = this.$.getAttribute('data-display-name');
        this.avatar = this.$.getAttribute('data-avatar');
        this.content = escapeHtml(this.$.getAttribute('data-content'));
        this.media = this.$.getAttribute('data-media');

        this.$.innerHTML = `
            <div class="comment-avt">
                <a href="/user/${this.username}">
                    <img src="${this.avatar}" alt="avatar" class="comment-img">
                </a>
            </div>
            <div class="comment-content">
                <span class="comment-username">${this.display_name}</span>
                <p>${this.content}</p>
                ${this.media && this.media != 'None'
                    ? `<img src="${this.media}" alt="lỗi" style="max-height: 360px; max-width: 100%; position: relative;">`
                    : ''
                }
                ${is_authenticated
                    ?
                    `
                    <div class="comment-bottom">
                        <button class="comment-reply">
                            Trả lời
                        </button>
                        <span class="time">${convertTime(this.time)}</span>
                        <div class="more">
                            <button class="ico-btn more-btn"
                                onclick="this.nextElementSibling.classList.toggle('hidden'); this.nextElementSibling.focus()"
                            >
                            </button>
                            <button class="more-menu hidden" onblur="this.classList.add('hidden')">
                                ${
                                    requestUsername === this.username
                                    ?
                                        `
                                        <div class="more-item delete">Xoá</div>
                                        `       
                                    : ''
                                }
                                <div class="more-item" onclick="this.parentElement.classList.add('hidden')">Báo cáo</div>
                            </button>
                        </div>
                    </div>
                    `
                    : ''
                }
            </div>
        `;
        let CBdeepth = this.deepth + 1;
        if(CBdeepth == 3){
            this.commentBox = document.querySelector(`.comment-box-container[comment-id="${this.parent}"]`);
            CBdeepth = 2;
        }else{
            this.commentBox = this.container.querySelector(`.comment-box-container[comment-id="${this.id}"]`);
        }
        this.commentBox = new CommentBox(
            this.commentBox,
            {
                username: this.username,
                display_name: this.display_name,
                parent: this.id,
                deepth: CBdeepth,
            },
            false
        );
        this.replyBtn = this.$.querySelector('.comment-bottom .comment-reply');
        if(this.replyBtn){
            this.replyBtn.onclick = e => this.commentBox.init();
        }
        this.deleteBtn = this.$.querySelector('.more .more-item.delete');
        if(this.deleteBtn){
            this.deleteBtn.onclick = () =>{
                const formBody = new FormData();
                formBody.append('id', this.id);
                formBody.append('csrfmiddlewaretoken', csrf_token);
                fetch('/api/comment/delete/',{
                    method: 'POST',
                    body: formBody,
                }).then(res => {
                    if(res.ok){
                        this.container.remove();
                    }
                });
            }
        }
        this.img = this.$.querySelector(".comment-content img");
        if(this.img){
            this.img.onclick = () => imageModal.open(this.img);
        }

        this.commentList = this.container.querySelector(`.comment-list[comment-id="${this.id}"]`);
    }

    this.init();
}

function CommentBox(node, data, isRootComment){
    this.$ = node;
    this.data = data;
    this.isRootComment = isRootComment;
    this.init = () => {
        this.$.innerHTML = `
        <div class="comment-dialog deepth-${data.deepth}">
            <div class="comment-avt">
                <a href="/user/${requestUsername}">
                    <img src="${requestAvatar}" alt="avatar" class="comment-img">
                </a>
            </div>
            <div class="comment-box">
                <textarea class="comment-editor" placeholder="${isRootComment ? 'Viết bình luận...' : 'Đang trả lời ' + data.display_name}"></textarea>
                <div class="comment-button-group">
                    <input type="file" accept="image/jpeg, image/png, image/webp" class="ico-btn comment-button-media"></input>
                    <div class="space"></div>
                    <button type="button" class="ico-btn comment-button-submit" parent="${data.parent}"></button>
                </div>
                <div class="comment-box-image"></div>
            </div>
        </div>
        `;
        this.$.scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"});
        this.imgContainer = new CommentBoxImage(this.$.querySelector(".comment-box-image"));
        this.textarea = this.$.querySelector('textarea');
        this.textarea.focus({preventScroll: true});
        this.textarea.addEventListener('keydown', e => {
            e.stopImmediatePropagation();
        });

        this.textarea.addEventListener("paste", (event) => {
            const items = event.clipboardData.items;
            for(let i in items){
                const item = items[i];
                if(item.kind === 'file' && (['image/png', 'image/jpeg', 'image/webp'].includes(item.type))){
                    const blob = item.getAsFile();
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        this.imgContainer.open(e.target.result);
                    }
                    reader.readAsDataURL(blob);
                }
            }
        });

        this.imgInput = this.$.querySelector('.comment-box input');
        this.imgInput.onchange = () => {
            if(this.imgInput.files && this.imgInput.files[0]){
                const reader = new FileReader();
    
                reader.onload = (e) => {
                    this.imgContainer.open(e.target.result);
                };
    
                reader.readAsDataURL(this.imgInput.files[0]);
            }
        }

        this.submitBtn = this.$.querySelector('.comment-box .comment-button-submit');
        this.submitBtn.onclick = () => {
            const content = this.textarea.value;
            if(!content) return;
            let media = this.imgContainer.img.getAttribute("src");
            if(media === "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAA") media = "";
            else{
                media = media.substring(media.indexOf(";base64,") + ";base64,".length);
            }
            this.clear();
            const formBody = new FormData();
            formBody.append('article', article);
            formBody.append('parent', this.data.parent || '-1');
            formBody.append('content', content);
            formBody.append('media', media);
            formBody.append('csrfmiddlewaretoken', csrf_token);
            fetch("/api/comment/",{
                method: "POST",
                body: formBody,
            });
        }
    }

    this.clear = () => {
        this.textarea.value = '';
        this.imgContainer.clear();
    }

    if(this.isRootComment) this.init();
}

function CommentBoxImage(node){
    this.$ = node;
    this.init = () => {
        this.$.classList.add("hidden", "CommentBoxImage");
        this.$.innerHTML = `
            <button class="ico-btn clear">Xoá</button>
            <img alt="lỗi" style="max-height: 240px; max-width: 100%; position: relative;" comment-id="-1">
        `;
        this.clearBtn = this.$.querySelector("button.clear");
        this.img = this.$.querySelector("img");

        this.img.onclick = () => imageModal.open(this.img);
        this.clearBtn.onclick = this.clear;
    }
    this.open = (imageData) => {
        this.img.setAttribute("src", imageData);
        this.$.classList.remove('hidden');
    }
    this.close = () => {
        this.$.classList.add("hidden");
    }
    this.clear = () => {
        this.img.setAttribute("src", "");
        this.close();
    }
    this.init();
}

function ImageModal(){
    this.$ = document.querySelector('#image-modal');
    this.init = () => {
        this.$.classList.add('hidden', 'ImageModal');
        this.$.innerHTML = `
            <span class="close" onclick="this.parentElement.classList.add('hidden')">&times;</span>
            <img>
        `
        this.img = this.$.querySelector('img');
    }
    this.close = () => {
        this.$.classList.add('hidden');
    }
    this.open = (node) => {
        this.img.setAttribute("src", node.getAttribute("src"));
        this.$.classList.remove('hidden');
    }

    this.init();
}

function CommentSocket(){
    this.socket = null;
    this.ws_url = `ws://${window.location.host}/ws/comment/c/${article}/`;
    this.open = () => {
        this.socket = new WebSocket(this.ws_url);
        this.socket.onopen = () => {
            console.log("Websocket opened for Comment");
        }
        this.socket.onclose = () => {
            setTimeout(function () {
                console.log("Reconnecting...");
                this.open();
            }, 2000);
        }
        this.socket.onmessage = e => {
            const data = JSON.parse(e.data);
            switch (data.type) {
                case 'comment':
                    if(commentView) commentView.receive(data);
                    break;
                default:
                    break;
            }
        }
        this.socket.onerror = err => {
            console.log("WebSocket encountered an error: " + err.message);
            console.log("Closing the socket.");
            this.socket.close();
        }
    }
    this.open();
}
commentView = null;     //this will be initialised when Reader UI is initialised
imageModal = new ImageModal();
new CommentSocket();