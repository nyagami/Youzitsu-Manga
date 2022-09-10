function display_model(){
    document.getElementById("page-model-container").classList.remove("d-none")
    book_card_HTML = document.getElementById("book-card").innerHTML
    document.getElementById("book-card").innerHTML = ""
    page_model = document.getElementById("page-model")
    page_model.innerHTML = book_card_HTML
    query_series
    links = document.getElementsByClassName("link-to-series")
    for(let i=0; i<links.length; i++) links[i].removeAttribute("onclick")
    set_background() //from page.js
    document.getElementById("button-nav").classList.remove("d-none")
    clearInterval(auto_change_cover) //from page.js
}
function escape_model(){
    book_card_HTML = document.getElementById("page-model").innerHTML
    document.getElementById("book-card").innerHTML = book_card_HTML
    document.getElementById("button-nav").classList.add("d-none")
    document.getElementById("page-model-container").classList.add('d-none')
    document.getElementById("page-model").innerHTML = ""
    query_series
    links = document.getElementsByClassName("link_to_series")
    for(let i=0; i<links.length; i++) links[i].setAttribute("onclick","display_model()")
    auto_change_cover = setInterval(change_cover, 10000)
}