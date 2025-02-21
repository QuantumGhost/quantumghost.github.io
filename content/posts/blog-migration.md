---
category: technology
date: 2020-03-07
slug: blog-migration
status: published
tags: [博客]
title: 博客域名迁移
aliases:
  - /blog-migration.html
---

本博客域名将由
[https://blog.quantumghost.me](https://blog.quantumghost.me) 迁移到
[https://blog.quantumghost.dev](https://blog.quantumghost.dev) 啦。

以前的用户继续访问 [https://blog.quantumghost.me](https://blog.quantumghost.me)
将会被 301 重定向到
[https://blog.quantumghost.dev](https://blog.quantumghost.dev) ，
之前的域名会今年内下线。

为什么要迁移呢？

前两天上 [draw.io](https://draw.io)
画图的时候，看到网站弹出了一个提示，大意是说 「draw.io 将在 2020
年内切换至 diagrams.net」。维护团队专门写了一篇
[博客](https://www.diagrams.net/blog/move-diagrams-net)，说明迁移到
diagrams.net 的原因，归纳起来 大致以下两点：

- `.io` 域名本应是被一些岛屿拥有，但是由于
  「[当代英国帝国主义](https://bit.ly/3cEgEji)」，
  这些岛屿并没有获得这个域名的相关收益。
- 2017 年 `.io` 域名发生了一起安全事故，一个研究员控制了七台 `.io`
  权威域名服务器中的四台。并且域名管理者没有对相关安全问题进行任何沟通

draw.io 的开发者因此认为控制 `.io`
域名的组织不再值得信任，决定迁移到其他域名。

按维基百科的
[介绍](https://zh.wikipedia.org/wiki/%E9%A0%82%E7%B4%9A%E5%9F%9F)，顶级域名大概分为以下几类：

- 基础建设顶级域（`.arpa`）
- 测试顶级域（`.test`）
- 国家及地区顶级域（ccTLD）
- 通用顶级域名（gTLD）

我博客之前的 `.me` 域名，其实也是 [黑山](https://bit.ly/2PUa66m)
的国家顶级域名。

虽然黑山的 ccTLD 并没有爆出管理不善的问题，但是相对于 gTLD
的管理，我个人觉得可能还是要差一些，而且
也会更多地受到现实世界政治变动的干扰（比如捷克斯洛伐克解体，就导致了
[.cs](https://zh.wikipedia.org/wiki/.cs) 这个 ccTLD
被剔除）。综合考虑之下，我决定从 ccTLD 迁移到 gTLD。

这几年根域名大爆炸，gTLD 当然多了很多选择了，不过我个人考虑了一下，觉得
`.dev` 看起来是最好的选择，原因如下：

- `.dev` 的基础设施应该是由 Google 运营的，有很好的安全记录
- 所有 `.dev` 域名都在各大浏览器的 [HSTS
  preload](https://hstspreload.org/) 列表中，只能够使用 HTTPS
  进行连接， 这点对于一个公开网站是非常重要的。
- `.dev` 相对 `.com`，`.net` 等 gTLD
  来说比较新，能够注册到我想要的域名，而且注册费也相对较低。

基于上述考量，我购买了 `quantumghost.dev`
这个域名，并把之前的博客重定向到新的域名上。

我利用 [Zeit](https://zeit.co/) 的 routes 配置了一个
[自动重定向](https://github.com/QuantumGhost/blog-redirect)，
只需要把域名绑定到对应的仓库上
即刻实现重定向，无需人工干预也不用操心部署问题。

FIN.
