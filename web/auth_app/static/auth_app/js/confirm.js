console.log('confirm_start')
$(function () {

    // const myKeyValue = window.location.search;
    // const urlParams = new URLSearchParams(myKeyValue);
    // const key = urlParams.get('key');

    const params = new Proxy(new URLSearchParams(window.location.search), {
      get: (searchParams, prop) => searchParams.get(prop),
    });
    let key = params.key;

    console.log('key:', key)
    $.ajax({
        url: '/api/v1/auth/confirm/',
        type: 'POST',
        data: {'key': key},
        success: successHandler,
        error: errorHandler
      })
});

function successHandler(data){
    alert("Спасибо за подтверждение, Ваш аккаунт активирован!")
    window.location.href='/login/'
  }

function errorHandler(data){
    alert("Ошибка регистрации")
  }