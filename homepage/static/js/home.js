const volumes_container = document.getElementsByClassName("volumes-container")
for(let i = 0; i < volumes_container.length; i++){
    fetch(`/api/get_all_volumes_by_series_slug/${volumes_container[i].title}/`).then(req => req.json()).then(list => {
        const volumes_list = list['volumes_list']
        let ul = `<ul class="d-flex">`;
        volumes_list.forEach((data) => {
            style = "";
            ul += `<li class="volume-item text-uppercase" style="border: solid 1.5px ${data['color']};">vol ${data['number']}</li>`;
        })
        ul += `</ul>`;
        volumes_container[i].innerHTML = ul;
    })
}
