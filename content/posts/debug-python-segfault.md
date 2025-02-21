---
category: technology
date: 2021-01-22
slug: debug-python-segfault
status: published
tags: [python, segfault, linux]
title: Python segfault 调试小记
aliases:
  - /debug-python-segfault.html
---

最近在做 App 的新版本，某一次后端服务上线之后，发现线上 Nginx 报出了
[499 错误](https://httpstatuses.com/499)。

检查之后发现，因为少安装了最近引入的一个依赖，后端服务没有正常启动。（该次发布由另一位同事
手动发布，没有使用发布脚本，所以漏掉了依赖安装阶段）

装好依赖之后，重新发布，发现还是有 499 错误。

一开始我们以为只是报警系统的延迟（我司的报警系统报警会延迟），但是过了一段时间，还是在报警系统上
收到了 499
报警；其他系统的同事也给我们反馈有调用超时的情况。这看起来就不仅仅是延迟了，
定去现上检查一下。

先登录物理机，发现 supervisor 里进程的 status 都是 running，uptime
也正常，看起来没有 什么问题。再登录 Docker 容器，发现容器目录下面有很多
[core.46454]{.title-ref} 之类的文件，猜测可能是 Python 进程发生了 [Core
Dump](https://en.wikipedia.org/wiki/Core_dump)。

Core Dump 的话，最大的可能性自然就是第三方 C 扩展 segfault
之类的了。正好最近添加的依赖 cyksuid 也是 C 扩展，于是就一边尝试把 core
拷贝出容器一边移除 cyksuid 重新发布，同时把 core 拷贝到有 gdb 的
机器上尝试用 gdb 查看 core 的原因。

重新发布完成之后，发现还是有 499 和 Python
进程重启的现象，所以大概就不是 cyksuid 的问题了。另一边 把 core
拷贝到其他机器上调试也没有成果，gdb bt
只能看到下面这样的内存地址，没有调试符号没法知道具体是 哪里出错了：

```text
(gdb) bt
#0  0x00007f0a9f5d4bbe in ?? ()
#1  0x0000000000000001 in ?? ()
#2  0x000000000048e837 in ?? ()
#3  0x0000000000000003 in ?? ()
#4  0x00000000004b2ec8 in ?? ()
#5  0x0000000000000000 in ?? ()
```

没办法，只好一边把容器的流量从线上拿掉，一边进入有问题的 Docker
容器进行调试。

登录容器，先试试手动启动 Python 进程。执行 `python manage.py shell` 发现
gevent 提示：

```text
/usr/local/lib/python3.7/importlib/_bootstrap.py:219: RuntimeWarning: greenlet.greenlet size changed, may indicate binary incompatibility. Expected 144 from C header, got 152 from PyObject
  return f(*args, **kwds)
/usr/local/lib/python3.7/importlib/_bootstrap.py:219: RuntimeWarning: greenlet.greenlet size changed, may indicate binary incompatibility. Expected 144 from C header, got 152 from PyObject
  return f(*args, **kwds)
```

会不会是 Greenlet 导致的呢？

于是就尝试用 gdb 直接在容器内分析 core dump。参考了
[这篇](http://www.brendangregg.com/blog/2016-08-09/gdb-example-ncurses.html)
的 方法，执行 `` gdb `which python` core.46454 ``，然后输入
`bt`，这次终于加载到了调试符号， gdb 输出：

```text
Program terminated with signal 11, Segmentation fault.
#0  __pyx_pf_6gevent_9_greenlet_8Greenlet_36run (__pyx_v_self=0x7f77e1e77950, unused=0x0)
    at src/gevent/greenlet.c:11161
11161   src/gevent/greenlet.c: No such file or directory.
    in src/gevent/greenlet.c
Missing separate debuginfos, use: debuginfo-install python-2.6.6-66.el6_8.x86_64
(gdb) bt
#0  __pyx_pf_6gevent_9_greenlet_8Greenlet_36run (__pyx_v_self=0x7f77e1e77950, unused=0x0)
    at src/gevent/greenlet.c:11161
#1  __pyx_pw_6gevent_9_greenlet_8Greenlet_37run (__pyx_v_self=0x7f77e1e77950, unused=0x0)
    at src/gevent/greenlet.c:11116
#2  0x00007f783e562e3f in __Pyx_CyFunction_CallMethod (func=0x7f783dcd2ad0, args=Unhandled dwarf expression opcode 0xf3
) at src/gevent/_hub_local.c:4445
#3  __Pyx_CyFunction_CallAsMethod (func=0x7f783dcd2ad0, args=Unhandled dwarf expression opcode 0xf3
) at src/gevent/_hub_local.c:4503
```

结合上面的 Warning，大概猜测可能是 greenlet
的问题了。但是为什么物理机上的服务没有问题呢？怀疑可能是依赖版本的问题，于是
分别确认物理机和虚拟机安装的版本，发现物理机是 `greenlet==0.4.15`
而容器环境是 `greenlet==0.4.17`，去 Github 翻了一下 issue
[发现](https://github.com/python-greenlet/greenlet/issues/178) Greenlet
在 0.4.17 更改了 ABI，而 Gevent 没有固定 Greenlet 版本，导致 Gevent 和
Greenlet ABI 不兼容而出现段错误。

既然原因大概明确了，那解决方案也很简单：在 requirements.txt 里面写死
`greenlet==0.4.15` 然后重新构建并发布容器，发布之后运行一切正常，也
证明上面的判断是准确的。

获得的教训是：

1. 不要轻视报警，特别是反复出现的报警（当然报警这个话题都可以单独展开说一篇了）
2. 最好把所有的依赖通过 pip freeze 冻结到 requirement.txt
  里面，或者是干脆使用 [Poetry](https://python-poetry.org)
  来管理依赖； 特别是，一定要固定 gevent 和 greenlet 的版本，保证兼容

FIN.
