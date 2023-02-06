此 repo 基于 [HUGO][hugo]，是基于 [Planet KDE][planet kde] 的[源码][planet kde source]的修改。尽管我们进行了一些调整以使其更适合
我们的应用场景，但大体的工作方式没有太大差异。如果你发现了一些项目中的问题，那么也许它们的原始仓库中也存在，这时可以考虑将这些贡献回馈到原始
仓库之中。

[hugo]: https://gohugo.io/
[planet kde]: https://planet.kde.org/
[planet kde source]: https://invent.kde.org/websites/planet-kde-org/

## 与原始版本的差异

我们做了如下修改：

1. 不依赖 KDE 的 [aether-sass](https://invent.kde.org/websites/aether-sass) HUGO 主题
   - 实际此站点并未用到太多此主题的功能
   - 使用此主题反而会使简单场景的开发步骤变麻烦，并且我们显然并不需要遵循 KDE 的 HIG
2. 无论对于哪种语言，均会展示所有文章
   - 初期过程中，中文文章的比率会很大，其他语言很长时间内大概都会处于没有文章或只有个别文章的程度
   - 目前也会忽略语言设置（后续可能还会调整）
3. 会读取 planet.ini 以及 sig.ini，其中 sig.ini 是通过 generate_sig_config.py 生成的
4. 一些其它调整
   - 不再使用 hackergotchi 这种称呼（老老实实叫 avatar）
   - 使用 GitHub Action 计划任务来获取博文内容，并使用 GitHub Pages 托管生成的内容

## 项目依赖

若要基于此仓库进行开发（例如希望进行改进或修正错误），你需要自备下述依赖：

- git（用于拉取 SIG 仓库，生成 `sig.ini`）
- hugo extended (我们需要 SCSS 支持)
- python3
  - feedparser
  - sh
  - pyyaml

此外，项目以直接附带的形式（故无需自备）使用了下述依赖：

- bootstrap 5.x (scss + js)
- bootstrap-icons 1.10.x

故在对项目进行修改的过程中，即可直接利用其对应的特性。

## 使用方式

操作步骤大致为：

1. 运行 `generate_sig_config.py` 以供生成 `sig.ini` （会与 `planet.ini` 位于同一路径下）
2. 运行 `custom_generation.py` 以根据 `planet.ini` 与 `sig.ini` 爬取文章
3. 运行 `hugo server` 启动本地 HTTP 服务以便预览效果（若有需要，也可以 `hugo -D` 生成静态站点）

对应的 GitHub 工作流 `update-feed.yml` 即直接对应到了上述流程，工作流可手动触发，也会每天进行一次计划任务触发。

## 其他说明

项目中的部分内容以 HUGO 生成时通过环境变量进行指定，类如通过 `HUGOxPARAMSxGITREPO` 传递了 `site.Params.GitRepo` 信息避免硬编码。
这类变量即便不提供一般也不会影响站点效果，若需参考所使用到的环境变量信息，请参阅 `update-feed.yml`。

项目附带的 HUGO 主题本身实际只提供了一个几乎最简化的主题，实际页面结构基本位于项目根目录下的 `layouts` 下。

项目主题附带的 bootstrap 有对变量进行部分调整，若需升级，则请留意 `_variables.scss` 中的配置。

此主题 *或许* 后续会服务于其他 deepin 静态站点的搭建，以便各个站点具有统一的样式风格（近似 KDE 的 aether-sass 的作用），但现在显然只是
个基本的骨架主题，基本没有什么功能。
