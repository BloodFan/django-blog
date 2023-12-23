$(function() {
    $('#createBlog').submit(createBlog);
    $(".file-upload").on('change', fileUploadHandler);
});


function createBlog(e){
    let form = $(this);
    e.preventDefault();
    console.log('here', form.serialize())
    $.ajax({
        url: '/api/v1/article/articles/',
        type: 'POST',
        data: form.serialize(),
        success: function(data) {
          console.log('success', data)
          successHandler()
        },
        error: function(data) {
          console.log('error', data)
        }
      })
}
    
function successHandler(){
    console.log("Спасибо за пост")
    window.location.href='/blog/'
}


function fileUploadHandler(e) {
    const files = this.files
    if (files) {
        var reader = new FileReader();

        reader.onload = function (e) {
            console.log('3', $(this))
            $('#image').attr('value', e.target.result)
        }

        reader.readAsDataURL(files[0]);
    }
}
