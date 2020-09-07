function initAutoPopulateSlugFromMeetingDate() {
  var slugFollowsTitle = false;

  $('#id_meeting_date').on('focus', function () {
    /* slug should only follow the title field if its value matched the title's value at the time of focus */
    var currentSlug = $('#id_slug').val();
    // If select value is not empty we get current selection's label.
    var value = this.value;
    var slugifiedTitle = cleanForSlug(value, true);
    slugFollowsTitle = (currentSlug == slugifiedTitle);
  });

  $('#id_meeting_date').on('change', function () {
    if (slugFollowsTitle) {
      var slugifiedTitle = cleanForSlug(this.value, true);
      $('#id_slug').val(slugifiedTitle);
    }
  });
}

$(function () {
  /* Only non-live pages should auto-populate the slug from the title */
  if (!$('body').hasClass('page-is-live') && $('body').hasClass('model-meetingminutes')) {
    initAutoPopulateSlugFromMeetingDate();
  }
});
