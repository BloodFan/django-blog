$(function () {
    userProfile()
});

function userProfile () {
      $.ajax({
          url: `/api/v1/user-profile/own-profile/`,
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
    const profile = $('#first_menu')
    const template = profileTemplate(data)
    profile.append(template)
    setVariable (data)
    $("#loadImage").on('change', fileUploadHandler); // загрузка обновленной аватарки
    $('#updateProfile').submit(updateProfile); 
};

function profileTemplate (user) {
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
    <div class="form-group">
         <div class="col-xs-12">
              <br>
                <button class="btn btn-lg btn-success" type="submit"><i class="glyphicon glyphicon-ok-sign"></i> Save</button>
                 <button class="btn btn-lg" type="reset"><i class="glyphicon glyphicon-repeat"></i> Reset</button>
          </div>
    </div>
  </form>
    `
}

function updateProfile (e) {
    let form = $(this);
    e.preventDefault();
    console.log('here', form.serializeArray())
    $.ajax({
        url: `/api/v1/user-profile/own-profile/`,
        type: 'POST',
        data: form.serialize(),
        success: successUpdateProfileHandler,
        error: function(data) {
          console.log('error', data)
        }
      })
}
    
function successUpdateProfileHandler(data){
    console.log("Обновление данных профайла", data)
    alert('Данные профиля обновлены успешно!')
}

function fileUploadHandler(e) {
    const files = this.files
    if (files) {
        var reader = new FileReader();

        reader.onload = function (e) {
            console.log('3', $(this))
            updateImage(e.target.result)
            // $('#image').attr('value', e.target.result)
        }

        reader.readAsDataURL(files[0]);
    }
}

function updateImage (e) {
  console.log('here')
  let form = {'image': e}
  // e.preventDefault();
  $.ajax({
      url: `/api/v1/user-profile/image/`,
      type: 'POST',
      data: form,
      success: successUpdateProfileHandler,
      error: function(data) {
        console.log('error', data)
      }
    })
}

function setVariable (data) {
  document.getElementById("imageAvatar").src=data.image; // вывод аватарки
  $("#gender").val(data.gender); // актуальное значение поля "gender"
  $('#likesCount').text(` ${data.like_count}`); // количество лайков
  $('#commentCount').text(` ${data.comment_count}`); // количество комментариев
  $('#articleCount').text(` ${data.article_count}`); // количество постов
}