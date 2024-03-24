/// Список пользователей
$(function () {
    getUsersList()
    $('.order').click(orderClickHandler)
});

function getUsersList () {
    const params = new URLSearchParams(window.location.search);
    $.ajax({
        url: `/api/v1/user-profile/users-list/?${params.toString()}`,
        type: 'get',
        success: function(data) {
        successUsersList(data)
        },
        error: function(data) {
        console.log('error', data)
        }
    })
};

function successUsersList (data) {
    console.log('success Users List', data)
    const users = $('#users')

    const list = $('<ul style="text-align: center"></ul>')

    users.empty()
    for (let user of data){
        var template = userTemplate(user)

        const listItem = $('<li></li>')
        listItem.html(template)
        list.append(listItem)
    }
    users.append(list)
    $('.follow').click(followHandler);
}

function orderClickHandler(e) {
    e.preventDefault();
    const object = $(this)
    const order = object.attr('data-order')
    const url = new URL(window.location);
    url.searchParams.set('order', order);
    window.history.pushState(null, '', url.toString());
    getUsersList()
  }


function userTemplate(user) {
    if (user.is_follower === false){
        var button = `<button id="follow${user.id}" class="follow" data-id="${user.id}" style="background-color: green;" class="btn btn-lg btn-success" type="submit"><i class="glyphicon glyphicon-ok-sign"></i> Подписаться.</button>`
    }
    else if (user.is_follower === true) {
        var button = `<button id="follow${user.id}" class="follow" data-id="${user.id}" style="background-color: red;" class="btn btn-lg btn-error" type="submit"><i class="glyphicon glyphicon-ok-sign"></i>  Отписаться.</button>`
    }
    return `
    <img class="avatar img-circle img-thumbnail" src="${user.image}" alt="" style="width: 15%; height: 10%;">
    <a href="${user.url}" >${user.full_name}(профиль, id=${user.id})</a> | 
    <a href="/blog/?author=${user.email}" >Посты пользователя(${user.article_count})</a> | 
    ${button}
    `
}

function followHandler (e) {
    const id = $(this).data('id');
    let form = {'user_id': id,}
    e.preventDefault();
    $.ajax({
      url: `/api/v1/actions/following/`,
      type: 'post',
      data: form,
      success: function(data) {
        successFollowHandler(data, id)
      },
      error: function(data) {
        console.log('error', data)
      }
    })
  }
  
  
  function successFollowHandler (data, id) {
    console.log('success', data)
    updateFollowButton(data.status, id)
  };
  
  
  function updateFollowButton(status, id){
    const button = document.querySelector(`#follow${id}`);
    if (status === false) {
      button.style.backgroundColor = "green";
      button.textContent = "Подписаться";
  
    } else if (status === true) {
      button.style.backgroundColor = "red";
      button.textContent = "Отписаться";
    }
  }