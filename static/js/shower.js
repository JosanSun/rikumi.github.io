function pageDidLoad(content) {
    // 设置 Markdown 样式
    marked.setOptions({
        renderer: new marked.Renderer(),
        gfm: true,
        tables: true,
        breaks: false,
        pedantic: false,
        sanitize: false,
        smartLists: false,
        smartypants: false,
        highlight: function (code, lang) {
            if (lang == "") {
                return hljs.highlightAuto(code).value;
            }
            return hljs.highlightAuto(code, [lang]).value;
        }
    });

    // 计算当前页面原始地址
    var url = window.location.href.replace("/show/", "/");
    var info = "[" + url + "](" + url + ")";

    // 将文件开头的大标题(如果有)后面添加页面链接
    content = content.replace(/^(\#\s.*\r?\n)/, "$1" + info + "\n");

    // 输出处理后的 Markdown 文本
    console.log(content);

    // 渲染 Markdown 文本
    content = marked(content);

    // 根据 <h1>~<h3> 以及 <hr> 对 Markdown 分页
    content = "<page>" + content.replace(/(<h[1-3][>\s])/g, "</page><page>$1").replace(/<hr>/g, "</page><page>") + "</page>";

    // 去除空页
    content = content.replace(/<page><\/page>/g, "");

    // 将所有内部链接转换成演示模式
    content = content.replace(/href="\/show\//g, "href=\"/").replace(/href="\//g, "href=\"/show/");

    // 将所有外部链接转换成新窗打开
    content = content.replace(/href="http/g, "target=\"_blank\" href=\"http");

    // 展示渲染结果
    $("#content").html(content);

    // 为内容动态应用 Markdown 样式(在此之前不应用 Markdown 样式)
    $("#content").removeClass("loading");
    $("#content").addClass("markdown-body");

    // 对内容应用分页展示
    $("#content").fullpage({
        scrollingSpeed: 500,
        scrollBar: true,
        scrollOverflow: true,
        dragAndMove: true,
        scrollOverflowOptions: {
            scrollbars: false,
            bounce: true
        },
        sectionSelector: "page"
    });
}