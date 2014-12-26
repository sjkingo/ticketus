$(document).ready(function() {
    $('.top-tags a').click(function() {
        var tag_name = $.trim($(this).text());
        var tagbox = $('#tags');
        tagbox.val(tagbox.val() + ' ' + tag_name);
    });
});
