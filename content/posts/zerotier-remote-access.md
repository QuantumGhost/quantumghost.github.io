---
category: technology
date: 2019-07-18
slug: use-zerotier-for-remote-access
status: published
tags: [ZeroTier, 网络]
title: 用 ZeroTier 实现内网穿透
toc: true
aliases:
  - /use-zerotier-for-remote-access.html
---

如果你在家中有一台 HomeLab
的话，你可能也会像我一样想要随时随地能够访问到它和它上面的各种服务。
ZeroTier 就是为此而生的。

[ZeroTier](https://www.zerotier.com/) 是一个 L2 VPN 软件，但是与传统的
VPN 软件不同 的是，它并没有采用 [客户端 -
服务器](https://en.wikipedia.org/wiki/Client%E2%80%93server_model)
的模型，而是采用了 P2P 的模型，节点之间会尽可能地通过 NAT 打洞
来建立直接连接，只有无法建立直接连接时才采用服务器中转。这立即就解决了在没有公网
IP 的情况下进行远程 连接的困难问题。同时，ZeroTier 还有强大的
[网络规则引擎](https://www.zerotier.com/manual/#3)，可以轻松地对 VPN
上的流量进行控制。

使用 ZeroTier 进行内网穿透有两种模式，一种是在家庭局域网中某台电脑上安装
ZeroTier，并将其作为虚拟 网络的出口路由，再配合 ZeroTier 的路由表和
iptables，将流量转发到局域网内其他电脑；另一种是直接将 ZeroTier
网段和局域网网段进行 L2 桥接。

## NAT 方式

大体上的原理就是把局域网内一台设备作为路由，对 ZeroTier 网段的流量进行
[地址转换](http://bit.ly/2LHSA2l)。实现方式不详述，有兴趣的请参考
[Gist](http://bit.ly/34F9Fmg)。（仅适用于 Linux）

## 桥接方式

首先需要规划网段。一般家庭用户的默认网段为 `192.168.xx.0/24`，如果要结合
ZeroTier，需要保证 路由器的 IP 段和 ZeroTier 自动分配的 IP
段不冲突，同时两边又处于同一子网。比较简单的办法是把原来 的 LAN 扩大到
`/22` 或者 `/23`。

例如，原来的子网是 `192.168.0.0/24`，那么扩大的时候可以扩大到
`192.168.0.0/22`，这样局域网和 ZeroTier 可以分别使用 `192.168.0.100` -
`192.168.0.200` 和 `192.168.1.100` - `192.168.1.200` 这两个 IP
段进行自动 IP 分配，同时也能保持互联。

接下来就是需要在局域网内找一台设备安装 ZeroTier
并加入网络。如果可能的话，路由器是最好的选择， 可以使用
[OpenWrt](https://openwrt.org) 或者
[Entware](https://github.com/Entware/Entware) 在路由器上安装
ZeroTier。如果路由器不能安装 ZeroTier，选择一台在线率高的设备也行。

安装完成之后，进入 ZeroTier
管理界面，找到要进行桥接的设备，点击左侧的设置图标，勾选
`Allow Ethernet Bridging`； 同时勾选上方设置中的
`Enable Broadcast`。（这一步非常重要，IPv4 依赖于 ARP
来发现其他设备，如果没有开启广播的话， 家庭网络内的设备就发现不了
ZeroTier 内的设备了）

如图：

![allow bridging in ZeroTier control panel](/static/images/zerotier-allow-bridging.png)

![enable broadcast for bridged device](/static/images/zerotier-enable-broadcast.png)

然后，将 ZeroTier
的网卡与该设备的网卡进行桥接。我是使用路由器进行桥接，路由器默认创建了
`br0` 作为所有 LAN 端口的桥接网卡，所以我只需要
`brctl addif br0 $ZT_INTERFACE` 即可。如果不是使用
路由器作为桥接设备的话，那么需要先手动使用 `brctl addbr`
创建桥接网卡，再使用 `brctl addif` 把物理网卡和 ZeroTier
网卡添加到桥接中。Linux 下的操作可以参考 [Linux
文档](https://wiki.linuxfoundation.org/networking/bridge) 和 [Arch
Wiki](https://wiki.archlinux.org/index.php/Network_bridge)，其他操作系统请参考对应
文档。

最后，如果你使用了 DHCP，你还需要在 ZeroTier
的规则引擎中屏蔽掉家庭网络路由的 DHCP 请求和响应，可以参考下面的规则

```
drop ethertype ipv4
    and ipprotocol udp
    and sport 68
    and dport 67
;

drop ethertype ipv4
    and ipprotocol udp
    and sport 67
    and dport 68
;
```

## 后记

如果你有公网 IP，而且不需要内网互联的话，可以考虑
[DDNS](https://en.wikipedia.org/wiki/Dynamic_DNS)，或者用 ssh 来做
[端口转发](https://www.ssh.com/ssh/tunneling/example)。如果没有公网 IP，
也可以考虑使用诸如 [Frp](https://github.com/fatedier/frp)
之类的工具进行转发。当然，
这需要一台稳定的服务器并进行相关配置，而且延迟也会有所上升。

另外，如果 ZeroTier 的两端都没有公网 IP 的话，NAT
打洞的成功率会低很多，通过官方转发的延迟非常高，
这个时候可以考虑自己建立 Moon 服务器的方式来进行转发。

FIN.
