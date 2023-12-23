console.log('sing-up')
$(function () {
  $('#signUpForm').submit(singUp);
});

function singUp(e) {
  let form = $(this);
  e.preventDefault();
  console.log('here', form.serializeArray())
  $.ajax({
    url: '/api/v1/auth/sign-up/',
    type: 'POST',
    data: form.serialize(),
    success: function(data) {
      console.log('success', data)
      successHandler(data)
    },
    error: function(data) {
      alert('error', data)
    }
  })
}

function successHandler(data){
  alert("Спасибо за регистрацию, ожидайте письмо на email")
}
