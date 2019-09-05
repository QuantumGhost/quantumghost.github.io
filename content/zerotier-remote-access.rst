用 ZeroTier 实现内网穿透
########################

:date: 2019-07-18
:slug: use-zerotier-for-remote-access
:status: draft

.. contents:: 目录

如果你在家中有一台 HomeLab 的话，你可能也会像我一样想要随时随地能够访问到它。传统的方案包括
`DDNS <https://en.wikipedia.org/wiki/Dynamic_DNS>`_，
`VPN <https://en.wikipedia.org/wiki/Virtual_private_network>`_ 或者用 ssh 来做
`端口转发 <https://www.ssh.com/ssh/tunneling/example>`_。上述方法都有一个局限，需要家中的
路由器有公网 IP，而目前很多地区的运营商并不提供公网 IP，上面的办法也就没有用武之地了。另一个
办法是使用诸如 `Frp <https://github.com/fatedier/frp>`_ 之类的工具进行转发，这种方案不需
要公网 IP 也能运行，但是需要一台稳定的服务器并进行相关配置，而且延迟也会有所上升。

`ZeroTier <https://www.zerotier.com/>`_ 是一个 L2 VPN 软件，但是与传统的 VPN 软件不同
的是，它并没有采用
`客户端 - 服务器 <https://en.wikipedia.org/wiki/Client%E2%80%93server_model>`_
的模型，而是采用了 P2P 的模型，节点之间会尽可能地通过 NAT 打洞
来建立直接连接，只有无法建立直接连接时才采用服务器中转。这立即就解决了在没有公网 IP 的情况下进行远程
连接的困难问题。同时，ZeroTier 还有强大的
`网络规则引擎 <https://www.zerotier.com/manual/#3>`_，可以轻松地对 VPN 上的流量进行控制。

使用 ZeroTier 进行内网穿透有两种模式，一种是在家庭局域网中某台电脑上安装 ZeroTier，并将其作为虚拟
网络的出口路由，再配合 ZeroTier 的路由表和 iptables，将流量转发到局域网内其他电脑；另一种是直接将
ZeroTier 网段和局域网网段进行 L2 桥接。下面将会简单介绍如何使用这两种方式进行内网穿透。

NAT 方式
=============


桥接方式
=============
