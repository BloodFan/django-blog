$(function () {
  $('#forgotPasswordForm').submit(forgotPasswordForm);
});

function forgotPasswordForm(e) {
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: '/api/v1/auth/password/reset/',
    type: 'POST',
    data: form.serialize(),
    success: function(data) {
      console.log('success', data)
      successHandler(data)
    },
    error: function(data) {
      console.log('error', data)
    }
  })
}

function successHandler(data){
  alert("подтверждающее письмо на замену пароля отправлено!")
  window.location.href='/login/'
}
