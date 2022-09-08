current_book = 0
current_page = {0:0}

query_series = fetch(`/api/${api}/`).then(res => res.json()).then(series_slug => {
    document.getElementById("current-pointer-vertical").style.height=`${1/series_slug.length*100}%`
    for(let i=0; i<series_slug.length; i++){
        if(i==current_book){
            document.getElementById("book-container").innerHTML = `<div id="page-container-${i}"></div>`
            document.getElementById("pointer-container").innerHTML = `<div class="current-pointer" id="current-pointer-${i}"></div>`
        }
        else{
            document.getElementById("book-container").innerHTML += `<div class="d-none" id="page-container-${i}"></div>`
            document.getElementById("pointer-container").innerHTML += `<div class="current-pointer d-none" id="current-pointer-${i}"></div>`
        }
        current_page[i] = 0
        fetch(`/api/${series_gender}/${series_slug[i]}/`).then(res => res.json()).then(series => {
                if(i==0){
                document.getElementById("title-container").innerHTML=`<a class="text-decoration-none" href="/read/manga/${series.slug}/"><h1 class="series-title">${series.title}</h1></a>`
                document.getElementById("content-container").innerHTML=`<div class="series-content">${series.description}</div>`
                document.getElementById("footer-container").innerHTML =`<div><a>${series.author}</a> | <a>${series.artist}</a></div>`
            }
            else{
                document.getElementById("title-container").innerHTML +=`<a class="d-none text-decoration-none" href="/read/manga/${series.slug}/"><h1 class="series-title">${series.title}</h1></a>`
                document.getElementById("content-container").innerHTML +=`<div class="series-content d-none">${series.description}</div>`
                document.getElementById("footer-container").innerHTML +=`<div class="d-none"><a class="d-none">${series.author}</a> | <a>${series.artist}</a></div>`
            }
        })
        fetch(`/api/${get_cover_gender}/${series_slug[i]}/`).then(res => res.json()).then(covers => {
            document.getElementById(`current-pointer-${i}`).style.width=`${1/covers.length*100}%`
            for(let j=0; j<covers.length; j++){
                if(j==current_page[current_book]) document.getElementById(`page-container-${i}`).innerHTML = `<a class="link_to_series" onclick=display_model()><img class="volume-cover img-fluid" src="${covers[j][2]}" alt="Ảnh bìa Volume"></a>`
                else document.getElementById(`page-container-${i}`).innerHTML += `<a onclick=display_model() class="d-none link_to_series"><img class="volume-cover img-fluid" src="${covers[j][2]}" alt="Ảnh bìa Volume"></a>`
            }
        })
    }
})