(function($, undefined){
    $(document).ready(function () {
        $(".list-container.editable tbody tr").each(function() {
            $(this).find('td').attr('contenteditable', 'true');
            var toolbar = $('<span class="btn-group" style="cursor:pointer; position: absolute; right: 6px; top: 4px"> \
                             <a class="btn btn-small"><i class="icon-trash"></i></a></span>');
            $(this).find("td").last().css('position', 'relative').append(toolbar);
            var updater = $('<a class="btn btn-small update-btn"><i class="icon-ok"></i></a>');
            $(this).keypress(function() {
                toolbar.prepend(updater);
            });
        });

        $(".list-container.editable tbody tr").each(function () {
            var $id = $(this).find("td").first(), i = $id.text(), url = $(this).parents(".list-container").eq(0).attr('data-url');
            $id.html('<a href="' + url  + i + '">' + i + '</a>');
            $id.attr('contenteditable', 'false');
        });
    });
})(jQuery);
