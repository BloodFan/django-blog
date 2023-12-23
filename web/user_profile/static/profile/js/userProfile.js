$(function () {
    userProfile()
});

function userProfile () {
    let id = window.location.pathname.split('/').filter(Boolean).slice(-1)
      $.ajax({
          url: `/api/v1/user-profile/profile/${id}/`,
          type: 'get',
          success: function(data) {
            successProfileHandler(data)
          },
          error: function(data) {
            console.log('error', data)
          }
      })
};

function successProfileHandler (data) {
    console.log('success', data)
    const profile = $('#first_menu')
    const template = profileTemplate(data)
    profile.append(template)
    setVariable(data)
    $('#follow').click(followHandler);
};

function profileTemplate (user) {

  if (user.is_follower === false){
    var button = `<button id="follow" data-id="${user.id}" class="btn btn-lg btn-success" type="submit"><i class="glyphicon glyphicon-ok-sign"></i> Подписаться.</button>`
  }
  else if (user.is_follower === true) {
    var button = `<button id="follow" data-id="${user.id}" style="background-color: red;" class="btn btn-lg btn-error" type="submit"><i class="glyphicon glyphicon-ok-sign"></i>  Отписаться.</button>`
  }
  
    return `
  <form class="form" action="##" id="updateProfile" method="post" >
    <div class="form-group">
        <div class="col-xs-6">
            <label for="first_name"><h4> first name </h4></label>
            <input type="text" class="form-control" name="first_name" value=${user.first_name} id="first_name" placeholder="first name" title="enter your first name if any.">
        </div>
    </div>
    <div class="form-group">
        <div class="col-xs-6">
          <label for="last_name"><h4>Last name</h4></label>
            <input type="text" class="form-control" name="last_name" value=${user.last_name} id="last_name" placeholder="last name" title="enter your last name if any.">
        </div>
    </div>
    <div class="form-group">
        <div class="col-xs-6">
            <label for="email"><h4>Email</h4></label>
            <input type="email" class="form-control" name="email" value=${user.email} id="email" placeholder="you@email.com" title="enter your email.">
        </div>
    </div>
    <div class="form-group">
      <div class="col-xs-6">
          <label for="birthday"><h4>birthday</h4></label>
          <input type="date" class="form-control" name="birthday" value=${user.birthday} id="birthday" placeholder="birthday" title="enter your birthday.">
      </div>
    </div>
    <div class="form-group">
      <div class="col-xs-6">
          <label for="gender"><h4>gender</h4></label>
          <select class="form-control" name="gender" id="gender" placeholder="gender" title="enter your gender.">
            <option value="" selected disabled hidden>Choose here</option>
            <option value=0>Not_known</option>
            <option value=1>Male</option>
            <option value=2>Female</option>
            <option value=9>Not_applicable</option>
          </select>
      </div>
    </div>
  </form>
  <div class="form-group">
    <div class="col-xs-12">
       <br>
        ${button}
    </div>
  </div>
    `
}

function setVariable (data) {
    document.getElementById("imageAvatar").src=data.image; // вывод аватарки
    var link = document.getElementById("followingLink"); // список на кого подписан user
    link.setAttribute("href", "/profile/subscriptions/?search=following&user_id="+data.id);
    var link = document.getElementById("followersLink");// список кто подписан на user'a
    link.setAttribute("href", "/profile/subscriptions/?search=followers&user_id="+data.id);
    $("#gender").val(data.gender); // актуальное значение поля "gender"
    $('#likesCount').text(` ${data.like_count}`); // количество лайков
    $('#commentCount').text(` ${data.comment_count}`); // количество комментариев
    $('#articleCount').text(` ${data.article_count}`); // количество постов
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
      successFollowHandler(data)
    },
    error: function(data) {
      console.log('error', data)
    }
  })
}


function successFollowHandler (data) {
  console.log('success', data)
  updateFollowButton(data.status)
};


function updateFollowButton(status){
  const button = document.querySelector(`#follow`);
  if (status === false) {
    button.style.backgroundColor = "";
    button.textContent = "Подписаться";

  } else if (status === true) {
    button.style.backgroundColor = "red";
    button.textContent = "Отписаться";
  }
}