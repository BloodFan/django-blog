$(function () {
    articleList()
    tagList()

});

console.log('blog-list')

function articleList () {
  const params = new URLSearchParams(window.location.search);
    $.ajax({
        url: `/api/v1/article/articles/?${params.toString()}`,
        type: 'get',
        success: successHandler
    })
};

function successHandler (data) {
    console.log('success', data)
    const articleList = $('#articleList')
    articleList.empty()
    for (let article of data.results){
        const template = articleTemplate(article)
  
        articleList.append(template)
    }
    $('.articleTags').click(tagClickHandler)
}


function tagTemplate (tag) {
  return `
    <a href="" data-id=${tag.id} class='articleTags'><span class="label label-info">${tag.name}</span></a>
  `
}

function tagClickHandler(e) {
  e.preventDefault();
  const tag = $(this)
  const tag_id = tag.attr('data-id')
  const url = new URL(window.location);
  url.searchParams.set('tags', tag_id);
  window.history.pushState(null, '', url.toString());
  articleList()
}
function rend(tag){
  return tagTemplate(tag)
}

function articleTemplate (article) {
  // let tags = article.tags.map(
  //   function (tag) {
  //     return tagTemplate(tag)
  //   }
  // )
  const date = new Date(article.updated)
  const formatter = new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: '2-digit', year: 'numeric' });
  const formattedDate = formatter.format(date);
  let tags = article.tags.map(tag=>tagTemplate(tag)).join('')
    return `
<div class="row">
  <div class="col-md-12 post">
    <div class="row">
      <div class="col-md-12">
        <h4>
          <strong>
            <a href="${article.url}" class="post-title">${article.title}</a>
          </strong>
        </h4>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12 post-header-line">
        <span class="glyphicon glyphicon-user"></span>by <a href="${article.author.url}">${article.author.full_name}</a> |
        <span class="glyphicon glyphicon-calendar"></span> posted on ${formattedDate} |
        <span class="glyphicon glyphicon-comment"></span><a href="#"> ${article.comments_count} Comments</a> |
        <i class="icon-share"></i><a href="#">39 Shares</a> |
        <i class="icon-share"></i><a href="#">Rating: ${article.rating}</a> |
        <span class="glyphicon glyphicon-tags"></span> Tags: ${tags}
      </div>
    </div>
    <div class="row post-content">
      <div class="col-md-3">
        <a href="#">
          <img
            src=${article.image}
            // alt="" class="img-responsive">
        </a>
      </div>
      <div class="col-md-9">
        <p>
            ${article.content}
        </p>
        <p>
          <a class="btn btn-read-more" href="${article.url}">Read more</a>
        </p>
      </div>
    </div>
  </div>
</div>
    `
}

// не реализовано
function updateQueryStringParameter(uri, key, value) {
  var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
  var separator = uri.indexOf('?') !== -1 ? "&" : "?";
  if (uri.match(re)) {
    return uri.replace(re, '$1' + key + "=" + value + '$2');
  }
  else {
    return uri + separator + key + "=" + value;
  }
}

// ПЕРВАЯ СТРОКА:
// "([?&])" начало захвата, соответствует одному символу из: ? или &
// key - передаваемый в функцию ключ
// "=.*?(&|$)"
//   =  это просто равенство, пример: tags=1
//   .  точка соответствует любому символу
//   *? соответствует предыдущему токену от нуля до бесконечности, то есть, (key + "=.*?" ) может принять ключ с value любого размера
// (&|$) конец захвата: или &(следующий элемент поиска) или $ - символ утверждает позицию в конце строки
// "i" - это флаг, без учета регистра

// ВТОРАЯ СТРОКА:
// Метод indexOf() возвращает первый индекс, по которому данный элемент может быть найден в массиве или -1, если такого индекса нет.
// тернарный оператор: если uri.indexOf('?') !== -1, то возвращается "&", иначе возвращается "?"