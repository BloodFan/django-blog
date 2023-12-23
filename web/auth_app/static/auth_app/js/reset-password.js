console.log('passwordReset_start')
$(function () {

    const params = new Proxy(new URLSearchParams(window.location.search), {
      get: (searchParams, prop) => searchParams.get(prop),
    });
    let token = params.token;
    let uid = params.uid;

    $.ajax({
        url: '/api/v1/auth/password/reset/validate/',
        type: 'POST',
        data: {
            'token': token,
            'uid': uid
        },
        success: successHandler,
        error: errorHandler
      })
});

function successHandler(data){
    alert("Token and uid validated successfully!")
    $(function () {
        $('#passwordReset').submit(passwordReset);
      });
  }

function errorHandler(data){
    alert("Invalid token or/and uid.")
    window.location.href='/login/'
  }

function passwordReset(e) {
    let form = $(this);
    e.preventDefault();

    const myKeyValue = window.location.search;
    const urlParams = new URLSearchParams(myKeyValue);
    const token = urlParams.get('token');
    const uid = urlParams.get('uid');

    $.ajax({
        url: '/api/v1/auth/password/reset/confirm/',
        type: 'POST',
        data: form.serialize() + '&token='+token+'&uid='+uid,
        success: function(data) {
        alert("Password restored successfully.")
        window.location.href='/login/'
        },
        error: function(data) {
        console.log('error', data)
        }
    })
  }