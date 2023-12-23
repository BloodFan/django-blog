$(function () {
    articleDetail()
    tagList()
    commentsList()
    $('#commentCreate').submit(commentCreate);
    // $('#likeForm').submit(likeHandler); // старый вариант с формами лайка и дизлайка
    $('#likeButton').click(likeHandler);
    // $('#dislikeForm').submit(likeHandler);
    $('#dislikeButton').click(likeHandler);
});


function articleDetail () {
  let slug = window.location.pathname.split('/').filter(Boolean).slice(-1)
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

function tagTemplate (tag) {
  return `
  <a href="" data-id=${tag.id} class='articleTags'><span class="label label-info">${tag.name}</span></a>
  `
}


function articleTemplate (article) {
  let tags = article.tags.map(tag=>tagTemplate(tag)).join('')
  return `
  <div class="col-lg-8" id="articledetail">

    <!-- the actual blog post: title/author/date/content -->
    <h1><a href="">${article.title}</a></h1>
    <p class="lead"><i class="fa fa-user"></i> by <a href="${article.author.url}">${article.author.full_name}</a>
    </p>
    <hr>
    <p><i class="fa fa-calendar"></i> Posted on ${article.created}</p>
    <p><i class="fa fa-tags"></i> Tags: ${tags}
    <hr>
    <img src=${article.image} class="img-responsive">
    <hr>
    <p class="lead">
      ${article.content}
    <hr>
  </div>
  `
}

function successHandler (data) {
  console.log('success article', data)

  setVariable(data)
  updateArticleColor(data.user_like_status);

  $('#commentCount').text(`Comments (${data.comments_count})`)

  const articleDetail = $('#articleDetail')

  const template = articleTemplate(data)
  articleDetail.append(template)
  $('.articleTags').click(tagClickHandler)
}


function tagClickHandler(e) {
  e.preventDefault();
  const tag = $(this)
  const tag_id = tag.attr('data-id')
  const url = new URL(window.location);
  url.pathname = '/blog/'
  url.searchParams.set('tags', tag_id);
  window.history.pushState(null, '', url.toString());
  location.replace(url); // область видимости
}


function commentCreate (e) {
  let slug = window.location.pathname.split('/').filter(Boolean).slice(-1)
  $('#articleSlug').val(slug)
  let form = $(this);
  e.preventDefault();
  console.log('here', form.serializeArray())
  $.ajax({
    url: `/api/v1/article/articles/${slug}/comments/`,
    type: 'POST',
    data: form.serialize(),
    success: function(data) {
      console.log('success', data)
      successCreateCommentHandler()
    },
    error: function(data) {
      console.log('error', data)
    }
  })
}

function successCreateCommentHandler(){
  console.log("Спасибо за comment")
  commentsList()
}


function commentsList () {
  let slug = window.location.pathname.split('/').filter(Boolean).slice(-1)
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


function commentChildTemplate(comment) {
  const template = `
    <li>
      <div class="comment-avatar"><img src="${comment.user.image}" alt=""></div>
      <div class="comment-box">
        <div class="comment-head">
          <h6 class="comment-name">
            <a href="${comment.user.url}">${comment.user.full_name}</a>
          </h6>
          <span>${comment.updated}</span>
        </div>
        <div class="comment-content">${comment.content}</div>
      </div>
    </li>
  `
  return template
}

function commentTemplate(comment){
  // console.log('comment', comment.user_like_status)
  // var likeCom = document.getElementById("commentColorLike");

  const childrenTemplate = comment.children.map(comment => commentChildTemplate(comment)).join('');
  const style = comment.user_like_status === 1 ? "color:red" : ""
  const template = `
    <li>
      <div class="comment-main-level">
        <div class="comment-avatar"><img src="${comment.user.image}" alt=""></div>
        <div class="comment-box">
          <div class="comment-head">
            <h6 class="comment-name by-author"><a href="${comment.user.url}">${comment.user.full_name}</a></h6>
            <span>${comment.updated}</span>
            <a href="#formReview" data-id="${comment.id}" data-name="${comment.user.full_name}" class="addChildComment"><i class="fa fa-reply"></i></a>
            <a href="#formReview" data-id="${comment.id}" data-vote="1" data-model="comment" id="comment${comment.id}" class="likeComment"><i style="${style}" class="fa fa-heart commentLike"></i></a>
          </div>
          <div class="comment-content">
            ${comment.content}
          </div>
        </div>
      </div>
      <ul class="comments-list reply-list">
        ${childrenTemplate}
      </ul>
    </li>
  `
  return template;
}

function successCommentsHandler (data) {
  let commentsList = $('#paginationComment')
  commentsList.empty()
  // for (let comment of data){
  //     const template = commentTemplate(comment)

  //     commentsList.append(template)
  // }
  commentsList.append(data.map(comment=>commentTemplate(comment)).join(''))
  $('.addChildComment').click(childCommentHandler)
  $('.likeComment').click(likeHandler);

}

function childCommentHandler(){
  const form = document.getElementById('commentCreate')
  form.parent.value = $(this).attr('data-id')
  let name = $(this).attr('data-name')
  form.content.value = `to ${name}, `
}

function likeHandler(e){
  // let form = $(this);
  const model = $(this).data('model');
  const id = $(this).data('id');
  const vote = $(this).data('vote');
  let form = {'model': model, 'object_id': id, 'vote': vote}
  e.preventDefault();
  $.ajax({
      url: '/api/v1/actions/vote/',
      type: 'POST',
      data: form,
      // data: form.serialize(),
      success: function(data) {
        console.log('success', data)
        successLikeHandler(data, id)
      },
      error: function(data) {
        console.log('error', data)
      }
    })
}
  
function successLikeHandler(data, id){
  console.log(data, "Спасибо за оценку.", id)
  if (data.model == 'article'){
    updateArticleColor(data.status)
  } else if (data.model == 'comment') {
    updateCommentColor(id, data.status)
  }
}

function updateCommentColor(id, like_status) {
  const comment = document.querySelector(`#comment${id}`);
  const like = comment.querySelector('i.commentLike');
  if (like_status === 2) {
    like.style.color = "";
  } else if (like_status === 1) {
    like.style.color = "red";
  }
}

function updateArticleColor(like_status) {
  var dislike = document.getElementById("dislikeButton");
  var like = document.getElementById("likeButton");

  if (like_status === 0) {
    like.style.color = "green";
    like.style.backgroundColor = "";
    dislike.style.color = "";
    dislike.style.backgroundColor = "red";

  } else if (like_status === 1) {
    like.style.color = "";
    like.style.backgroundColor = "green";
    dislike.style.color = "red";
    dislike.style.backgroundColor = "";
  }
  else if (like_status === 2) {
    like.style.backgroundColor = "";
    dislike.style.backgroundColor = "";
    like.style.color = "green";
    dislike.style.color = "red";
  }
}

function setVariable(data){
  // $("#object_id").val(data.id); // record id in hidden-field to post-request
  // $("#object_id_2").val(data.id); // record id in hidden-field to post-request
  $("#likeButton").data("id", data.id); // ЗАНЯТНО, в Button поля 'data-id' нет и при просмотре кода страницы не указывается data-id, НО работает
  $("#dislikeButton").data("id", data.id);
}