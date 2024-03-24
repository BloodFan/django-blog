$(function () {
    getNewsLine()
});


function getNewsLine () {
    console.log('success News Line')
    $.ajax({
        url: `/api/v1/actions/news-list/`,
        type: 'get',
        success: function(data) {
        successNewsLine(data)
        },
        error: function(data) {
        console.log('error', data)
        }
    })
};

function successNewsLine (data) {
    console.log('success News Line', data)
    const newsline = $('#newsline')

    const list = $('<ul></ul>')

    newsline.empty()
    for (let news of data){
        var template = getTemplate (news)
        const listItem = $('<li></li>')
        listItem.html(template)
        list.append(listItem)
        listItem.after('<hr>')
    }
    newsline.append(list)
    $('.familiarization').click(createFamiliarization)
}

function createFamiliarization(e) {
    const actionItem = $(this)
    const actionId = actionItem.data('id')
    e.preventDefault();
    let form = {'id': actionId}
    $.ajax({
        url: '/api/v1/actions/familiarization/',
        type: 'POST',
        data: form,
        success: function(data) {
          console.log('success')
          successFamiliarization(actionItem)
        },
        error: function(data) {
          console.log('error', data)
        }
      })
}

function successFamiliarization(actionItem) {
    actionItem.find('i.icon-check-empty').replaceWith('<i class="fa fa-check"></i>')
}

function getTemplate (news){
    if (news.event == 'update_avatar') {
        var template = updateAvatarTemplate(news)
    }
    else if(news.event == 'create_like_article') {
        var template = createLikeArticleTemplate(news)
    }
    else if(news.event == 'create_like_comment') {
        var template = createLikeCommentTemplate(news)
    }
    else if(news.event == 'create_article') {
        var template = createArticleTemplate(news)
    }
    else if(news.event == 'create_comment') {
        var template = createCommentTemplate(news)
    }

    return template
}


function updateAvatarTemplate(data) {
    // <img class="avatar img-circle img-thumbnail" src="${data.user.image}" alt="" style="width: 15%; height: 10%;">
    date = formattedDate(data)
    return `
    <div class="row">
        <button data-id=${data.id} class="familiarization"><i class="icon-check-empty"></i> </i></button>
        ${date} <a href="${data.user.url}" >${data.user.full_name}(профиль, id=${data.user.id})</a> обновил аватар.
    </div>
    <div class="row" style="text-align: center">
        <img class="avatar img-circle img-thumbnail" src="${data.meta.image}" alt="" style="width: 15%; height: 10%;">
    </div>
    `
}

function createLikeArticleTemplate(data) {
    date = formattedDate(data)
    return `
    <div class="row">
        <button data-id=${data.id} class="familiarization"><i class="icon-check-empty"></i> </i></button>
        ${date} <a href="${data.user.url}" >${data.user.full_name}(профиль, id=${data.user.id})</a> поставил лайк <a href="${data.content_object.url}" >посту</a>.
    </div>
    `

}

function createLikeCommentTemplate(data) {
    date = formattedDate(data)
    return `
    <div class="row">
        <button data-id=${data.id} class="familiarization"><i class="icon-check-empty"></i> </i></button>
        ${date} <a href="${data.user.url}" >${data.user.full_name}(профиль, id=${data.user.id})</a> поставил лайк комментарию в <a href="${data.content_object.url}" >посте</a>.
    </div>
    `

}

function createArticleTemplate(data) {
    date = formattedDate(data)
    return `
    <div class="row">
        <button data-id=${data.id} class="familiarization"><i class="icon-check-empty"></i> </i></button>
        ${date} <a href="${data.user.url}" >${data.user.full_name}(профиль, id=${data.user.id})</a> создал новый пост: <a href="${data.content_object.url}" >${data.content_object.title}</a>.
    </div>
    `
}

function createCommentTemplate(data) {
    date = formattedDate(data)
    return `
    <div class="row">
        <button data-id=${data.id} class="familiarization"><i class="icon-check-empty"></i> </i></button>
        ${date} <a href="${data.user.url}" >${data.user.full_name}(профиль, id=${data.user.id})</a> написал комментарий к <a href="${data.content_object.url}?scrollTo=comment${data.object_id}" >посту</a>.
    </div>
    `
}

function formattedDate(data){
    const date = new Date(data.date)
    const formatter = new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: '2-digit', year: 'numeric' });
    const formattedDate = formatter.format(date);
    return formattedDate
}