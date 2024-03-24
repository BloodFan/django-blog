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