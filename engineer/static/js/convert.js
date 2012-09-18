(function ($, markdown) {
  $(document).ready(function () {
    var $wrap = $("#id_body"),
        template = $("#template").html(),
        last_date;

    function formatDate(d) {
        var dobj = new Date(d),
            months = ['Jan', 'Feb', 'March', 'April', 'May', 'June',
                      'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        function pad(t) {
            return t < 10 ? "0" + t : t;
        }

        return {
                date: months[dobj.getMonth()] + ' ' + dobj.getDate(),
                time: pad(dobj.getHours()) + ':' + pad(dobj.getMinutes())
               }
    }

    function transform(t, e) {
        var d = formatDate(e.datetime);

        e.date = d.date;
        e.time = d.time;

        e.text = markdown.toHTML(e.text)
		t=e.text;
        return t;
    }

    function render($j, data) {
        var prev_date, e, d;
        $j.html("");
        for(var i=0, l=data.length; i<l; i++) {
            e=data[i], d=formatDate(e.datetime);
            e["class"] = prev_date == d.date ? "hide-date" : "";
            prev_date = last_date = d.date;

            $j.append(transform(template, e));
        }
        setTimeout(function () {
            window.scrollTo(0, $("#id_body_markdown").offset().top);
            $("#id_body_markdown").val(localStorage.draft_text).focus();
        }, 100);
    }
    function init(reinit) {
		$("#id_body").parents('div').eq(0).after("<div id='preview'></div>");
        $("#preview").html(markdown.toHTML(localStorage.draft_text));

    }

    function getData() {
		var data = {text: "", datetime: (new Date).toJSON(), type: "text", place: "", lat: "", lon:""};
		data.text = $("#id_body_markdown").val();
		data.place = $("#place").val();
        return data;
    }

    function preview(e) {
        var d = getData();
        if ($("#id_body_markdown").val().trim()) {
            d["class"] = (formatDate(d.datetime).date == last_date) ? "hide-date" : "";
			var html = transform(template, d);
            $("#id_body").val(html);
			$("#preview").html(html);

            window.scrollTo(0, $("#id_body_markdown").offset().top);
        } else {
            $("#preview").html("");
        }
    }

    $("#preview-btn").click(preview);
    $("#submit-btn").click(function () {
        var d = getData();
        if (d.text.trim() != "") {
            $.ajax({
                type: 'POST',
                url: '/journal',
                data: d,
                success: function () {
                    alert("Successfully added!");
                    localStorage.draft_text = "";
                    init(true);
                }
            });
        }
    });

    var live_preview, wait=400;
    $("#id_body_markdown").keyup(function () {
            clearTimeout(live_preview);
            live_preview = setTimeout(preview, wait);
        localStorage.draft_text = $(this).val();
    });
	
    localStorage.live_preview = true;
    init();
  });
})(Zepto, markdown);
