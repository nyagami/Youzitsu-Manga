fetch('/api/get_all_series/')
.then(res => res.json())
.then(all_series => {
    for(let series in all_series){
        const manga = all_series[series];
        html = `
        <div class="series-card">
            <picture class="d-block">
                <img src="${manga.cover}" alt="series embed_image">
            </picture>
            <div class="btn-group btn" role="button" onclick=" location.href='/read/series/${manga.slug}' ">
                <span>Đọc ngay ››</span>
            </div>
            <div class="btn-group justify-content-around">
                <div class="react"><span><i class="fas fa-heart icon"></i></span></div>
                <div class="react"><span><i class="fas fa-share-square icon"></i></span></div>
                <div class="react"><span><i class="fas fa-award icon"></i></span></div>
            </div>
        </div>
        <div class="series-content">
            <div class="series-title"><b><a href='/read/series/${manga.slug}'>${series}</a></b></div>
            <div class="volumes-container">
                <ul>
                ${manga.volumes.reduce((prev, vol) => {
                    const style = `border: solid 1.5px ${vol.color};`;
                    const li = `
                    <li class="volume-item text-uppercase" role="button" onclick="location.href='/read/manga/${manga.slug}/#volume-${vol.num}'" style = "${style}">
                        vol ${vol.num}
                    </li>`;
                    return prev + li;
                }, '')}
                </ul>
            </div>
        </div>
        `;
        $(`#${manga.slug}`).html(html);
    }
})