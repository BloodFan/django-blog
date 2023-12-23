$(function () {
    getListSubscribers()
});

function getListSubscribers () {
    const params = new URLSearchParams(window.location.search);
      $.ajax({
          url: `/api/v1/actions/subscriber-list/?${params.toString()}`,
          type: 'get',
          success: function(data) {
            successListFollowersHandler(data)
          },
          error: function(data) {
            console.log('error', data)
          }
      })
  };

function successListFollowersHandler (data) {
    console.log('success List Followers', data)
    const subscription = $('#subscription')

    const list = $('<ul style="text-align: center"></ul>')

    subscription.empty()
    for (let subscriber of data){
        var template = subscriberTemplate(subscriber)

        const listItem = $('<li></li>')
        listItem.html(template)
        list.append(listItem)
        // subscription.append(template);
    }

    subscription.append(list)
    $('.follow').click(followHandler);
}

function subscriberTemplate(subscriber) {
    if (subscriber.is_follower === false){
        var button = `<button id="follow${subscriber.id}" class="follow" data-id="${subscriber.id}" class="btn btn-lg btn-success" type="submit"><i class="glyphicon glyphicon-ok-sign"></i> Подписаться.</button>`
    }
    else if (subscriber.is_follower === true) {
        var button = `<button id="follow${subscriber.id}" class="follow" data-id="${subscriber.id}" style="background-color: red;" class="btn btn-lg btn-error" type="submit"><i class="glyphicon glyphicon-ok-sign"></i>  Отписаться.</button>`
    }
    return `
    <img class="avatar img-circle img-thumbnail" src="${subscriber.image}" alt="" style="width: 30%; height: 30%;">
    <a href="${subscriber.url}" >${subscriber.full_name}(ссылка на профиль, id=${subscriber.id})</a>
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