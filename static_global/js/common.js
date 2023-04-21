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
        this.commentBoxCtn = this.$.querySelector('.comment-box-container');
        CBD = {
            parent: '-1',
            deepth: '0',
        }
        new CommentBox(this.commentBoxCtn, CBD, true);
        this.$.querySelectorAll("[data-bind='comment_node']").map(node => new CommentNode(node));
    }
    this.init();
}

function CommentNode(node){
    this.$ = node;
    this.init = () => {
        this.$.classList.add('CommentNode');
        this.container = this.$.parentElement;
        const id = this.$.getAttribute('data-id');
        const parent = this.$.getAttribute('data-parent');
        const time = this.$.getAttribute('data-time');
        let deepth = Number(this.$.getAttribute('data-deepth'));
        const username = this.$.getAttribute('data-username');
        const display_name = this.$.getAttribute('data-display-name');
        const avatar = this.$.getAttribute('data-avatar');
        const content = this.$.getAttribute('data-content');
        const media = this.$.getAttribute('data-media');

        this.$.innerHTML = `
            <div class="comment-avt">
                <a href="/user/${username}">
                    <img src="${avatar}" alt="avatar" class="comment-img">
                </a>
            </div>
            <div class="comment-content">
                <span class="comment-username">${display_name}</span>
                <p>${content}</p>
                ${media && media != 'None'
                    ? `<img onclick="displayModal(this)" src="${media}" alt="lỗi" style="max-height: 360px; max-width: 100%; position: relative;">`
                    : ''
                }
                ${is_authenticated
                    ?
                    `
                    <div class="comment-bottom">
                        <button class="comment-reply">
                            Trả lời
                        </button>
                        <span class="time">${convertTime(time)}</span>
                        <div class="more">
                            <button class="ico-btn more-btn"
                                onclick="this.nextElementSibling.classList.toggle('hidden'); this.nextElementSibling.focus()"
                            >
                            </button>
                            <button class="more-menu hidden" onblur="this.classList.add('hidden')">
                                ${
                                    requestUsername === username
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
        if(deepth == 2){
            this.commentBox = document.querySelector(`.comment-box-container[comment-id="${parent}"]`);
            deepth = 1;
        }else{
            this.commentBox = this.container.querySelector(`.comment-box-container[comment-id="${id}"]`);
        }
        this.commentBox = new CommentBox(
            this.commentBox,
            {
                username: username,
                display_name: display_name,
                parent: id,
                deepth: deepth + 1,
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
                formBody.append('id', id);
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
                    <button type="button" class="ico-btn comment-button-submit"
                        parent="${data.parent}"
                    >
                    </button>
                </div>
                <div>
                    <button class="ico-btn delete hidden" onclick="this.nextElementSibling.setAttribute('src','data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAA'); this.classList.add('hidden')">🗑️</button>
                    <img onclick="displayModal(this)" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAA" alt="lỗi" style="max-height: 240px; max-width: 100%; position: relative;" comment-id="-1">
                </div>
            </div>
        </div>
        `;
        this.img = this.$.querySelector('.comment-box img');
        this.deleteBtn = this.$.querySelector('.comment-box .delete');

        this.textarea = this.$.querySelector('textarea');
        this.$.scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"});
        this.textarea.focus({preventScroll: true});
        this.textarea.addEventListener('keydown', e => {
            e.stopImmediatePropagation();
        });

        // hack
        const img = this.img;
        const deleteBtn = this.deleteBtn;

        this.textarea.addEventListener("paste", (event) => {
            const items = event.clipboardData.items;
            for(let i in items){
                const item = items[i];
                if(item.kind === 'file' && (['image/png', 'image/jpeg', 'image/webp'].includes(item.type))){
                    const blob = item.getAsFile();
                    const reader = new FileReader();
                    reader.onload = function(e){
                        img.setAttribute('src', e.target.result);
                        deleteBtn.classList.remove("hidden");
                    }
                    reader.readAsDataURL(blob);
                }
            }
        });

        this.imgInput = this.$.querySelector('.comment-box input');
        this.imgInput.onchange = () => {
            if(this.imgInput.files && this.imgInput.files[0]){
                const reader = new FileReader();
    
                reader.onload = function (e) {
                    img.setAttribute('src', e.target.result);
                    deleteBtn.classList.remove("hidden");
                };
    
                reader.readAsDataURL(this.imgInput.files[0]);
            }
        }

        this.submitBtn = this.$.querySelector('.comment-box .comment-button-submit');
        this.submitBtn.onclick = () => {
            const content = this.textarea.value;
            if(!content) return;
            this.textarea.value = '';
            let media = this.img.getAttribute("src");
            if(media === "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAA") media = "";
            else{
                media = media.substring(media.indexOf(";base64,") + ";base64,".length);
            }
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

    if(this.isRootComment) this.init();
}

function ImageModal(){
    this.$ = document.querySelector('#image-modal');
    this.init = () => {
        this.$.innerHTML = `
            <span class="close" onclick="this.parentElement.classList.add('hidden')">&times;</span>
            <img>
        `
        this.img = this.$.querySelector('img');
        this.$.classList.add('hidden', 'ImageModal');
    }
    this.close = () => {
        this.$.classList.add('hidden');
    }
    this.open = () => {
        this.$.classList.remove('hidden');
    }

    this.init();
}


imageModal = new ImageModal();