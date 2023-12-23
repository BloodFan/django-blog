$(function() {
    tagsList()
});

function tagsList() {
    $.ajax({
        url: '/api/v1/article/tags/',
        type: 'get',
        success: successTagHandler
    })
};

function successTagHandler(data){
    const tagsList = $('.loadTags')
    tagsList.empty()
    for (let tag of data){
        const template = tagsTemplate(tag)
        tagsList.append(template)
    }
    new MultiSelectTag('tags')
}

function tagsTemplate (tag) {
    return `
    <option value="${tag.id}">${tag.name}</option>
    `
}