GPG 密钥签名策略
##################

:slug: gpg-policy
:status: published

概要
=====

本文适用于以下密钥所做出的签名：

.. code::

    sec>  rsa4096/0xB29A14086516184D 2018-09-15 [SC]
          C68598CDAF8511D16CB90610B29A14086516184D
    uid                   [ultimate] Luke Lin <lqd1991@gmail.com>
    ssb>  rsa4096/0x9F2E8786D1B7EC74 2018-09-15 [E]

你可以使用以下方式获取我的 GPG 公钥：

- ``gpg --fetch-keys https://keybase.io/quantumghost/key.asc``
- ``gpg --recv-keys --keyserver hkps://keys.openpgp.org C68598CDAF8511D16CB90610B29A14086516184D``
- ``gpg --fetch-keys https://blog.quantumghost.me/key.asc``

你也可以在 `Keybase <https://keybase.io/>`_ 上关注 `我 <https://keybase.io/quantumghost>`_。

**注意**

- 使用 ``--recv-keys`` **导入密钥时务必使用完整的密钥 ID** ，`有资料显示 <https://evil32.com/>`_，
  `密钥碰撞 <https://lwn.net/Articles/689792/>`_ 是可行的。
- 使用 ``--recv-keys`` 导入密钥时请使用 ``hkps://keys.openpgp.org`` 作为 keyserver，使用
  其他 keyserver 可能让你受到 `Certificate Flooding Attach <http://bit.ly/30if6V3>`_ 。

本策略最初撰写于 2019-07-04 且从此日期开始执行，不过也随时可能被更新版本替代。
本文档的结构和内容系受到 Allen Zhong 的 `PGP 密钥签名策略 <https://atr.me/~pgp/policy-cn.html>`_ 启发。

签名策略
===========

签名级别
---------

依据 `GPG 手册 <https://www.gnupg.org/documentation/manuals/gnupg/GPG-Configuration-Options.html>`_
和 `OpenPGP Message Format <https://tools.ietf.org/html/rfc4880#section-5.2.1>`_，证书分为 ``Generic (0)``,
``Persona (1)``, ``Casual (2)``, ``Positive (3)`` 四个级别。为了明确含义，现在定义各级别意义如下
（注意这些级别与 GPG 手册和规范的规定不完全一致）：

- Level 0（一般认证）

  同 GPG 手册中的定义，我不对密钥的验证流程做出保证。

- Level 1（个人认证）

  我会为通过仅通过电子邮件验证的密钥进行这一级别签名，此级别签名仅保证密钥持有者控制被签名 uid
  所对应的电子邮件。

- Level 2（谨慎认证）

  我只会在线下为他人实行此等级签名，此等签名需要验证政府签发的身份证件（身份证，户口本或护照）。
  此级别基本保证被签名 uid 和邮箱由现实中的对应实体控制。

- Level 3（积极认证）

  同二，且被签名者需要是我线下认识并且认为可以足够信任的人，被签名者需要使用硬件 Token（如
  `Yubikey <https://www.yubico.com/>`_，GPG SmartCard）或密钥不可导的软件 Token
  （如 `Krypton <https://krypt.co/>`_）保存密钥。

签名流程
==========

- Level 1

  被签名人需要使用邮箱向我发送一封邮件，该邮箱应属于待签名密钥 uid 所对应邮箱之一，该邮件应使用待签名密钥签名
  并使用我的密钥加密，并需包含如下内容：

  - 密钥指纹
  - 密钥被上传至哪一个密钥服务器（或其他获取密钥的方式）
  - 希望我签名的 UID, 若希望我签名所有 UID 则此项可留空
  - 关于希望获得 Level 0 签名的一些说明

- Level 2

  被签名人需要带上身份证件并与我进行一次线下会面。

  被签名人需要手写或打印需要被签名的密钥指纹到一张纸条上，并在会面时出示给我看。

  签名流程大体同 Level 1，除此之外，我将当面核验被签名人的身份证件和被签名人的邮箱收到了我发出的验证邮件，并同时
  检查被签名人的有效身份证件。

一般步骤：

- 我会向待签名密钥中的每个 uid 对应的电子邮件地址发送一封验证邮件，验证邮件包含随机字符串并使用待签名密钥加密
- 待签名者需要使用对应的邮箱将待签名字符串回复原样给我，在收到邮件后我将确认我收到的随机字符串是否与发出的相同
- 如果待签名者的所有邮箱都进行了回复并通过了验证，我将进行签名并将签名上传至 pool.sks-keyservers.net
- 如果部分 uid 未通过验证，我将挂起签名流程，直到所有 uid 都已通过验证或待签名人放弃签名
- 待签名人需要在 24 小时内完成上述流程，否则视作放弃签名

公平性原则
==========

对于我请求他人做出的签名，我会（按照对方的签名策略）以相同级别签署对方的密钥。同时，我也希望从我所签署的密钥的持有者处获得与我所作出的相同级别的签名。

我希望对密钥进行交叉签名，所以若被签署人并不愿意签署我的密钥，则向我提出签名请求不具有任何意义。

Changelog
==========

- 2019.07.04 初版发布

参考资料
=========

* `Allen Zhong 的 GPG 签名策略 <https://atr.me/~pgp/policy-cn.html>`_
* `GPG 手册对于密钥管理的介绍 <https://www.gnupg.org/gph/en/manual/c235.html>`_


授权协议
===========

Copyright (C) 2019-2019 QuantumGhost.

Permission is granted to copy, distribute and/or modify this document under the terms of the `GNU Free Documentation License <http://www.gnu.org/licenses/fdl.html>`_, Version 1.2 or any later version published by the Free Software Foundation.

