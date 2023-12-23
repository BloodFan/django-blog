$(function () {
    $('#modalButton').click(getListSubscribers);
});

function getListSubscribers () {
      $.ajax({
          url: `/api/v1/actions/subscriber-list/`,
          type: 'get',
          success: function(data) {
            successListFollowersHandler(data)
          },
          error: function(data) {
            console.log('error', data)
          }
      })
  };

function successListFollowersHandler (data) {
    console.log('success List Followers', data)
    var modal = document.getElementById("myModal");

    var content = modal.querySelector(".modal-content");
    content.innerHTML = "";

    var closeBtn = document.createElement("span");
    closeBtn.classList.add("close");
    closeBtn.innerHTML = "&times;";

    closeBtn.addEventListener("click", function() {
    modal.style.display = "none";
    });

    content.appendChild(closeBtn);

    for (let subscriber of data){
        var template = subscriberTemplate(subscriber)
        var item = document.createElement("li");
        item.innerText = template;
        content.append(item);
    }

    modal.style.display = "block";

    span.onclick = function() {
        modal.style.display = "none";
      };
}

function subscriberTemplate(subscriber) {
    return `<a href="${subscriber.url}" >${subscriber.full_name}</a>`
}