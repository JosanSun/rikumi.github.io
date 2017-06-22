# 关于 Heya 博客系统

## 简介
Heya 是基于 Python Flask 的极简 Markdown 博客系统。它没有聚合和分类页面，每个文章仅对应一个 .md 文件，支持文件夹分类。通过后端路由转发，将对应的 .md 文件地址发送到前端，前端负责从 GitHub 获取对应的文件进行渲染和展示。本系统一经部署无需手动维护，更新文章只需要本地修改并`push`到 Github 即可。

## 踩坑小记
2016 年下半年开的坑，本来是打算做一个（而且几乎已经做成了一个）在线协作式 Markdown 编辑器，只有文章编辑界面，没有文章渲染展示界面，而且由于没有用户系统，它曾是人人可编辑的。当时唯一值得炫耀的是，通过后端频繁调用 git 命令行，利用 git 的分支特性，实现了多人同时编辑，自动合并更改或提示冲突的功能。整个界面只有编辑器和一个保存按钮。

后来看了很多前端大神自己搭的博客，有的用 Hexo，有的用 MWeb，基本都是以简洁、静态等特性为出发点，所以我把之前开的坑重新挖了一遍，改成了一个伪静态的、易于维护的 Markdown 个人博客，取名为`Heya`，不是河鸭，是へや（部屋，房间）。

## 优点和特性
程序员不喜欢重复造轮子，但有这么一个轮子，程序员从不用别人的：那就是博客。这个轮子就是程序员（尤其前端程序员）的脸，造的好不好，体现出一个程序员多方面的综合素质。每次造完这个轮子，程序员都要把优点特性、用到的框架什么的在博客上展示一番，目的不是为了让别人用你的轮子（因为他们也想自己造一个），而是为了学习和交流。

那么本 Heya 轮子的特性也写在这里，供各路程序员学习交流：
0. 服务器和数据分离，数据（包括文章和配置）在`HeyaData`repo 上，服务端一次部署无需维护；
1. 后端自动从 git 配置项获取 Github 用户名，监视该用户的`HeyaData`repo；
2. 更新博客只需本地修改 .md 文件并`push`到 Github 即可；
3. 支持文件夹分类，数据 repo 里面怎么放，博客上就怎么访问；
4. json 配置文件，可自定义首页名、博客名、昵称头像介绍词、footer 文字、侧栏导航、网易云歌单、主题色；
5. 支持 iOS 作为全屏 Webapp 添加到桌面，能根据头像自动生成 Favicon 和 Webapp 图标；
6. 支持自定义 404 页面[`404.md`](/404.md)；
7. Markdown 使用[`marked.js`](https://github.com/chjj/marked)渲染，使用
   [`highlight.js`](https://highlightjs.org/) 执行语法高亮；
8. css 响应式布局（移动版用了覆盖式 nav 和 footer，效果比较神奇）；
9. 自带`pull`功能，访问 [/pull](/pull) 可自动 pull 后端代码并展示输出结果；
10. 加了个log，打开 F12 控制台可以看到 markdown 原文本；
11. 写到这忽然发现`marked.js`的列表序号居然强制从1开始（死

## 缺陷和不足
0. 没有自动生成的聚合页面和分类页面，索引全靠手写；
1. 侧栏暂时没地方放社交链接，以及侧栏导航暂不支持站外链接。

## 示例数据展示
### 配置文件 `config.json`
```javascript
{
  	"title": "RIKUheya",
  	"nickname": "Riku",
  	"intro": "一个UI 半个码农",
  	"avatar": "https://avatars1.githubusercontent.com/u/5051300",
  	"index": "最新动态",
  	"sidebar": ["最新动态", "关于我"],
  	"footer": "Proudly designed & developed by Riku",
  	"playlist": "16249817",
  	"themeColor": "#ed6988",

    // 此处省略 Base64 数据（此处假设JSON有注释）
  	"favicon": "data:image/png;base64,iVBORw0KG..."
}
```
### 404页面 `404.md`
```markdown
# 404
找不到你要的文章。

[返回首页](/首页)
```

## 项目地址
[后端代码](https://github.com/Vhyme/RIKUheya)｜[博客数据](https://github.com/Vhyme/HeyaData)
