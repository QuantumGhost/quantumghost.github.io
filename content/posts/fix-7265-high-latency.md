---
category: technology
date: 2020-02-28
slug: fix-7265-high-latency
status: published
tags: [网络, Linux, 驱动]
title: 解决 Intel 7265 网卡在 Linux 下延迟过高的问题
aliases:
  - /fix-7265-high-latency.html
---

警告：本文是篇流水帐，可能不值得浪费你的宝贵时间。

我有一台 NUC 5 i5，装了 Debian 放在家里作为 Homelab 使用。

前几天把它连到 WiFi 上面，发现从其他笔记本 / 手机 ping
它的延迟很高，达到了一两百毫秒； 但是从它 ping
网关或其他设备却只有几毫秒，是正常的局域网延迟。去网上搜索找到一个
[方案](https://wiki.debian.org/iwlwifi) 是设置 iwlwifi 内核模块参数：

```text
options iwlwifi bt_coex_active=0 swcrypto=1 11n_disable=8
```

但是我配置上了重启发现，问题并没有得到解决。

然后我不死心，从 Intel 网站又找了官方驱动，想要替换掉 Debian
自带的微码。研究了一下， 想找到如何让 Linux 加载我下载的 `.ucode`
文件，但是并没有什么收获。试图卸载 `iwlwifi` 驱动也不行。
于是去网上搜索，发现新版本要执行 `modprobe -r iwlmvm` 才能卸载网卡驱动。

这个 `iwlmvm` 是个什么东西呢？然后我就 `modinfo iwlmvm`
看了一下这是个什么模块，意外地发现了一个参数：

```text
# parm:           power_scheme:power management scheme: 1-active, 2-balanced, 3-low power, default: 2 (int)
```

电源管理？？会不会是这个导致了网卡高延迟呢？

于是试试给内核模块配置加入一行：

```text
options iwlmvm power_scheme=1
```

就好了。

最后来个对比图吧：

![前后效果对比图](/static/images/intel-7262-latency.png)

其实如果搜
`debian 7265 lag`，第一条点进去有个链接就能看到正确的解决方案了，可能是我当时的关键词不对吧
😂。
