(function ($, undefined) {
    var MAX_LI_PER_COL = 7;
    $(document).ready(function () {
        $(".directory > ul > li").live('click', function () {
            var $ul = $(this).find("ul").clone(),
                $self = $(this);
            if (!$ul || $ul.length == 0) return;

            $(".submenu").anim({opacity: 0}, 0.1, "ease", function () {
                var $lis = $ul.find("li");
                $(".submenu").empty().append($ul);
                $self.siblings().removeClass("highlighted");
                $self.addClass("highlighted");
                $(".submenu").anim({opacity: 1}, 0.1);
            });
        });

        $(".directory > ul > li > span > a").live('click', function() {
            return false;
        });

        $(".tab-menu > ul > li > a").live('click', function () {
            var $tab = $(this).attr('href');
            $tab= $($tab).clone();
                $self = $(this);
            if (!$tab|| $tab.length == 0) return;
   
            $(".tab-body").anim({opacity: 0}, 0.1, "ease", function () {
                $(".tab-body").empty().append($tab);
                $self.parents('li').eq(0).addClass("active");
                $self.parents('li').eq(0).siblings().removeClass("active");
                $(".tab-body").anim({opacity: 1}, 0.1);
            });
    
        });
    });
})(Zepto);
