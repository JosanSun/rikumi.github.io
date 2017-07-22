## RIKUheyaへようこそ！

欢迎光临 RIKUheya，这里是我的小站。
<img width="390" height="456" src="http://static.myseu.cn/2017-07-07-sizuru.png" class="moe">

## 本站正式接入 Disqus 评论框

经过一上午的不务正业，终于接入了 Disqus，不指望有多少人评论，只是觉得你来我往的感觉更好些，也更像一个正经的博客。

不仅文章页面，首页和404页都可以进行评论，只希望让小站热乎起来😝

## 开源 iOS 展开跳转+三向滑动返回动效框架 AnyPullBack 发布

今天发布了人生第一个 Pod 项目，一个开源的 iOS 版三向滑动返回动效插件，跳转和返回手势的效果类似36氪和轻芒杂志，使用时只需引入 `AnyPullBackNavigationController` 即可直接使用。项目已发布到 Cocoapods，只需在 Podfile 引入 `pod 'AnyPullBack'` 即可使用。

[项目地址](https://github.com/vhyme/AnyPullBack)

## 博客首页播放器换成纯音BGM歌单

如题，最近把博客首页播放器换成了BGM歌单，均为纯音乐，不太喜欢女声的可以试试这些。目前的音乐来源是罚抄神作「Rewrite」，以及「凪のあすから」和「あの夏で待ってる」原声带。

由于网易云音乐接口的问题，偶尔可能会有 Error happens，不要惊慌，换个网络或者过一阵子应该就好了。

查看歌单：[RIKUheya](http://music.163.com/playlist/582976667/18769885?userid=18769885)｜[我喜欢的音乐](http://music.163.com/playlist/16249817/18769885?userid=18769885)

## 考完啦，开始填坑

> 消灭了 概率论 🔥233

> 消灭了 数模 🔥233

> 消灭了 信号 🔥233

> 消灭了 计组 🔥233

今天开始漫长的暑假填坑，首先把本站改成了纯前端项目，利用 [Docute](https://docutejs.org) 实现 GitHub 文章的前端获取和前端路由，现在 RikuHeya 和 HeyaData 合并成了一个项目，而且**所有的跳转都不会重载页面了（可以放心听我的歌单了）**

## P2P弦网络及其Python实现 - ChordNetwork

高级数据结构研讨课的课件和项目，欢迎交流学习和使用。

[项目主页](https://github.com/vhyme/ChordNetwork)｜[查看文档](/技术文档/ChordNetwork)

## Git快速上手教程

为了方便初学者迅速掌握 Git 基础知识，编写了这份简陋的 Git 快速上手教程，希望能为初学者学习 Git 有帮助。

[查看文档](/技术文档/Git快速上手)

## 小猴偷米广告合作管理规范

最近众多社团和学生组织开始利用小猴偷米轮播图作为宣传途径，因此润色了一下规范文档，张贴在此，供合作者参考。

[查看文档](/技术文档/小猴偷米广告投放须知)

## 新开坑：微信小程序跳转层数检测工具

微信小程序提供了 `navigateTo` 和 `redirectTo` 两种方式可以进入新的页面，前者会打开新的界面（跳转），后者则会在原界面直接展示（重定向），而微信小程序限制了 `navigateTo` 跳转栈的层数不能超过5层。这就要求小程序中不能有过高的跳转栈，也不能有循环跳转。最近达人荟live新版小程序发布在即，由于界面太多，无法人工逐一检查多层跳转和循环跳转，所以花了一中午+一下午的时间写了这个Python脚本，用于检测微信小程序的多层跳转和循环跳转问题。

该脚本先利用文件系统操作，列出当前小程序目录下所有的 `navigateTo` 跳转和 `redirectTo` 重定向；然后采用带权有向图结构，按照跳转权为1、重定向权为0，作出相应的出边表，然后从每个入度为0的节点开始，对这个图结构采用深度优先遍历，查找长度超过5的路径以及长度不为0的环。该脚本采用Python3编写，理论上兼容Python2，另外具有调试参数 `-d` 可以完整展示整个遍历过程。

顺便感谢一些学长让我想起了深度优先遍历是啥😂

[项目主页](https://github.com/vhyme/WXANavigationTester)

## 微信小程序教学参考 & iOS教学参考

最近达人荟所属组织：创梦空间工作室最近准备招新，招收一些有相关兴趣的同学提供培养和实习机会，我也应邀担任微信小程序和iOS方向的负责人，根据要求写了一套微信小程序和iOS的简要参考文档，供学习者查阅。

[微信小程序教学参考](/技术文档/微信小程序教学参考)｜[iOS教学参考](/技术文档/iOS教学参考)

## 日文歌词去除注音的正则表达式

在用我的APCloud播放器的时候，发现某些歌词有大量注音，歌词显示的空间不够，导致歌词显示不完整，于是打算用正则把它们统一去掉，经过多次踩坑和测试，下面这种方案最稳妥：

```python
## 去掉日文歌词的注音
ret = re.sub(u'[(（][\u2E80-\u4DFF]+[)）]', '', src)
```

## 网易云在线歌单播放器项目APCloud基本完工

昨天开坑了这个项目，目的是把[163music-APlayer-you-get-docker](https://github.com/YUX-IO/163music-APlayer-you-get-docker)项目所用的API升级成最新的网易云音乐API，以解决大多数歌曲无法播放问题。项目大部分采用了开源终端音乐播放器[musicbox](https://github.com/darknessomi/musicbox)所使用的API，mp3直链获取采用了[Meting](https://github.com/metowolf/Meting)项目提供的API和加密算法。由于musicbox核心代码均采用Python3编写，索性也把本博客站升级为Python3。在此特别感谢[163music-APlayer-you-get-docker](https://github.com/YUX-IO/163music-APlayer-you-get-docker)项目提供灵感，感谢[APlayer](https://github.com/DIYgod/APlayer)、[musicbox](https://github.com/darknessomi/musicbox)、[Meting](https://github.com/metowolf/Meting)项目提供轮子。

该项目完成后，作为一个轻量级竖版页面，可以直接作为iframe引用到博客中，通过url自定义要播放的歌单。你可以随意使用该站点，但如果对服务器造成流量冲击，该项目随时会下线，所以推荐自行下载代码，部署到自己的服务器上。

[项目GitHub地址](https://github.com/vhyme/APCloud)丨[项目部署地址（含使用说明）](https://myseu.cn/apcloud/)丨[演示地址](https://myseu.cn/apcloud/16249817)

## [计软学生会] 我的16-17-2工作总结暨宣传部参考指南（秋季版）

本指南按照时间顺序，以2016年秋季学期为例，参考上一届九系学生会宣传部窦颢工作总结，详细列举计软学生会宣传部秋季学期需要做的事，并从我个人的角度给出一系列总结和建议，供后人探讨和借鉴。

[阅读全文](/宣传部/工作总结秋季版)

## 日系字体「新ゴ」修改英数和符号，iOS/macOS/Win10全套替换

这套字体原作来自宁静之雨，自己做了一些修改，包含 iOS9/10 和 macOS 通用的 PingFang.ttc，macOS 版网易云使用的冬青黑体，以及 Win10 使用的微软雅黑/雅黑UI字体替换。
- iOS替换方法：越狱后用 Filza 或类似的文件管理器复制到 /System/Library/Fonts/LanguageSupport 覆盖；
- macOS替换方法：打开并安装苹方和冬青黑体，然后打开字体册解决重复字体，选择新安装的字体即可；
- Win10替换方法：用 WinPE 或其他系统环境将三个字体文件复制到 /Windows/Fonts 覆盖。

[百度云下载](https://pan.baidu.com/share/link?shareid=826865158&uk=3408869611)丨[原作链接](http://bbs.themex.net/showthread.php?t=16904284)