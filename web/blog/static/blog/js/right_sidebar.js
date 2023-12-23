function tagList() {
    $.ajax({
        url: '/api/v1/article/tags/',
        type: 'get',
        success: successTagHandler
    })
}
  
function successTagHandler(data) {
    const tagList = $('#tagList')
    for (let tag of data) {
        const template = tagListTemplate(tag)
        tagList.append(template)
    }
    $('.tags').click(tagClickHandler)
}
  
function tagListTemplate (tag) {
return `
<li><a href="" data-id=${tag.id} class='tags'><span class="badge badge-info">${tag.name}</span></a></li>
`
}


$("#searchField").keyup(function(e) {
    if (e.keyCode === 13) {
        articleSearch(e)
    }
});

$("#searchButton").click(articleSearch)

function articleSearch (e) {
    var query = $("#searchField").val();
    const url = new URL(window.location);
    url.searchParams.set('search', query);
    window.history.pushState(null, '', url.toString());
    articleList()
    
}


$("#cleanButton").click(cleanSearch)

function cleanSearch () {
    const url = new URL(window.location);
    url.searchParams.delete('tags')
    url.searchParams.delete('search')
    window.history.pushState(null, '', url.toString());
}