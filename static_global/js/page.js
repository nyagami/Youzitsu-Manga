function change_page(step) {
    pages = document.getElementById(`page-container-${current_book}`).childNodes
    if (current_page[current_book]+step < 0 || current_page[current_book]+step >= pages.length) return
    pages[current_page[current_book]].classList.add("d-none")
    pages[current_page[current_book] + step].classList.remove("d-none")
    current_page[current_book] += step
    document.getElementById(`current-pointer-${current_book}`).style.marginLeft = `${current_page[current_book]/pages.length*100}%`
    if(!document.getElementById('page-model-container').classList.contains('d-none')){
        set_background()
    }
}

function change_book(step){
    books = document.getElementById("book-container").childNodes
    if (current_book+step < 0 || current_book+step >= books.length) return
    books[current_book].classList.add('d-none')
    books[current_book + step].classList.remove('d-none')

    title_container = document.getElementById("title-container").childNodes
    title_container[current_book].classList.add('d-none')
    title_container[current_book + step].classList.remove('d-none')

    content_container = document.getElementById("content-container").childNodes
    content_container[current_book].classList.add('d-none')
    content_container[current_book + step].classList.remove('d-none')

    pointer_container = document.getElementById("pointer-container").childNodes
    pointer_container[current_book].classList.add('d-none')
    pointer_container[current_book + step].classList.remove('d-none')
    current_book += step
    document.getElementById("current-pointer-vertical").style.top = `${current_book/books.length*100}%`
    if(!document.getElementById('page-model-container').classList.contains('d-none')){
        set_background()
    }
}

function set_background(){
    current_image = document.getElementById(`book-container`).childNodes[current_book].childNodes[current_page[current_book]].firstChild.src.split('.')
    current_image.pop()
    document.getElementById("page-model-background").style.backgroundImage = `url(${current_image.join('.')}_blur.jpeg)`
    document.getElementById("link-full-img").setAttribute("href",`${current_image}.jpeg`)
    link_to_read = document.getElementById("title-container").childNodes[current_book].href
    document.getElementById("link-to-read").setAttribute("href",link_to_read)
}

document.querySelector('body').addEventListener('keydown', function (e) {
    if (e.key == "ArrowLeft") change_page(-1)
    else if (e.key == "ArrowRight") change_page(1)
    else if (e.key == "ArrowUp") change_book(-1)
    else if (e.key == "ArrowDown") change_book(1)
    if(e.key == 'Escape'){
        if(!document.getElementById('page-model-container').classList.contains('d-none')){
            escape_model()
        }
    }
}, false);

let change_cover = () => {
    if (Math.floor(Math.random() * 2)) change_page(1)
    else change_page(-1)
}

auto_change_cover = setInterval(change_cover, 10000)