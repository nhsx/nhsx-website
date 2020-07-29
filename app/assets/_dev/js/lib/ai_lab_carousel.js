document.addEventListener("DOMContentLoaded", function () {
  var carousels = document.querySelectorAll(".resource-block.carousel");

  if (!carousels) {
    return;
  }

  var moveIndexes = function (carousel, index) {
    var ordinal = 0;
    var items = carousel.querySelectorAll(".nhsuk-promo-group__item");
    var length = items.length;

    // Store the active index in the data attribute of the carousel
    if (index <= length - 1) {
      carousel.dataset.activeIndex = index;
    } else {
      carousel.dataset.activeIndex = 0;
    }

    // Let's move through the items in the carousel
    while (ordinal < length) {
      ordinal++;
      var item = items[index];

      // Check the item exists
      if (item) {
        item.style.setProperty("order", ordinal);
      }

      // If we're still in the source order of the
      // carousel, increment by one
      if (index < length - 1) {
        index++;
      } else {
        // If we've got to the end of the source order,
        // loop back round to the beginning
        index = 0;
      }
    }
  };

  var moveNext = function (carousel) {
    var items = carousel.querySelectorAll(".nhsuk-promo-group__item");
    // Get the index that we want the carousel to move to
    var activeIndex = Number(carousel.dataset.activeIndex) + 1;

    // If the index is greater than the maximium index in the
    // items, then we're starting at the beginning again
    if (activeIndex > items.length - 1) {
      activeIndex = 0;
    }

    moveIndexes(carousel, activeIndex);
  };

  var movePrevious = function (carousel) {
    var items = carousel.querySelectorAll(".nhsuk-promo-group__item");
    // Get the index that we want the carousel to move to
    var activeIndex = Number(carousel.dataset.activeIndex) - 1;

    // If the index is less than zero, we're moving to the
    // last item
    if (activeIndex < 0) {
      activeIndex = items.length - 1;
    }

    moveIndexes(carousel, activeIndex);
  };

  carousels.forEach(function (carousel) {
    var nextButton = carousel.querySelector(".next");
    var previousButton = carousel.querySelector(".previous");

    carousel.dataset.activeIndex = 0;

    nextButton.addEventListener(
      "click",
      function (event) {
        moveNext(carousel);
        event.preventDefault();
      },
      false
    );

    previousButton.addEventListener(
      "click",
      function (event) {
        movePrevious(carousel);
        event.preventDefault();
      },
      false
    );
  });
});
