(function ($) {

    $(document).ready(function () {
        $('.changes-review-checkbox').change(function () {
            let that = this;
            const change_id = $(that).val();
            const is_checked = that.checked;
            $.ajax("review_rsvp_changes/" + change_id, {
                data: JSON.stringify({'reviewed': is_checked}),
                contentType: 'application/json',
                type: 'POST',
                success: function(data) {
                    let parent = $($(that).parents('tr')[0]);
                    parent.removeClass('success info');
                    if (is_checked) {
                        parent.addClass('info');
                    } else {
                        parent.addClass('success');
                    }
                }
            });
        });
    });
})(jQuery);
