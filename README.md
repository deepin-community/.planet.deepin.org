# [🌎 Planet deepin](#)

[English](./README.md) | [简体中文](./README.zh_CN.md)

Planet deepin is a web feed aggregator that collects blog posts from people who contribute to the deepin community.

If you are a deepin contributor you can have your blog on Planet deepin. Blog content should be mostly
deepin themed and not liable to offend. If you have a general blog you may want to set up a tag and
subscribe the feed for that tag only to Planet deepin.

## Adding your feed

If you are from an existing SIG in deepin community and prefer to add the feed of your SIG, then you can add your
SIG's feed by updating your SIG's metadata.yml config file. Head to [deepin-community/SIG](sig repo) to learn more.

[sig repo]: https://github.com/deepin-community/SIG

If you are a solo contributor and want to get your feed added, we prefer Pull Requests via GitHub:

1. Fork this repository
2. Edit `planet.ini` and add:

```toml
[id]       # replace id with your feed's unique identifier (a-z0-9-_) (e.g. dde-port)
feed_url = # url to your rss/atom feed                                (e.g. https://deepin-community.github.io/sig-dde-porting/atom.xml)
title    = # (optional) title of your feed                            (e.g. DDE Porting SIG)
           #   will be used as the `author` field of a post
           #   so better set this to your name for people to identify you
           #   if not set, the title field in the feed data will be used
site_url = # (optional) url to your website                           (e.g. https://deepin-community.github.io/sig-dde-porting)
           #   default to the link field in the feed data
           #   or if that's not set, the host part of feed_url
avatar   = # (optional) filename or url of your avatar                (e.g. dde-porting.svg)
flairs   = # (optional) space-separated list of flairs of the author, currently supports:
           #   irc:irc_nickname          (e.g. irc:myircnickname)
           #   matrix:@username:url      (e.g. matrix:@username:deepin.org)
           #   telegram:username         (e.g. telegram:deepin-community)
           #   gsoc
```

If you do not have a GitHub account, you can drop a mail to [deepin-devel mailing list](mailing list) or reach us out
in our [Matrix chatroom](deepin matrix) with the above information provided, so we can help you get it added.

[mailing list]: https://www.freelists.org/list/deepin-devel
[deepin matrix]: https://matrix.to/#/#deepin-community:deepin.org

## Planet deepin Guidelines

Planet deepin is one of the public faces of the deepin project and is read by millions of users and potential
contributors. The content aggregated at Planet deepin is the opinions of its authors, but the sum of that
content gives an impression of the project. Please keep in mind the following guidelines for your blog
content. We reserve the right to remove an inappropriate blog from the Planet. If that happens multiple
times, we'll consider what needs to happen to get your blog aggregated again.

### Blogs should be deepin themed

The majority of content in your blog should be about deepin and your work on deepin. Blog posts about personal
subjects are also encouraged since Planet deepin is a chance to learn more about the developers behind deepin.
However, blog feeds should not be entirely personal, if in doubt set up a tag for Planet deepin and subscribe
the feed from that tag, so you can control what gets posted.

### Posts should be constructive

Posts can be positive and promote deepin, they can be constructive and lay out issues which need to be
addressed, but blog feeds should not contain useless, destructive and negative material. Constructive
criticism is welcome and the occasional rant is understandable, but a feed where every post is critical
and negative is unsuitable. This helps to keep deepin overall a happy project.

### You must be a deepin contributor

Only have your blog on Planet deepin if you actively contribute to deepin, for example through code, user
support, documentation etc.

### It must be a personal blog, or in a blog class

Planet deepin is a collection of blogs from deepin contributors.

## Development

See HACKING.zh.md

## About and Credit

There are a lot of FOSS community are running their own feed aggregator, like [Planet Qt](planet qt), 
[Planet KDE](planet kde), [NixOS Planet](nixos planet), [Planet Debian](planet debian) and so on. Such platform
could help gathering information that related to the community and made them available to more people. Planet deepin
is also intended to be used in the same usage.

[planet qt]: https://planet.qt.io/
[planet kde]: https://planet.kde.org/
[nixos planet]: https://planet.nixos.org/
[planet debian]: https://planet.debian.org/

This repo is based on [HUGO](hugo), and is modified [from the source](planet kde source) of [Planet KDE](planet kde).
Go check them out if you are interested. Please refer to the header of each source file to see about license information.

[hugo]: https://gohugo.io/
[planet kde source]: https://invent.kde.org/websites/planet-kde-org/