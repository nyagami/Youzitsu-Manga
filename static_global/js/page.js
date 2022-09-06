function pre_page() {
    page = document.getElementById(`page-container-${current_book}`).childNodes
    if (!page[current_page[current_book]].previousSibling) return
    page[current_page[current_book]].classList.add("d-none")
    page[current_page[current_book] - 1].classList.remove("d-none")
    current_page[current_book] -= 1
}

function next_page() {
    page = document.getElementById(`page-container-${current_book}`).childNodes
    if (!page[current_page[current_book]].nextSibling) return
    page[current_page[current_book]].classList.add("d-none")
    page[current_page[current_book] + 1].classList.remove("d-none")
    current_page[current_book] += 1
}

function pre_series() {
    nodes = document.getElementById("book-container").childNodes
    if (!nodes[current_book].previousSibling) return
    nodes[current_book].classList.add('d-none')
    nodes[current_book - 1].classList.remove('d-none')

    title_container = document.getElementById("title-container").childNodes
    title_container[current_book].classList.add('d-none')
    title_container[current_book - 1].classList.remove('d-none')

    content_container = document.getElementById("content-container").childNodes
    content_container[current_book].classList.add('d-none')
    content_container[current_book - 1].classList.remove('d-none')

    pointer_container = document.getElementById("pointer-container").childNodes
    pointer_container[current_book].classList.add('d-none')
    pointer_container[current_book - 1].classList.remove('d-none')
    current_book -= 1
}

function next_series() {
    nodes = document.getElementById("book-container").childNodes
    if (!nodes[current_book].nextSibling) return
    nodes[current_book].classList.add('d-none')
    nodes[current_book + 1].classList.remove('d-none')

    title_container = document.getElementById("title-container").childNodes
    title_container[current_book].classList.add('d-none')
    title_container[current_book + 1].classList.remove('d-none')

    content_container = document.getElementById("content-container").childNodes
    content_container[current_book].classList.add('d-none')
    content_container[current_book + 1].classList.remove('d-none')

    pointer_container = document.getElementById("pointer-container").childNodes
    pointer_container[current_book].classList.add('d-none')
    pointer_container[current_book+1].classList.remove('d-none')
    current_book += 1
}

document.querySelector('body').addEventListener('keydown', function (e) {
    if (e.key == "ArrowLeft") pre_page()
    else if (e.key == "ArrowRight") next_page()
    else if (e.key == "ArrowUp") pre_series()
    else if (e.key == "ArrowDown") next_series()
}, false);

setInterval(() => {
    if (Math.floor(Math.random() * 2)) next_page()
    else pre_page()
}, 10000)