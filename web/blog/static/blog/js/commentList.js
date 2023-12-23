$(function () {
  console.log('commentlist js')
  commentsList()
});

function commentsList () {
  let slug = window.location.pathname.split('/').filter(Boolean).slice(-1)
  console.log('commentsList')
    $.ajax({
        url: `/api/v1/article/articles/${slug}/comments/`,
        type: 'get',
        success: function(data) {
          console.log('success commentsList', data)
          successCommentsHandler(data)
        },
        error: function(data) {
          console.log('error', data)
        }
    })
};

function commentChildrenTemplate (comment) {
  
  return `
  <li>
  <h3><i class="fa fa-comment"></i> ${comment.name} says:
   <small> ${comment.updated}</small>
  </h3>
  <p>${comment.content}</p>
  </li>
  `
}



function commentTemplate (comment) {

  let childrenList = comment.children.map(children=>commentChildrenTemplate(children)).join('')

  return `
  <h3><i class="fa fa-comment"></i> ${comment.name} says:
   <small> ${comment.updated}</small>
  </h3>
  <h5>
    <button data-id="${comment.id}" data-name="${comment.name}" type="button" class="addChildComment">Ответить</button>
  </h5> 
  <p>${comment.content}</p>
  <ul>
  ${childrenList}
  </ul>
  `
}

function successCommentsHandler (data) {

  let commentsList = $('#commentslist')
  commentsList.empty()
  // for (let comment of data){
  //     const template = commentTemplate(comment)

  //     commentsList.append(template)
  // }
  commentsList.append(data.map(comment=>commentTemplate(comment)).join(''))
  $('.addChildComment').click(childCommentHandler)
}

function childCommentHandler(){
  const form = document.getElementById('commentCreate')
  form.parent.value = $(this).attr('data-id')
  let name = $(this).attr('data-name')
  form.content.value = `to ${name}, `
}
