---
category: technology
date: 2019-11-06
slug: wrireguard-on-rpi
status: published
tags: [WireGuard, 网络, VPN]
title: 在树莓派 3B 上安装 WireGuard
aliases:
  - /wrireguard-on-rpi.html
---

警告：本文是篇流水帐，可能不值得浪费你的宝贵时间。

最近国内的 ZeroTier
网络十分不稳定，[之前架的](/use-zerotier-for-remote-access.html)
桥接几乎不可用。为了方便从外部连接家中服务， 决定再搭一个 VPN，然后用
[Sakura Frp](https://www.natfrp.com/) 把 VPN 和 SSH 端口转发出来，
保证总是能连上家庭网络。

考察了一下 macOS 的支持和维护难易度，最后决定使用 WireGuard 作为
VPN。（其他 VPN 很多需要 [tuntap
内核扩展](http://tuntaposx.sourceforge.net/) ，或者是 Debian
官方源里没有二进制包）

先看 WireGuard [官方安装指南](https://www.wireguard.com/install/)，添加
unstable 源然后再从源安装，看起来很简单的样子。

添加进去之后，执行 `sudo apt update` 提示：

```
W: GPG error: https://mirrors.ustc.edu.cn/debian unstable InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 04EE7237B7D453EC NO_PUBKEY 648ACFD622F3D138
```

诶，这是咋回事啊？？

安装 debian-keyring 和 debian-ports-archive-keyring
也解决不了这个问题，搜了下这两个 key
也没有任何官方来源，我可不敢随便添加 apt key。官方方案就此作罢。

这也没事，官方在 Linux 下面除了提供内核态的 WireGuard 实现，也提供了一个
Golang 的
[用户态实现](https://github.com/WireGuard/wireguard-go/)，我们用这个就好了。

三下五除二把用户态方案编译好丢到 RPi
上跑起来，发现没有任何可以指定配置的地方 @_@。在 WireGuard 官方
网站逛了一圈，发现了
[跨平台配置协议](https://www.wireguard.com/xplatform/)。原来用户态实现创建了一个
Unix domain socket，通过这个协议来对 WireGuard 进行配置。

用 nc 连到 `/var/run/wireguard/wg0.sock`
测试了一下，确实是使用的跨平台协议，那么下一步就是如何使用配置协议进行配置。
官方提供的 wg-quick 跟 WireGuard 的内核扩展一样在 unstable
源里面，所以我肯定是用不了了；写 shell 去配置当然也行， 但是可维护性就
😂 了。在 Github 上看了一下，找到一个 Golang 实现的
[配置模块](https://github.com/WireGuard/wgctrl-go/)，实现了跨平台配置协议，但是
API 比较底层， 不能达到我想要的
指定配置文件就能完成配置的效果。（而且我还想跟 WireGuard
官方实现使用同样的配置格式）

然后就是找官方的配置文件是什么格式，最后在 wg 的
[文档](https://git.zx2c4.com/WireGuard/about/src/tools/man/wg.8#CONFIGURATION%20FILE%20FORMAT)
里找到了。这个格式看起来跟 Ini
有点像但是又不完全一样，试了好几个库都解析不了重复的 `Peer`
段，于是只好自己手写一个按行解析的 Parser = =。

Parser 写完，再糊上周边命令，然后提交给上游 wgctrl-go，上游说：

| Attempting to emulate what wg-quick is doing is outside the scope of
  this package.

行吧，那我留着自己用。从 wgctrl-go 里面拆分到一个叫
[wg-quick-go](https://github.com/QuantumGhost/wg-quick-go) 的 repo
然后打包上传 Github。

WireGuard 配置搞定了，但是还有一些其他的周边工作需要做。原版 WireGuard
配置文件似乎支持 `PostUp`, `PostDown` 这种 hook，可以在 WireGuard
启动之后执行自定义脚本；而配置协议里面是没有这些内容的。这部分功能通过
systemd 的 `ExecStartPost` 和 `ExecStopPost` 模拟来解决了。

另外一个问题是，WireGuard 是 Layer 3 的 VPN，不能直接与 RPi
的其他网卡进行桥接，只能使用 SNAT 的方式来解决内网访问问题， 而 SNAT
需要使用 nftables 添加相关规则，这里折腾了半天都不行，最后把错误消息丢到
Google 上搜了一下，发现我的内核不够新， 根本就没有 `nf_tables`
这个内核模块。但是 `apt update` 又提示我没有可更新的软件包。 尝试使用
rpi-update 也因为墙的原因不成功。然后去搜了一下，发现 RPi
社区的源（包含内核）在 `raspi.list` 这个文件里，而这个文件被我干掉了
😂😂。于是把 USTC 的镜像源加到列表里面，更新重启，终于可以正常配置了。

下面是我的 nftables 配置，仅供参考：

```
table inet filter {

    chain input {
        type filter hook input priority 0;
    }

    chain forward {
        type filter hook forward priority 0;
        iifname "wg0" counter accept;
    }

    chain output {
        type filter hook output priority 0;
    }
}

table ip nat {
    chain prerouting {
        type nat hook prerouting priority 0;
    }

    chain postrouting {
        type nat hook postrouting priority 100;
        oifname "eth0" masquerade;
        oifname "wlan0" masquerade;
    }
}
```

如果一开始就直接用 OpenVPN，可能就没这么多幺蛾子了 2333。

FIN.
