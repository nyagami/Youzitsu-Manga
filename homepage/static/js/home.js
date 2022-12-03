const volumes_wrapper = document.getElementsByClassName("volumes-wrapper")
for(let i = 0; i < volumes_wrapper.length; i++){
    fetch(`/api/get_all_volumes_by_series_slug/${volumes_wrapper[i].title}/`).then(req => req.json()).then(list => {
        const volumes_list = list['volumes_list']
        let ul = `<ul class="d-flex">`;
        volumes_list.forEach((volume_number) => {
            ul += `<li class="volume-item text-uppercase text-center">vol &#10;&#13;${volume_number}</li>`;
        })
        ul += `</ul>`;
        volumes_wrapper[i].innerHTML = ul;
    })
}