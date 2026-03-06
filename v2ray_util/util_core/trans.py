#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import gettext
from pathlib import Path

# 通过包文件所在路径定位 locale_i18n 目录，替代已弃用的 pkg_resources
_locale_dir = str(Path(__file__).resolve().parent.parent / 'locale_i18n')

lang = 'en'
if os.path.exists('/etc/v2ray_util/util.cfg'):
    from .config import Config
    lang = Config().get_data('lang')
if lang == 'zh':
    trans = gettext.translation('lang', _locale_dir, languages=['zh_CH'])
else:
    trans = gettext.translation('lang', _locale_dir, languages=['en_US'])
trans.install()
_ = trans.gettext
