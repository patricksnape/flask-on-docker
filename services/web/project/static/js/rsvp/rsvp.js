(function ($) {

    $(document).ready(function () {
        $('#attending-radio input[type=radio][name=attending]').change(function () {
            if ($(this).val() === '1') {
                $('#attending-content').fadeIn();
            } else {
                $('#attending-content').fadeOut();
            }
        });

        $('#attending-radio .disabled').click(function (e) {
            e.stopPropagation();
            e.preventDefault();
            e.stopImmediatePropagation();
            return false;
        });
    });
})(jQuery);
