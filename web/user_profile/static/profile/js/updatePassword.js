$(function () {
    $('#updatePassword').submit(updatePassword);
});

function updatePassword (e) {
    let form = $(this);
    e.preventDefault();
    console.log('here', form.serializeArray())
    $.ajax({
        url: `/api/v1/user-profile/change-password/`,
        type: 'POST',
        data: form.serialize(),
        success: successUpdatePasswordHandler,
        error: function(data) {
          console.log('error', data)
        }
      })
}

function successUpdatePasswordHandler(data){
    console.log("Обновление пароля", data)
    alert('Пароль обновлен успешно!')
}