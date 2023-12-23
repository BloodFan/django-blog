$(function () {
    tagDetail()
});


function tagDetail () {
  let slug = window.location.pathname.split('/').filter(Boolean).slice(-1)
  console.log(slug)
    $.ajax({
        url: `/api/v1/article/tags/${slug}/`,
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
  console.log('success', data)
  const tagDetail = $('#tagDetail')

  const template = tagTemplate(data)
  tagDetail.append(template)

}


function tagTemplate (tag) {
  return `

    <p>Name tag: ${tag.name}</p>
    <p>Description tag: ${tag.description}</p>
    <p>Slug tag: ${tag.slug}</p>

  </div>
  `
}