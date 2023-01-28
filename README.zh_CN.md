# [🌎 deepin 星球](#)

[English](./README.md) | [简体中文](./README.zh_CN.md)

deepin 星球是一个订阅源聚合站点，其汇集了参与 deepin 社区贡献的贡献者们的、与 deepin 相关的博客文章。

如果你是一个参与 deepin 相关社区贡献的贡献者，那么欢迎你把自己的博客加入到 deepin 星球之中。博客主题应当主要与 deepin 相关
且整体客观且具有建设性。如果你有一个通用性质的博客的话，你也可以考虑为 deepin 相关的主题设置一个标签，并将此标签对应的订阅源
添加到 deepin 星球。

## 添加你的订阅源

如果你是现有 deepin 社区中的兴趣小组（SIG）成员且希望为你的小组添加订阅，那么你可以直接更新对应小组的 metadata.yml 配置文件
来达到此目的。请前往 [deepin-community/SIG](sig repo) 仓库来了解更多。

[sig repo]: https://github.com/deepin-community/SIG

如果你是个人贡献者且希望将你自己的订阅源加进来，我们建议你在 GitHub 上发起 Pull Request 的形式进行添加：

1. Fork（复刻）此仓库
2. 编辑 `planet.ini` 并添加:

```toml
[id]       # 将 id 替换为你的订阅源的标识符 (a-z0-9-_)                    (例如 dde-port)
feed_url = # 你的订阅源的 RSS 或 ATOM 链接                               (例如 https://deepin-community.github.io/sig-dde-porting/atom.xml)
title    = # (可选) 你的订阅源的标题                                     (例如 DDE Porting SIG)
           #   将会成为对应博客文章的 `author`（作者）字段的值
           #   所以最好设为你的名字或昵称，以方便大家可以认出你
           #   如果不设置，则将使用订阅源中的 title 字段的信息。
site_url = # (可选) 你的站点的 url 网址                                  (例如 https://deepin-community.github.io/sig-dde-porting)
           #   默认为订阅源中的 link 字段的信息，或 feed_url 的主机名部分
avatar   = # (可选) 你的头像/logo 的文件名或 url                          (例如 dde-porting.svg)
flairs   = # (可选) 你的一些附属信息，为使用空格分割的列表。目前支持这些信息：
           #   irc:irc_nickname          (例如 irc:myircnickname)
           #   matrix:@username:url      (例如 matrix:@username:deepin.org)
           #   telegram:username         (例如 telegram:deepin-community)
           #   gsoc
```

如果你没有 GitHub 帐号，那么你也可以考虑通过 [deepin-devel 邮件列表](mailing list) 或是 deepin 的 [Matrix 聊天室](deepin matrix)
与我们取得联系并提供上述的信息，以便我们帮助你进行添加。

[mailing list]: https://www.freelists.org/list/deepin-devel
[deepin matrix]: https://matrix.to/#/#deepin-community:deepin.org

## deepin 星球准则

deepin 星球是 deepin 项目的公众“面孔”之一，且会被众多用户与潜在贡献者订阅与浏览。尽管 deepin 星球所聚合的内容均仅代表其对应的
原作者自身的观点，但 deepin 星球作为一个整体而言将会影响到公众对 deepin 社区的印象。所以请留意你博客的内容。我们保留从 deepin
星球中移除您的博客订阅源的权力，如果你的博客多次违反准则被移除，我们则可能考虑不再接受你博客的订阅源。

### 博文的主题应当与 deepin 相关

你所添加的博客订阅源中的博文的主题应当与 deepin 具有相关性。尽管我们也允许纯个人主题的博文出现（deepin 星球也提供了一个让人们了
解 deepin 社区的贡献者本身的机会），但订阅源中的博文应当至少有一定比例的文章与 deepin 社区相关而不能是完全的个人日志性质的博客。
如果你不太确定的话，可以考虑为你的个人博客设置一些标签，然后将 deepin 标签对应的订阅源加入到 deepin 星球，这样你可以更好的控制
你的哪些博客会出现在 deepin 星球之中。

### 博文应当具有建设性

博文可以是关于 deepin 的积极描述，也可以列出 deepin 现存问题之类的建设性文章，但不能是完全消极且毫无建设性的文章。我们欢迎
有建设性的批判文章，即便偶尔有抱怨性质的文章也可以接受，但完全无建设性的负面文章或所有文章均为负面内容的博客将不会被允许加入。
这有助于保持 deepin 项目与 deepin 社区的健康氛围。

### 你必须是一个 deepin 贡献者

你必须是一名 deepin 贡献者才能将你的订阅源加入 deepin 星球。当然，贡献的类型可以不限于代码、用户支持、文档、设计等任何方面。

### 必须是博客类的订阅源

deepin 星球是 deepin 贡献者的博客聚合平台。

## 开发

参见 HACKING.zh.md

## 关于

很多开源自由软件社区都有自己的订阅源聚合平台，例如 [Planet Qt](planet qt)、[Planet KDE](planet kde)、
[NixOS Planet](nixos planet)、[Planet Debian](planet debian) 等。这些平台可以汇集对应开源社区的各类相关信息并将其呈现给
更多的社区贡献者和用户。deepin 星球也是与此相同意图的平台。

[planet qt]: https://planet.qt.io/
[planet kde]: https://planet.kde.org/
[nixos planet]: https://planet.nixos.org/
[planet debian]: https://planet.debian.org/

此 repo 基于 [HUGO](hugo)，是基于 [Planet KDE](planet kde) 的[源码](planet kde source)的修改。如果你感兴趣的话，也不妨
看看对应的项目源码。对于源码的许可证信息，请参阅仓库中的各个源文件的文件头。

[hugo]: https://gohugo.io/
[planet kde source]: https://invent.kde.org/websites/planet-kde-org/