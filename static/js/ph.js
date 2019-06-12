$(document).ready(function() {

    //在文档任意位置触发点击事件，将排序列表隐藏
    $(document).click(function () {
        $("#sort_list").hide();
    });

    //是否隐藏“高级搜索”
    $("#test").click(function () {
        var advanced_search = $("#sc_adv");
        var display = advanced_search.css('display');
        if (display === 'none') {
            advanced_search.show();
            $("#su").attr("disabled", false)
        } else {
            advanced_search.hide();
            $("#su").attr("disabled", true)
        }
    });

    //点击普通搜索框时，隐藏“高级搜索”
    $("#kw").click(function () {
        $("#sc_adv").hide();
    });

    var paper_datail_a = $("a[target=\"_blank\"]");

    //鼠标移进“论文题目”领域，paper颜色变为紫色
    paper_datail_a.mouseover(function () {
        $(this).css("border-bottom", "1px purple solid");
        $(this).css("color", "purple");

    });

    //鼠标移除“paper”领域，字体颜色变为黑色
    paper_datail_a.mouseout(function () {
        $(this).css("color", "black");
        $(this).css("border-bottom", "");
    });

    //用户点击“换页”的响应时间
    $("a.pagination-link").click(function () {
        var current_page = $("a.pagination-link.is-current");
        if ($(this).text() !== current_page.text()) {
            current_page.removeClass("is-current");
            current_page.removeAttr("aria-current");
            $(this).addClass("is-current");
            $(this).attr("aria-current", "page");
            $('body').prop('scrollTop','0');//滚动条滚到最上方
            get_data(true);
        }
    });

    //“下一页“的响应事件
    $("#next_page").on("click", function () {
        var current_page = $("a.pagination-link.is-current");
        var page_num = $("#page_num").val();

        if (parseInt(current_page.text()) < page_num) {
            current_page.removeClass("is-current");
            current_page.removeAttr("aria-current");
            var next_page = current_page.parent().next().children();
            if (next_page.length > 0) {
                next_page.addClass("is-current");
                next_page.attr("aria-current", "page");
            } else {
                var page_list = $("#page_list");
                page_list.empty();
                var current = parseInt(current_page.text());
                for (var i = 1; i < 10; i++) {
                    if (current + i <= page_num) {
                        var page = "<li><a class=\"pagination-link\"\n" +
                            "aria-label=\"Goto page" + (current + i) + "\">" + (current + i) + "</a></li>";
                        page_list.append(page);
                    }
                }

                page_list.children(":first").children().addClass("is-current");
                page_list.children(":first").children().attr("aria-current", "page");

            }

            $('body').prop('scrollTop','0');//滚动条滚到最上方
            get_data(true);


        }
    });

    //"上一页"的响应事件
    $("#previous_page").on("click", function () {
        var current_page = $("a.pagination-link.is-current");
        var page_num = $("#page_num").val();

        if (parseInt(current_page.text()) > 1) {
            current_page.removeClass("is-current");
            current_page.removeAttr("aria-current");
            var prev_page = current_page.parent().prev().children();

            if (prev_page.length > 0) {
                prev_page.addClass("is-current");
                prev_page.attr("aria-current", "page");
            } else {
                var page_list = $("#page_list");
                page_list.empty();
                var current = parseInt(current_page.text());
                for (var i = 1; i < 10; i++) {
                    if (current - i > 0) {
                        var page = "<li><a class=\"pagination-link\"\n" +
                            "aria-label=\"Goto page" + (current - i) + "\">" + (current - i) + "</a></li>";
                        page_list.prepend(page);
                    }
                }

                page_list.children(":last").children().addClass("is-current");
                page_list.children(":last").children().attr("aria-current", "page");

            }

            $('body').prop('scrollTop','0');//滚动条滚到最上方
            get_data(true);
        }


    });

    // 导航栏“year”是否显示更多
    $("#year_show_more,#fos_show_more,#author_show_more,#publisher_show_more").on("click", function () {
        var list = $(this).parent().parent();
        list.children().show();
        list.append($(this));
        $(this).hide();
    });



    //显示需排序的字段列表
    $("#button_sort").on("click", function (event) {
        var sort_list = $("#sort_list");
        if (sort_list.css('display') === 'none') {
            sort_list.show();
            event.stopPropagation();
        } else {
            sort_list.hide();
        }
    });

    //点击排序列表时，保证列表不会隐藏
    $("#sort_list").on("click", function (event) {
        event.stopPropagation();
    });

    //点击排序后的一系列响应事件
    $("a.dropdown-item").on("click", function () {

        var chosen_sort = $("#chosen_sort");
        var chosen_id = chosen_sort.text().toString().trim().toLowerCase() + "_sort";
        $("#" + chosen_id).show();
        var ele = $(this).text();
        chosen_sort.text(ele);
        $(this).hide();
        $("#sort_list").hide();
        get_data(false);
    });

    //导航栏year, fos , author, publisher的显示与否
    $("#year_arrow,#fos_arrow,#publisher_arrow,#author_arrow").on("click",function(){

        var menu = $(this).parent().next();
        if(menu.css('display') === 'none'){
            $(this).children().attr("class","fa fa-caret-down");
            menu.show();

        }else{
            $(this).children().attr("class","fa fa-caret-right");
            menu.hide();
        }
    });


    //
    $("a[style=\"font-size: 15px\"]").on("click", function () {
        if ($(this).hasClass("is-active")) {
            $(this).removeClass("is-active");
        } else {
            $(this).addClass("is-active");
        }
        get_data(false)
    });


    //过滤 选择的fos 的paper
    $("input[type='checkbox']").on("click", function (event) {
        event.stopPropagation();
        get_data(false);
    });


    //显示被点击fos的子类别
    $("a.is-black").on("click", function () {
        get_sub_fos($(this));
    });

});


    function get_sub_fos(current) {

        var fos_id = current.children(":first").val();
        var url = '/paper/get_fos_agg';
        //判断是高级搜索还是普通搜索
        if ($("#search_type").val() === "advanced") {
            content = {
                "title": $("#title").val(),
                "author_name": $("#author_name").val(),
                "author_org": $("#author_org").val(),
                "venue": $("#venue").val(),
                "keywords": $("#keywords").val(),
                "year": $("#year").val(),
                "fos": $("#fos").val(),
                "lang": $("#lang").val(),
                "publisher": $("#publisher").val(),
                "issn": $("#issn").val(),
                "doi": $("#doi").val(),
                "url": $("#url").val(),
                "abstract": $("#abstract").val(),
                "fos_id": fos_id,
                "type":"advanced"
            };
        } else {
            content = {
                "search_content": $("#kw").val(),
                "fos_id": fos_id,
                "type":"general"
            };
        }

        if(current.next().length > 0){
            current.next().toggle();
        }else {
            $.ajax({
                type: 'post',
                url: url,
                data: content,
                success: function (response) {
                    var response_json = JSON.parse(response);
                    if (response_json.length > 0) {
                        current.after("<ul></ul>");
                        for (var i = 0; i < response_json.length; i++) {
                            var fos = "<li><a class=\"is-black\">" +
                                "<input type=\"checkbox\" style=\"width:1.2em;height:1.2em\" value=" +
                                response_json[i].id + ">" +
                                response_json[i].name + "(" + response_json[i].count + ")" +
                                "</a></li>";
                            current.next().append(fos);
                            var last = current.next().children(":last").children(":first");
                            last.on("click", function(){
                                get_sub_fos($(this));
                            });

                            last.children(":first").on("click", function(){
                                get_data(false);
                                event.stopPropagation();
                            });
                        }
                    }
                }
            });
        }
    }

    function get_chosen_facet(facet) {
        var eles = facet.children().children(".is-active");
        var results = [];
        for (var i = 0; i < eles.length; i++) {
            var last_index = eles[i].text.lastIndexOf("(");
            results.push(eles[i].text.substring(0, last_index));
        }
        return results;
    }

    function get_chonsen_fos(){
        var eles = $("input:checkbox:checked");
        var results = [];
        eles.each(function(){
            console.log($(this).val());
            results.push($(this).val())
        });
        return results;
    }

    function page_init() {

        var page_list = $("#page_list");
        page_list.empty();
        var max_page = parseInt($("#page_num").val());
        for (var i = 1; i < 10; i++) {
            if (i <= max_page) {
                var page = "<li><a class=\"pagination-link\"\n" +
                    "aria-label=\"Goto page" + i + "\">" + i + "</a></li>";
                page_list.append(page);
            }
        }
        page_list.children(":first").children().addClass("is-current");
        page_list.children(":first").children().attr("aria-current", "page");

    }

    function get_data(is_paged) {

        //is_paged 是否根据当前已有检索方式继续翻页，否的话，回到当前所选检索方式的第一页
        var sort = $("#chosen_sort").text();
        var page = $("a.pagination-link.is-current").text();
        var content;
        var url;

        //判断是高级搜索还是普通搜索
        if ($("#search_type").val() === "advanced") {
            content = {
                "title": $("#title").val(),
                "author_name": $("#author_name").val(),
                "author_org": $("#author_org").val(),
                "venue": $("#venue").val(),
                "keywords": $("#keywords").val(),
                "year": $("#year").val(),
                "fos": $("#fos").val(),
                "lang": $("#lang").val(),
                "publisher": $("#publisher").val(),
                "issn": $("#issn").val(),
                "doi": $("#doi").val(),
                "url": $("#url").val(),
                "abstract": $("#abstract").val(),
                "page": page,
                "sort": sort
            };
            url = '/paper/search_advanced';
        } else {
            content = {
                "search_content": $("#kw").val(),
                "page": page,
                "sort": sort
            };
            url = '/paper/search_general'
        }

        content['year_facet'] = get_chosen_facet($("#menu_year")).toString();
        content['author_facet'] = get_chosen_facet($("#menu_author")).toString();
        content['publisher_facet'] = get_chosen_facet($("#menu_publisher")).toString();
        content['fos_facet'] = get_chonsen_fos().toString();

        if (!is_paged) {
            content['page'] = 1;
        }

        $.ajax({
            type: 'post',
            url: url,
            data: content,
            success: function (response) {

                var response_json = JSON.parse(response);
                var paper_list = response_json.data;

                //is_paged 是否根据当前已有检索方式继续翻页，否的话，回到当前所选检索方式的第一页
                if (!is_paged) {
                    $("#page_num").val(response_json.page_num);
                    $("#result_num").text("About " + response_json.result_num + " results");
                    page_init();
                }
                var papers = $("#papers");
                papers.empty();
                for (var i = 0; i < paper_list.length; i++) {
                    var author_name = "";
                    var publisher = "";
                    var year = "";
                    var sub_abstract = "";
                    var doi = "";
                    var n_citation = "";
                    var original = "";
                    if (paper_list[i].hasOwnProperty("authors")) {
                        for (var j = 0; j < paper_list[i].authors.length; j++) {
                            author_name += ("<small><font color=\"green\">" + paper_list[i].authors[j].name + "</font>  , </small>");
                        }
                    }
                    if (paper_list[i].hasOwnProperty("publisher")) {
                        publisher = paper_list[i].publisher;
                    }
                    if (paper_list[i].hasOwnProperty("year")) {
                        year = "("+paper_list[i].year+")";
                    }
                    if (paper_list[i].hasOwnProperty("sub_abstract")) {
                        sub_abstract = paper_list[i].sub_abstract + "...";
                    }
                    if (paper_list[i].hasOwnProperty("doi")) {
                        doi = "&nbsp;&nbsp;&nbsp;" + "-doi:" + paper_list[i].doi;
                    }
                    if (paper_list[i].hasOwnProperty("n_citation")) {
                        n_citation = "<p style=\"color:purple ;font-size:13px\">Cited by " + paper_list[i].n_citation + "</p>";
                    }
                    if (paper_list[i].hasOwnProperty("original")){
                        original =  "<a href="+ paper_list[i].original+ " target=\"_blank\" style=\"color: #0a0a0a\">\n" +
                            "<i class=\"fa fa-book\"></i> ORIGINAL LINK</a>"
                    }


                    var paper = "<article class=\"media\">" +
                        "<div class=\"media-content\">" +
                        "<div class=\"content\">" + "<div class=\"abstract\">" +
                        "<a href=\"/paper/get_paper_by_id?paper_id=" + paper_list[i].id + "\"" +
                        " target=\"_blank\" style=\"color: #0a0a0a\">" +
                        "<strong style=\"font-size: 18px\">" + paper_list[i].title + "</strong></a></div>"+
                        "<div class=\"title\" style=\"font-size: small;margin: 5px\">" +
                        author_name +
                        "</div>" +
                        "<p style=\"font-size: small;margin: 5px\">" + publisher + "," + year
                        + doi +"&nbsp;&nbsp;" +original +"</p>" +
                        "<p class=\"abstract\" style=\"font-size: small;margin: 5px\">" +
                        sub_abstract +
                        "</p>" +
                        n_citation +
                        "</div>" +
                        "</div>" +
                        "</article>";
                    papers.append(paper);

                    $("a.pagination-link").click(function () {
                        var current_page = $("a.pagination-link.is-current");
                        if ($(this).text() !== current_page.text()) {
                            current_page.removeClass("is-current");
                            current_page.removeAttr("aria-current");
                            $(this).addClass("is-current");
                            $(this).attr("aria-current", "page");
                            get_data(true);
                        }
                    });

                    $("a[target=\"_blank\"]").mouseover(function () {
                        $(this).css("border-bottom", "1px purple solid");
                        $(this).css("color", "purple");
                    });

                    $("a").mouseout(function () {
                        $(this).css("color", "black");
                        $(this).css("border-bottom", "");
                    });


                }
            }
        });
    }



