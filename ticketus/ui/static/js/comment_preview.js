$(document).ready(function() {
    function Preview(input, preview) {
        this.update = function() {
            preview.innerHTML = markdown.toHTML(input.value);
        };
        input.editor = this;
        this.update();
    }
    new Preview(document.getElementById('comment-text'), document.getElementById('preview-html'));
});
