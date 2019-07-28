#!/usr/bin/env python

AUTHOR = 'QuantumGhost'
SITENAME = "QuantumGhost's Vault"
SITEURL = ''
THEME = "themes/attila"

PATH = 'content'
TIMEZONE = 'Asia/Hong_Kong'

DEFAULT_LANG = 'zh-CN'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_METADATA = {
    'status': 'draft',
}

DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
USE_FOLDER_AS_CATEGORY = False
PAGE_URL = 'pages/{slug}'

MENUITEMS = (
    ('博客', '/archives'),
    ('分类', '/categories'),
    ("标签", '/tags'),
    ("GPG 签名策略", "/pages/gpg-policy"),
    ("关于", '/pages/about'),
)

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

STATIC_PATHS = ['static', 'extra']
PLUGIN_PATHS = ['plugins']
PLUGINS = ['cjk_auto_spacing', 'pelican_gist']

EXTRA_PATH_METADATA = {
    # 'extra/CNAME': {'path': 'CNAME'},
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/keybase.txt': {'path': 'keybase.txt'},
    'extra/key.asc': {'path': 'key.asc'},
    'extra/now.json': {'path': 'now.json'},
}

# Blogroll

# Social widget
SOCIAL = (('Github', 'https://github.com/QuantumGhost'),
        ('Keybase', 'https://keybase.io/QuantumGhost'),)

DEFAULT_PAGINATION = 20

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
