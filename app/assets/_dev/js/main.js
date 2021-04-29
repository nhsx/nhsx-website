var scrollToTopButton = document.getElementById("js-top");

if (scrollToTopButton) {
  var contents = document.getElementById("contents").offsetTop;
}

var scrollFunc = function scrollFunc() {
  // Get the current scroll value
  var y = window.scrollY; // If the scroll value is greater than the window height show top link

  if (y > contents) {
    scrollToTopButton.classList.add("sticky-link--show");
  } else {
    scrollToTopButton.classList.remove("sticky-link--show");
  }
};

if (scrollToTopButton) {
  window.addEventListener("scroll", scrollFunc);
  document.addEventListener("DOMContentLoaded", function () {
    scrollFunc();
  });
}
