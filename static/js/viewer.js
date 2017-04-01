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

    // 计算当前页面对应的演示地址
    var url = decodeURI(window.location.href);

    // 排除404页面和pull页面
    //  ^  ( (\/\/)  |   [^/]  )   +    \/  (404  (\.md)   ?     |    pull  \/   ?   )   $
    // 开头,( "//"  或者 不是"/" )出现多次,"/",(("404",".md"有或没有)或者("pull","/"有或没有)),结束
    if (!url.match(/^((\/\/)|[^/])+\/(404(\.md)?|pull\/?)$/)) {

        // 匹配域名开头到第一个单斜杠位置，并替换成/show/
        //  ^        .*         ?    [^\/]  \/ ([^\/]    |   $ )
        // 开头,零或多个任意字符:非贪心,不是"/","/",(不是"/" 或者 结束)
        var regex = /^.*?[^\/]\/([^\/]|$)/;
        if (url.match(regex)) {
            url = url.replace(regex, "/show/$1");
        } else {
            url += "/show/"
        }
        var info = "[演示当前页面](" + url + ")";

        // 将 Markdown 最开头的大标题(如果有)后面添加页面演示链接
        //  ^   (\#    \s       .*        \r   ?    \n)
        // 开头,("#",空白字符,零或多个任意字符,CR有或没有,LF)
        content = content.replace(/^(\#\s.*\r?\n)/, "$1" + info + "\n");
    }

    // 输出处理后的 Markdown 文本
    console.log(content);

    // 渲染 Markdown 文本
    content = marked(content);

    // 将所有外部链接转换成新窗打开
    content = content.replace(/href="http/g, "target=\"_blank\" href=\"http");

    // 展示渲染结果
    $("#content").html(content);

    // 为内容动态应用 Markdown 样式(在此之前不应用 Markdown 样式)
    $("#content").removeClass("loading");
    $("#content").addClass("markdown-body");

    // 修复 del 元素无法在 iOS 端触发 :hover 的问题
    // http://stackoverflow.com/questions/18047353/fix-css-hover-on-iphone-ipad-ipod
    $("del").attr("onclick", "");
}

var menu = false;

function toggleMenu() {
    menu = !menu;
    if (menu) {
        $("body").addClass("menu-on");
    } else {
        $("body").removeClass("menu-on");
    }
}