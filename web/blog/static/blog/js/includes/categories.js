$(function() {
    categoryList()
});

function categoryList() {
    $.ajax({
        url: '/api/v1/article/categories/',
        type: 'get',
        success: successCategoryHandler
    })
};

function successCategoryHandler(data){
    const categoryList = $('#loadCategory')
    categoryList.empty()
    categoryList.append('<option disabled selected value> -- select an category -- </option>')
    for (let category of data){
        const template = categoryTemplate(category)
  
        categoryList.append(template)
    }
}

function categoryTemplate (category) {
    return `
    <option value="${category.id}">${category.name}</option>
    `
}