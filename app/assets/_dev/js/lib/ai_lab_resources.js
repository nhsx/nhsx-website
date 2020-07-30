document.addEventListener("DOMContentLoaded", function () {
  var loadResources = document.querySelector("#loadResources");
  var resourceContainer = document.querySelector("#resources");

  if (!loadResources || !resourceContainer) {
    return;
  }

  loadResources.addEventListener("click", function (event) {
    var url = this.getAttribute("href");

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.setRequestHeader('x-requested-with', 'XMLHttpRequest');
    xhr.onload = function () {
      if (xhr.status === 200) {
        resourceContainer.innerHTML += xhr.responseText
        var nextPage = xhr.getResponseHeader("next_page")
        if (nextPage) {
          url = url.replace(/page=(\d+)/, "page=" + nextPage);
          loadResources.setAttribute("href", url);
        } else {
          loadResources.remove();
        }
      }
    };
    xhr.send();

    event.preventDefault();
  })
})
