$(function() {
    articleDetail()
    $('#editBlog').submit(editBlog);
    $(".file-upload").on('change', fileUploadHandler);
});

function articleDetail () {
    let slug = window.location.pathname.split('/').filter(Boolean).slice(-2, -1)[0]
    console.log('success slug', slug)
    $.ajax({
        url: `/api/v1/article/articles/${slug}/`,
        type: 'get',
        success: function(data) {
          successHandler(data)
        },
        error: function(data) {
          console.log('error', data)
        }
    })
  };

function successHandler (data) {
    console.log('success article', data)
    $('#title').val(data.title)
    $('#summernote').summernote('code', data.content);
    $('#loadCategory').val(data.category.id)
    // console.log('success tags', data.tags[0].id)
    // $('#tags').val(data.tags[0].id)
    // tagHandler(data.tags)
}

function editBlog(e){
    let form = $(this);
    e.preventDefault();
    console.log('here', form.serializeArray() )
    let slug = window.location.pathname.split('/').filter(Boolean).slice(-2, -1)
    $.ajax({
      url: `/api/v1/article/articles/${slug}/`,
      type: 'patch',
      data: form.serialize(),
      success: function(data) {
        console.log('success', data)
        editSuccessHandler()
      },
      error: function(data) {
        console.log('error', data)
      }
    })
}

function editSuccessHandler(){
  console.log("Пост обновлен!")
  let slug = window.location.pathname.split('/').filter(Boolean).slice(-2, -1)[0]
  window.location.href=`/blog/${slug}`
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


// function tagHandler(data){
//     tagList = $('.input-container')
//     for (let tag of data){
//         const template = tagTemplate(tag)
//         tagList.append(template)
//     }
// }

// function tagTemplate (tag) {
//     return `
//     <div class="item-container">
//         <div class="item-label" data-value="${tag.id}">${tag.name}</div>
//         <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="item-close-svg">
//                     <line x1="18" y1="6" x2="6" y2="18"></line>
//                     <line x1="6" y1="6" x2="18" y2="18"></line>
//         </svg>
//     </div>
//     `
// }