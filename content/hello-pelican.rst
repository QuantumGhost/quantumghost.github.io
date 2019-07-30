Hello, Pelican
###################

:date: 2019-01-14
:slug: hello-pelican
:status: published

这个博客总算是建起来了。

我使用的技术栈：

- 博客系统：`Pelican <https://docs.getpelican.com/>`_
- 评论系统：`Hypothesis <https://hypothes.is>`_
- 发布系统：`Zeit Now <https://zeit>`_

为什么选择 Pelican
======================

TL; DR：因为 Pelican 支持使用 `reStructuredText <https://en.wikipedia.org/wiki/ReStructuredText>`_ 作为博客源文件。

其他静态博客大多主要使用 Markdown 作为博客的源文件。 Markdown 具有易读易书写的优点，但是原版
Markdown 缺乏扩展性，无法嵌入 LaTeX 公式等内容；第三方扩展的语法则存在兼容性问题，各种语法互不兼容。
此外，在 Markdown 中书写 LaTeX 还存在转义的问题。

而这些问题在 reStructuredText （以下简写为 rst） 中都不存在。

首先，rst 只有 `Docutils <http://docutils.sourceforge.net/rst.html>`_ 这一个实现。这意味着没有多种方言。

其次，rst 有强大的扩展机制，可以轻松地通过 `Directives <http://docutils.sourceforge.net/docs/ref/rst/directives.html>`_
进行扩展。比如 `这个 <https://github.com/QuantumGhost/pelican-gist>`_ 插件就通过实现 ``.. gist::`` 指令来在 rst 文档
中包含 gist。基于此，支持 LaTeX 也可以通过自定义指令和 MathJax 渲染来实现。

再次，Pelican 和 rst 都是用 Python 实现的，相较于同样具有扩展性的 `AsciiDoc <http://asciidoc.org/>`_，对于我来说更容易 Hack。

综上所述，我选了 Pelican 而不是 Hugo 或者 Hexo 来生成静态博客。

为什么选择 Hypothesis
======================

TL；DR：因为 web annotation 很 cool。


为什么用 Zeit Now 做发布
=========================

TL；DR：因为 Github 免费用户不能从私有仓库发布 Pages。
