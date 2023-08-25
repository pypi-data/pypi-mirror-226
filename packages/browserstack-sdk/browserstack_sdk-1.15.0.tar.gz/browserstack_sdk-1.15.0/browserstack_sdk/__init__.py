# coding: UTF-8
import sys
bstack1l1ll1_opy_ = sys.version_info [0] == 2
bstack11ll1111l_opy_ = 2048
bstack1lll1l1_opy_ = 7
def bstack1ll1lllll_opy_ (bstack111l11l1l_opy_):
    global bstack1l1lll1ll_opy_
    stringNr = ord (bstack111l11l1l_opy_ [-1])
    bstack1l1l111l_opy_ = bstack111l11l1l_opy_ [:-1]
    bstack1l1ll1l1l_opy_ = stringNr % len (bstack1l1l111l_opy_)
    bstack1l1l1ll11_opy_ = bstack1l1l111l_opy_ [:bstack1l1ll1l1l_opy_] + bstack1l1l111l_opy_ [bstack1l1ll1l1l_opy_:]
    if bstack1l1ll1_opy_:
        bstack1ll111lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1111l_opy_ - (bstack11lllllll_opy_ + stringNr) % bstack1lll1l1_opy_) for bstack11lllllll_opy_, char in enumerate (bstack1l1l1ll11_opy_)])
    else:
        bstack1ll111lll_opy_ = str () .join ([chr (ord (char) - bstack11ll1111l_opy_ - (bstack11lllllll_opy_ + stringNr) % bstack1lll1l1_opy_) for bstack11lllllll_opy_, char in enumerate (bstack1l1l1ll11_opy_)])
    return eval (bstack1ll111lll_opy_)
import atexit
import os
import signal
import sys
import time
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
from multiprocessing import Pool
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack1ll11ll1_opy_ = {
	bstack1ll1lllll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࠀ"): bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࠩࠁ"),
  bstack1ll1lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩࠂ"): bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡫ࡦࡻࠪࠃ"),
  bstack1ll1lllll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࠄ"): bstack1ll1lllll_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࠅ"),
  bstack1ll1lllll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪࠆ"): bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫࠇ"),
  bstack1ll1lllll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪࠈ"): bstack1ll1lllll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࠧࠉ"),
  bstack1ll1lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪࠊ"): bstack1ll1lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧࠋ"),
  bstack1ll1lllll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࠌ"): bstack1ll1lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨࠍ"),
  bstack1ll1lllll_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪࠎ"): bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩࠪࠏ"),
  bstack1ll1lllll_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫࠐ"): bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡶࡳࡱ࡫ࠧࠑ"),
  bstack1ll1lllll_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ࠒ"): bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ࠓ"),
  bstack1ll1lllll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠔ"): bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠕ"),
  bstack1ll1lllll_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫࠖ"): bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡼࡩࡥࡧࡲࠫࠗ"),
  bstack1ll1lllll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭࠘"): bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭࠙"),
  bstack1ll1lllll_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩࠚ"): bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩࠛ"),
  bstack1ll1lllll_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩࠜ"): bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩࠝ"),
  bstack1ll1lllll_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨࠞ"): bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨࠟ"),
  bstack1ll1lllll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࠠ"): bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࠡ"),
  bstack1ll1lllll_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩࠢ"): bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩࠣ"),
  bstack1ll1lllll_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪࠤ"): bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪࠥ"),
  bstack1ll1lllll_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧࠦ"): bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧࠧ"),
  bstack1ll1lllll_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫࠨ"): bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡳࡪࡋࡦࡻࡶࠫࠩ"),
  bstack1ll1lllll_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭ࠪ"): bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭ࠫ"),
  bstack1ll1lllll_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬࠬ"): bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡨࡰࡵࡷࡷࠬ࠭"),
  bstack1ll1lllll_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩ࠮"): bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡩࡧࡦࡩࡨࡦࠩ࠯"),
  bstack1ll1lllll_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ࠰"): bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ࠱"),
  bstack1ll1lllll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࠲"): bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࠳"),
  bstack1ll1lllll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࠴"): bstack1ll1lllll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ࠵"),
  bstack1ll1lllll_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭࠶"): bstack1ll1lllll_opy_ (u"ࠪࡶࡪࡧ࡬ࡠ࡯ࡲࡦ࡮ࡲࡥࠨ࠷"),
  bstack1ll1lllll_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ࠸"): bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ࠹"),
  bstack1ll1lllll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭࠺"): bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭࠻"),
  bstack1ll1lllll_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ࠼"): bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ࠽"),
  bstack1ll1lllll_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩ࠾"): bstack1ll1lllll_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬ࠿"),
  bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧࡀ"): bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧࡁ"),
  bstack1ll1lllll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧࡂ"): bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡱࡸࡶࡨ࡫ࠧࡃ"),
  bstack1ll1lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࡄ"): bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࡅ"),
  bstack1ll1lllll_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࡆ"): bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࡇ"),
}
bstack1111111l_opy_ = [
  bstack1ll1lllll_opy_ (u"࠭࡯ࡴࠩࡈ"),
  bstack1ll1lllll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࡉ"),
  bstack1ll1lllll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࡊ"),
  bstack1ll1lllll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࡋ"),
  bstack1ll1lllll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧࡌ"),
  bstack1ll1lllll_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨࡍ"),
  bstack1ll1lllll_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬࡎ"),
]
bstack111l11lll_opy_ = {
  bstack1ll1lllll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࡏ"): [bstack1ll1lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨࡐ"), bstack1ll1lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡤࡔࡁࡎࡇࠪࡑ")],
  bstack1ll1lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࡒ"): bstack1ll1lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ࡓ"),
  bstack1ll1lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࡔ"): bstack1ll1lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠨࡕ"),
  bstack1ll1lllll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࡖ"): bstack1ll1lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠬࡗ"),
  bstack1ll1lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࡘ"): bstack1ll1lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕ࡙ࠫ"),
  bstack1ll1lllll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯࡚ࠪ"): bstack1ll1lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡆࡘࡁࡍࡎࡈࡐࡘࡥࡐࡆࡔࡢࡔࡑࡇࡔࡇࡑࡕࡑ࡛ࠬ"),
  bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ࡜"): bstack1ll1lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࠫ࡝"),
  bstack1ll1lllll_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫ࡞"): bstack1ll1lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬ࡟"),
  bstack1ll1lllll_opy_ (u"ࠩࡤࡴࡵ࠭ࡠ"): [bstack1ll1lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡔࡕࡥࡉࡅࠩࡡ"), bstack1ll1lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ")],
  bstack1ll1lllll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstack1ll1lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstack1ll1lllll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstack1ll1lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack11l1lll_opy_ = {
  bstack1ll1lllll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstack1ll1lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstack1ll1lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstack1ll1lllll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstack1ll1lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstack1ll1lllll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstack1ll1lllll_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstack1ll1lllll_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstack1ll1lllll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstack1ll1lllll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack11l111_opy_ = {
  bstack1ll1lllll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstack1ll1lllll_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstack1ll1lllll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstack1ll1lllll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstack1ll1lllll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstack1ll1lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstack1ll1lllll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstack1ll1lllll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstack1ll1lllll_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstack1ll1lllll_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstack1ll1lllll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstack1ll1lllll_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstack1ll1lllll_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstack1ll1lllll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstack1ll1lllll_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack1111lll1l_opy_ = [
  bstack1ll1lllll_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstack1ll1lllll_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstack1ll1lllll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstack1ll1lllll_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstack1ll1lllll_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstack1ll1lllll_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstack1ll1lllll_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstack1ll1lllll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstack1ll1lllll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstack1ll1lllll_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstack1ll1lllll_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstack1ll1lllll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack111l111_opy_ = [
  bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstack1ll1lllll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstack1ll1lllll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstack1ll1lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstack1ll1lllll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstack1ll1lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstack1ll1lllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstack1ll1lllll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
  bstack1ll1lllll_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬࢫ")
]
bstack11lllll1_opy_ = [
  bstack1ll1lllll_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ࢬ"),
  bstack1ll1lllll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࢭ"),
  bstack1ll1lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࢮ"),
  bstack1ll1lllll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢯ"),
  bstack1ll1lllll_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫࢰ"),
  bstack1ll1lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩࢱ"),
  bstack1ll1lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩࢲ"),
  bstack1ll1lllll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ࢳ"),
  bstack1ll1lllll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢴ"),
  bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࢵ"),
  bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢶ"),
  bstack1ll1lllll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫࢷ"),
  bstack1ll1lllll_opy_ (u"࠭࡯ࡴࠩࢸ"),
  bstack1ll1lllll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࢹ"),
  bstack1ll1lllll_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧࢺ"),
  bstack1ll1lllll_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫࢻ"),
  bstack1ll1lllll_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪࢼ"),
  bstack1ll1lllll_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ࢽ"),
  bstack1ll1lllll_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ࢾ"),
  bstack1ll1lllll_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪࢿ"),
  bstack1ll1lllll_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬࣀ"),
  bstack1ll1lllll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬࣁ"),
  bstack1ll1lllll_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨࣂ"),
  bstack1ll1lllll_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧࣃ"),
  bstack1ll1lllll_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬࣄ"),
  bstack1ll1lllll_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࣅ"),
  bstack1ll1lllll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪࣆ"),
  bstack1ll1lllll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨࣇ"),
  bstack1ll1lllll_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬࣈ"),
  bstack1ll1lllll_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ࣉ"),
  bstack1ll1lllll_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬ࣊"),
  bstack1ll1lllll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋"),
  bstack1ll1lllll_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬ࣌"),
  bstack1ll1lllll_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ࣍"),
  bstack1ll1lllll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࣎"),
  bstack1ll1lllll_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࣏"),
  bstack1ll1lllll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࣐࠭"),
  bstack1ll1lllll_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪ࣑ࠫ"),
  bstack1ll1lllll_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵ࣒ࠪ"),
  bstack1ll1lllll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴ࣓ࠩ"),
  bstack1ll1lllll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨࣔ"),
  bstack1ll1lllll_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩࣕ"),
  bstack1ll1lllll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧࣖ"),
  bstack1ll1lllll_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧࣗ"),
  bstack1ll1lllll_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࣘ"),
  bstack1ll1lllll_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣙ"),
  bstack1ll1lllll_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪࣚ"),
  bstack1ll1lllll_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ࣛ"),
  bstack1ll1lllll_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫࣜ"),
  bstack1ll1lllll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪࣝ"),
  bstack1ll1lllll_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪࣞ"),
  bstack1ll1lllll_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫࣟ"),
  bstack1ll1lllll_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬ࣠"),
  bstack1ll1lllll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࣡"),
  bstack1ll1lllll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫ࣢"),
  bstack1ll1lllll_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࣣࠧ"),
  bstack1ll1lllll_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪࣤ"),
  bstack1ll1lllll_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstack1ll1lllll_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࣦ"),
  bstack1ll1lllll_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬࣧ"),
  bstack1ll1lllll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬࣨ"),
  bstack1ll1lllll_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࣩࠧ"),
  bstack1ll1lllll_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧ࣪"),
  bstack1ll1lllll_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨ࣫"),
  bstack1ll1lllll_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨ࣬"),
  bstack1ll1lllll_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪ࣭ࠪ"),
  bstack1ll1lllll_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸ࣮ࠬ"),
  bstack1ll1lllll_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࣯"),
  bstack1ll1lllll_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࣰࠪ"),
  bstack1ll1lllll_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸࣱ࠭"),
  bstack1ll1lllll_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࣲࠫ"),
  bstack1ll1lllll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ࣳ"),
  bstack1ll1lllll_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪࣴ"),
  bstack1ll1lllll_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬࣵ"),
  bstack1ll1lllll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࣶࠬ"),
  bstack1ll1lllll_opy_ (u"࠭ࡩࡦࠩࣷ"),
  bstack1ll1lllll_opy_ (u"ࠧࡦࡦࡪࡩࠬࣸ"),
  bstack1ll1lllll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨࣹ"),
  bstack1ll1lllll_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨࣺ"),
  bstack1ll1lllll_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬࣻ"),
  bstack1ll1lllll_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬࣼ"),
  bstack1ll1lllll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫࣽ"),
  bstack1ll1lllll_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstack1ll1lllll_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪࣿ"),
  bstack1ll1lllll_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬऀ"),
  bstack1ll1lllll_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩँ"),
  bstack1ll1lllll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪं"),
  bstack1ll1lllll_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ः"),
  bstack1ll1lllll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ऄ"),
  bstack1ll1lllll_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩअ"),
  bstack1ll1lllll_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧआ"),
  bstack1ll1lllll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩइ"),
  bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪई"),
  bstack1ll1lllll_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨउ"),
  bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ऊ"),
  bstack1ll1lllll_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩऋ"),
  bstack1ll1lllll_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬऌ"),
  bstack1ll1lllll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫऍ"),
  bstack1ll1lllll_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫऎ"),
  bstack1ll1lllll_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ए"),
  bstack1ll1lllll_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨऐ"),
  bstack1ll1lllll_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ऑ"),
  bstack1ll1lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ"),
  bstack1ll1lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨओ"),
  bstack1ll1lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭औ"),
  bstack1ll1lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪक"),
  bstack1ll1lllll_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬख"),
  bstack1ll1lllll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩग"),
  bstack1ll1lllll_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭घ"),
  bstack1ll1lllll_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨङ")
]
bstack1l11l111_opy_ = {
  bstack1ll1lllll_opy_ (u"࠭ࡶࠨच"): bstack1ll1lllll_opy_ (u"ࠧࡷࠩछ"),
  bstack1ll1lllll_opy_ (u"ࠨࡨࠪज"): bstack1ll1lllll_opy_ (u"ࠩࡩࠫझ"),
  bstack1ll1lllll_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"): bstack1ll1lllll_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪट"),
  bstack1ll1lllll_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫठ"): bstack1ll1lllll_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬड"),
  bstack1ll1lllll_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"): bstack1ll1lllll_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬण"),
  bstack1ll1lllll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬत"): bstack1ll1lllll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭थ"),
  bstack1ll1lllll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧद"): bstack1ll1lllll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨध"),
  bstack1ll1lllll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩन"): bstack1ll1lllll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऩ"),
  bstack1ll1lllll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫप"): bstack1ll1lllll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬफ"),
  bstack1ll1lllll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫब"): bstack1ll1lllll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬभ"),
  bstack1ll1lllll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭म"): bstack1ll1lllll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧय"),
  bstack1ll1lllll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨर"): bstack1ll1lllll_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऱ"),
  bstack1ll1lllll_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫल"): bstack1ll1lllll_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬळ"),
  bstack1ll1lllll_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬऴ"): bstack1ll1lllll_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧव"),
  bstack1ll1lllll_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨश"): bstack1ll1lllll_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩष"),
  bstack1ll1lllll_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"): bstack1ll1lllll_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ह"),
  bstack1ll1lllll_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫऺ"): bstack1ll1lllll_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऻ"),
  bstack1ll1lllll_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫़ࠧ"): bstack1ll1lllll_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"),
  bstack1ll1lllll_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"): bstack1ll1lllll_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫि"),
  bstack1ll1lllll_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"): bstack1ll1lllll_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫु"),
  bstack1ll1lllll_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"): bstack1ll1lllll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ"),
}
bstack1lll1l1l_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧॄ")
bstack1l1lll11l_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪॅ")
bstack11l1ll11_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬॆ")
bstack111llll11_opy_ = {
  bstack1ll1lllll_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫे"): 50,
  bstack1ll1lllll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩै"): 40,
  bstack1ll1lllll_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬॉ"): 30,
  bstack1ll1lllll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ"): 20,
  bstack1ll1lllll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬो"): 10
}
bstack11llllll1_opy_ = bstack111llll11_opy_[bstack1ll1lllll_opy_ (u"ࠧࡪࡰࡩࡳࠬौ")]
bstack1ll1ll1_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack11l1ll1l1_opy_ = bstack1ll1lllll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧॎ")
bstack11l111l11_opy_ = bstack1ll1lllll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩॏ")
bstack1111lllll_opy_ = bstack1ll1lllll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack1lll11lll_opy_ = [bstack1ll1lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭॑"), bstack1ll1lllll_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ॒࠭")]
bstack1ll1l1l1l_opy_ = [bstack1ll1lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓"), bstack1ll1lllll_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॔")]
bstack11l111lll_opy_ = [
  bstack1ll1lllll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪॕ"),
  bstack1ll1lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"),
  bstack1ll1lllll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨॗ"),
  bstack1ll1lllll_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩक़"),
  bstack1ll1lllll_opy_ (u"࠭ࡡࡱࡲࠪख़"),
  bstack1ll1lllll_opy_ (u"ࠧࡶࡦ࡬ࡨࠬग़"),
  bstack1ll1lllll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪज़"),
  bstack1ll1lllll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩड़"),
  bstack1ll1lllll_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨढ़"),
  bstack1ll1lllll_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩफ़"),
  bstack1ll1lllll_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭य़"), bstack1ll1lllll_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩॠ"),
  bstack1ll1lllll_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪॡ"),
  bstack1ll1lllll_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧॢ"),
  bstack1ll1lllll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ॣ"),
  bstack1ll1lllll_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭।"),
  bstack1ll1lllll_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬ॥"),
  bstack1ll1lllll_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ०"), bstack1ll1lllll_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ१"), bstack1ll1lllll_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ२"), bstack1ll1lllll_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ३"), bstack1ll1lllll_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫ४"),
  bstack1ll1lllll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ५"),
  bstack1ll1lllll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨ६"),
  bstack1ll1lllll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧ७"), bstack1ll1lllll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ८"),
  bstack1ll1lllll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ९"),
  bstack1ll1lllll_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩ॰"),
  bstack1ll1lllll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨॱ"),
  bstack1ll1lllll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫॲ"),
  bstack1ll1lllll_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩॳ"),
  bstack1ll1lllll_opy_ (u"ࠬࡧࡶࡥࠩॴ"), bstack1ll1lllll_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩॵ"), bstack1ll1lllll_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩॶ"), bstack1ll1lllll_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩॷ"),
  bstack1ll1lllll_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧॸ"), bstack1ll1lllll_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩॹ"), bstack1ll1lllll_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧॺ"),
  bstack1ll1lllll_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧॻ"), bstack1ll1lllll_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫॼ"),
  bstack1ll1lllll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩॽ"), bstack1ll1lllll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫॾ"), bstack1ll1lllll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧॿ"), bstack1ll1lllll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬঀ"), bstack1ll1lllll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨঁ"),
  bstack1ll1lllll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨং"), bstack1ll1lllll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪঃ"),
  bstack1ll1lllll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩ঄"),
  bstack1ll1lllll_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭অ"),
  bstack1ll1lllll_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨআ"), bstack1ll1lllll_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫই"), bstack1ll1lllll_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩঈ"), bstack1ll1lllll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨউ"),
  bstack1ll1lllll_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫঊ"),
  bstack1ll1lllll_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩঋ"), bstack1ll1lllll_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨঌ"),
  bstack1ll1lllll_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩ঍"),
  bstack1ll1lllll_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬ঎"),
  bstack1ll1lllll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭এ"),
  bstack1ll1lllll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঐ"),
  bstack1ll1lllll_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧ঑"),
  bstack1ll1lllll_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭঒"),
  bstack1ll1lllll_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩও"),
  bstack1ll1lllll_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨঔ"),
  bstack1ll1lllll_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧক"),
  bstack1ll1lllll_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨখ"),
  bstack1ll1lllll_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭গ"),
  bstack1ll1lllll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬঘ"),
  bstack1ll1lllll_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫঙ"),
  bstack1ll1lllll_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨচ"),
  bstack1ll1lllll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧছ"),
  bstack1ll1lllll_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧজ"),
  bstack1ll1lllll_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫঝ"),
  bstack1ll1lllll_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩঞ"), bstack1ll1lllll_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪট"), bstack1ll1lllll_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪঠ"),
  bstack1ll1lllll_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬড"),
  bstack1ll1lllll_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ঢ"),
  bstack1ll1lllll_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬণ"),
  bstack1ll1lllll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ত"),
  bstack1ll1lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩথ"),
  bstack1ll1lllll_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪদ"),
  bstack1ll1lllll_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪধ"), bstack1ll1lllll_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧন"), bstack1ll1lllll_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬ঩"),
  bstack1ll1lllll_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪপ"),
  bstack1ll1lllll_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬফ"),
  bstack1ll1lllll_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧব"),
  bstack1ll1lllll_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ভ"),
  bstack1ll1lllll_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪম"), bstack1ll1lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧয"),
  bstack1ll1lllll_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬর"), bstack1ll1lllll_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧ঱"),
  bstack1ll1lllll_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫল"),
  bstack1ll1lllll_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ঳"),
  bstack1ll1lllll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ঴"), bstack1ll1lllll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫ঵"), bstack1ll1lllll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬশ"), bstack1ll1lllll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩষ"),
  bstack1ll1lllll_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪস"),
  bstack1ll1lllll_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬহ"),
  bstack1ll1lllll_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ঺"),
  bstack1ll1lllll_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭঻"),
  bstack1ll1lllll_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪ়ࠫ"),
  bstack1ll1lllll_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪঽ"),
  bstack1ll1lllll_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪা"), bstack1ll1lllll_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫি"),
  bstack1ll1lllll_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧী"),
  bstack1ll1lllll_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬু"),
  bstack1ll1lllll_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧূ"),
  bstack1ll1lllll_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৃ"),
  bstack1ll1lllll_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪৄ"),
  bstack1ll1lllll_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ৅"),
  bstack1ll1lllll_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫ৆"),
  bstack1ll1lllll_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬে"),
  bstack1ll1lllll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬৈ"),
  bstack1ll1lllll_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ৉"),
  bstack1ll1lllll_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ৊"),
  bstack1ll1lllll_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧো"),
  bstack1ll1lllll_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨৌ"),
  bstack1ll1lllll_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩ্ࠬ"),
  bstack1ll1lllll_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ৎ"),
  bstack1ll1lllll_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ৏"),
  bstack1ll1lllll_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ৐"),
  bstack1ll1lllll_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ৑"),
  bstack1ll1lllll_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ৒"),
  bstack1ll1lllll_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ৓"),
  bstack1ll1lllll_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭৔"),
  bstack1ll1lllll_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ৕"), bstack1ll1lllll_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ৖"),
  bstack1ll1lllll_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪৗ"), bstack1ll1lllll_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ৘"),
  bstack1ll1lllll_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭৙"),
  bstack1ll1lllll_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ৚"),
  bstack1ll1lllll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ৛"),
  bstack1ll1lllll_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨড়"), bstack1ll1lllll_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨঢ়"),
  bstack1ll1lllll_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ৞"),
  bstack1ll1lllll_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬয়"),
  bstack1ll1lllll_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨৠ"),
  bstack1ll1lllll_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪৡ"),
  bstack1ll1lllll_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬৢ"),
  bstack1ll1lllll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧৣ"),
  bstack1ll1lllll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ৤"),
  bstack1ll1lllll_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ৥"),
  bstack1ll1lllll_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ০"),
  bstack1ll1lllll_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ১"), bstack1ll1lllll_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭২"),
  bstack1ll1lllll_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ৩")
]
bstack11l1lll11_opy_ = bstack1ll1lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ৪")
bstack11l1l1ll1_opy_ = [bstack1ll1lllll_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ৫"), bstack1ll1lllll_opy_ (u"࠭࠮ࡢࡣࡥࠫ৬"), bstack1ll1lllll_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ৭")]
bstack1ll1lll1_opy_ = [bstack1ll1lllll_opy_ (u"ࠨ࡫ࡧࠫ৮"), bstack1ll1lllll_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৯"), bstack1ll1lllll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৰ"), bstack1ll1lllll_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪৱ")]
bstack1l1llllll_opy_ = {
  bstack1ll1lllll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৲"): bstack1ll1lllll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstack1ll1lllll_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৴"): bstack1ll1lllll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৵"),
  bstack1ll1lllll_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"): bstack1ll1lllll_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৷"),
  bstack1ll1lllll_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৸"): bstack1ll1lllll_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৹"),
  bstack1ll1lllll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭৺"): bstack1ll1lllll_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻")
}
bstack1l1l1lll1_opy_ = [
  bstack1ll1lllll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৼ"),
  bstack1ll1lllll_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstack1ll1lllll_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৾"),
  bstack1ll1lllll_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৿"),
  bstack1ll1lllll_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਀"),
]
bstack1l1lllll_opy_ = bstack111l111_opy_ + bstack11lllll1_opy_ + bstack11l111lll_opy_
bstack11l1llll_opy_ = [
  bstack1ll1lllll_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫਁ"),
  bstack1ll1lllll_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨਂ"),
  bstack1ll1lllll_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧਃ"),
  bstack1ll1lllll_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ਄"),
  bstack1ll1lllll_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩਅ"),
  bstack1ll1lllll_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪਆ"),
  bstack1ll1lllll_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫਇ"),
  bstack1ll1lllll_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩਈ")
]
bstack111l1lll1_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀࠫਉ")
bstack1ll111l11_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧਊ")
bstack111ll1ll_opy_ = [ bstack1ll1lllll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ਋") ]
bstack11llll11_opy_ = [ bstack1ll1lllll_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ਌") ]
bstack11l1l1l1l_opy_ = [ bstack1ll1lllll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ਍") ]
bstack1ll1l1l_opy_ = bstack1ll1lllll_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ਎")
bstack1111l11l_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩਏ")
bstack1111l1_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫਐ")
bstack1l1lllll1_opy_ = bstack1ll1lllll_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ਑")
bstack111l1l11_opy_ = [
  bstack1ll1lllll_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭਒"),
  bstack1ll1lllll_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪਓ"),
  bstack1ll1lllll_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬਔ"),
  bstack1ll1lllll_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫਕ"),
  bstack1ll1lllll_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪਖ"),
  bstack1ll1lllll_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨਗ"),
  bstack1ll1lllll_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨਘ"),
  bstack1ll1lllll_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫਙ"),
  bstack1ll1lllll_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬਚ"),
  bstack1ll1lllll_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਛ"),
  bstack1ll1lllll_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ਜ"),
  bstack1ll1lllll_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬਝ"),
  bstack1ll1lllll_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪਞ"),
  bstack1ll1lllll_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩਟ"),
  bstack1ll1lllll_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ਠ"),
  bstack1ll1lllll_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪਡ"),
  bstack1ll1lllll_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧਢ"),
  bstack1ll1lllll_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਣ"),
  bstack1ll1lllll_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧਤ"),
  bstack1ll1lllll_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਥ"),
  bstack1ll1lllll_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧਦ"),
]
bstack1l1ll1l_opy_ = bstack1ll1lllll_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧਧ")
def bstack11lll11l_opy_():
  global CONFIG
  headers = {
        bstack1ll1lllll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩਨ"): bstack1ll1lllll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ਩"),
      }
  proxies = bstack11ll1l1l_opy_(CONFIG, bstack11l1ll11_opy_)
  try:
    response = requests.get(bstack11l1ll11_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack111lllll1_opy_ = response.json()[bstack1ll1lllll_opy_ (u"ࠬ࡮ࡵࡣࡵࠪਪ")]
      logger.debug(bstack11l1111l1_opy_.format(response.json()))
      return bstack111lllll1_opy_
    else:
      logger.debug(bstack1lll1l111_opy_.format(bstack1ll1lllll_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧਫ")))
  except Exception as e:
    logger.debug(bstack1lll1l111_opy_.format(e))
def bstack1l11111l1_opy_(hub_url):
  global CONFIG
  url = bstack1ll1lllll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤਬ")+  hub_url + bstack1ll1lllll_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣਭ")
  headers = {
        bstack1ll1lllll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨਮ"): bstack1ll1lllll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ਯ"),
      }
  proxies = bstack11ll1l1l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11lll1l1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l1111ll_opy_.format(hub_url, e))
def bstack1ll1l11_opy_():
  try:
    global bstack1l11l1ll_opy_
    bstack111lllll1_opy_ = bstack11lll11l_opy_()
    bstack11ll1ll1_opy_ = []
    results = []
    for bstack1lll1111l_opy_ in bstack111lllll1_opy_:
      bstack11ll1ll1_opy_.append(bstack1l1l1l1l1_opy_(target=bstack1l11111l1_opy_,args=(bstack1lll1111l_opy_,)))
    for t in bstack11ll1ll1_opy_:
      t.start()
    for t in bstack11ll1ll1_opy_:
      results.append(t.join())
    bstack1ll111ll1_opy_ = {}
    for item in results:
      hub_url = item[bstack1ll1lllll_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬਰ")]
      latency = item[bstack1ll1lllll_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭਱")]
      bstack1ll111ll1_opy_[hub_url] = latency
    bstack1ll111l1l_opy_ = min(bstack1ll111ll1_opy_, key= lambda x: bstack1ll111ll1_opy_[x])
    bstack1l11l1ll_opy_ = bstack1ll111l1l_opy_
    logger.debug(bstack1l11l1l1l_opy_.format(bstack1ll111l1l_opy_))
  except Exception as e:
    logger.debug(bstack1ll1l11ll_opy_.format(e))
bstack1l111l1ll_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡓࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠼ࠣࡿࢂ࠭ਲ")
bstack1lllll1l_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡄࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡷࡪࡺࡵࡱࠣࠪਲ਼")
bstack1llllll11_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡒࡤࡶࡸ࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠪ਴")
bstack1lll1ll1l_opy_ = bstack1ll1lllll_opy_ (u"ࠩࡖࡥࡳ࡯ࡴࡪࡼࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧਵ")
bstack1ll1111_opy_ = bstack1ll1lllll_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢ࡫ࡹࡧࠦࡵࡳ࡮࠽ࠤࢀࢃࠧਸ਼")
bstack1ll11lll1_opy_ = bstack1ll1lllll_opy_ (u"ࠫࡘ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࡽࢀࠫ਷")
bstack1lll111l_opy_ = bstack1ll1lllll_opy_ (u"ࠬࡘࡥࡤࡧ࡬ࡺࡪࡪࠠࡪࡰࡷࡩࡷࡸࡵࡱࡶ࠯ࠤࡪࡾࡩࡵ࡫ࡱ࡫ࠬਸ")
bstack1ll1l111l_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫਹ")
bstack1l1l111ll_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡣࡱࡨࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࡤࠬ਺")
bstack1l11l1l11_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡄࡴࡵ࡯ࡵ࡮ࡎ࡬ࡦࡷࡧࡲࡺࠢࡳࡥࡨࡱࡡࡨࡧ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠱ࡦࡶࡰࡪࡷࡰࡰ࡮ࡨࡲࡢࡴࡼࡤࠬ਻")
bstack1l111111l_opy_ = bstack1ll1lllll_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵ࠮ࠣࡴࡦࡨ࡯ࡵࠢࡤࡲࡩࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࡭࡫ࡥࡶࡦࡸࡹࠡࡲࡤࡧࡰࡧࡧࡦࡵࠣࡸࡴࠦࡲࡶࡰࠣࡶࡴࡨ࡯ࡵࠢࡷࡩࡸࡺࡳࠡ࡫ࡱࠤࡵࡧࡲࡢ࡮࡯ࡩࡱ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡲࡤࡦࡴࡺࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡵࡨࡰࡪࡴࡩࡶ࡯࡯࡭ࡧࡸࡡࡳࡻࡣ਼ࠫ")
bstack1ll1ll111_opy_ = bstack1ll1lllll_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡧ࡫ࡨࡢࡸࡨࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡦࡪ࡮ࡡࡷࡧࡣࠫ਽")
bstack1l1l1111_opy_ = bstack1ll1lllll_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡧࡰࡱ࡫ࡸࡱ࠲ࡩ࡬ࡪࡧࡱࡸࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡆࡶࡰࡪࡷࡰ࠱ࡕࡿࡴࡩࡱࡱ࠱ࡈࡲࡩࡦࡰࡷࡤࠬਾ")
bstack1ll1111l_opy_ = bstack1ll1lllll_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡦࠧਿ")
bstack1l1111l1l_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡩ࡭ࡳࡪࠠࡦ࡫ࡷ࡬ࡪࡸࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡲࡶࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡹࡧ࡬࡭ࠢࡷ࡬ࡪࠦࡲࡦ࡮ࡨࡺࡦࡴࡴࠡࡲࡤࡧࡰࡧࡧࡦࡵࠣࡹࡸ࡯࡮ࡨࠢࡳ࡭ࡵࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷ࠳࠭ੀ")
bstack1l1ll111_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡉࡣࡱࡨࡱ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡱࡵࡳࡦࠩੁ")
bstack1l1ll111l_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡃ࡯ࡰࠥࡪ࡯࡯ࡧࠤࠫੂ")
bstack1l1l11ll1_opy_ = bstack1ll1lllll_opy_ (u"ࠩࡆࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࠡࡣࡷࠤࡦࡴࡹࠡࡲࡤࡶࡪࡴࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡴ࡬ࠠࠣࡽࢀࠦ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡥ࡯ࡹࡩ࡫ࠠࡢࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰ࠴ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠢࡩ࡭ࡱ࡫ࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡹ࠮ࠨ੃")
bstack11111l11_opy_ = bstack1ll1lllll_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡶࡪࡪࡥ࡯ࡶ࡬ࡥࡱࡹࠠ࡯ࡱࡷࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡢࡦࡧࠤࡹ࡮ࡥ࡮ࠢ࡬ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠦࡡࡴࠢࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧࠦࡡ࡯ࡦࠣࠦࡦࡩࡣࡦࡵࡶࡏࡪࡿࠢࠡࡱࡵࠤࡸ࡫ࡴࠡࡶ࡫ࡩࡲࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠽ࠤࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨࠠࡢࡰࡧࠤࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠣࠩ੄")
bstack1l111llll_opy_ = bstack1ll1lllll_opy_ (u"ࠫࡒࡧ࡬ࡧࡱࡵࡱࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠿ࠨࡻࡾࠤࠪ੅")
bstack111l1l1_opy_ = bstack1ll1lllll_opy_ (u"ࠬࡋ࡮ࡤࡱࡸࡲࡹ࡫ࡲࡦࡦࠣࡩࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡸࡴࠥ࠳ࠠࡼࡿࠪ੆")
bstack11111_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱ࠭ੇ")
bstack111ll1l_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲࠧੈ")
bstack11l111ll_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱࠦࡩࡴࠢࡱࡳࡼࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠡࠨ੉")
bstack1ll111ll_opy_ = bstack1ll1lllll_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥࡹࡴࡢࡴࡷࠤࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡐࡴࡩࡡ࡭࠼ࠣࡿࢂ࠭੊")
bstack11ll111l1_opy_ = bstack1ll1lllll_opy_ (u"ࠪࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡲ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡼ࡯ࡴࡩࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࢀࢃࠧੋ")
bstack1l11ll1_opy_ = bstack1ll1lllll_opy_ (u"࡚ࠫࡶࡤࡢࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠬੌ")
bstack11ll1l11_opy_ = bstack1ll1lllll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀ੍ࠫ")
bstack11ll11l1_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࠠࡢࡰࠣࡥࡵࡶࡲࡰࡲࡵ࡭ࡦࡺࡥࠡࡈ࡚ࠤ࠭ࡸ࡯ࡣࡱࡷ࠳ࡵࡧࡢࡰࡶࠬࠤ࡮ࡴࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠱ࠦࡳ࡬࡫ࡳࠤࡹ࡮ࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡰ࡫ࡹࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡮࡬ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡵ࡬ࡱࡵࡲࡥࠡࡲࡼࡸ࡭ࡵ࡮ࠡࡵࡦࡶ࡮ࡶࡴࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡤࡲࡾࠦࡆࡘ࠰ࠪ੎")
bstack1ll1llll_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡔࡧࡷࡸ࡮ࡴࡧࠡࡪࡷࡸࡵࡖࡲࡰࡺࡼ࠳࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤࡴࡴࠠࡤࡷࡵࡶࡪࡴࡴ࡭ࡻࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡰࡨࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࠥ࠮ࡻࡾࠫ࠯ࠤࡵࡲࡥࡢࡵࡨࠤࡺࡶࡧࡳࡣࡧࡩࠥࡺ࡯ࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࡁࡁ࠹࠴࠰࠯࠲ࠣࡳࡷࠦࡲࡦࡨࡨࡶࠥࡺ࡯ࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡶࡩࡱ࡫࡮ࡪࡷࡰ࠳ࡷࡻ࡮࠮ࡶࡨࡷࡹࡹ࠭ࡣࡧ࡫࡭ࡳࡪ࠭ࡱࡴࡲࡼࡾࠩࡰࡺࡶ࡫ࡳࡳࠦࡦࡰࡴࠣࡥࠥࡽ࡯ࡳ࡭ࡤࡶࡴࡻ࡮ࡥ࠰ࠪ੏")
bstack111l1l1l1_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡾࡳ࡬ࠡࡨ࡬ࡰࡪ࠴࠮ࠨ੐")
bstack111lll11_opy_ = bstack1ll1lllll_opy_ (u"ࠩࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡩࡨࡲࡪࡸࡡࡵࡧࡧࠤࡹ࡮ࡥࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠧࠧੑ")
bstack11l1111l_opy_ = bstack1ll1lllll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦ࠰ࠣࡿࢂ࠭੒")
bstack1l11l11l_opy_ = bstack1ll1lllll_opy_ (u"ࠫࡊࡾࡰࡦࡥࡷࡩࡩࠦࡡࡵࠢ࡯ࡩࡦࡹࡴࠡ࠳ࠣ࡭ࡳࡶࡵࡵ࠮ࠣࡶࡪࡩࡥࡪࡸࡨࡨࠥ࠶ࠧ੓")
bstack1ll111_opy_ = bstack1ll1lllll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡩࡻࡲࡪࡰࡪࠤࡆࡶࡰࠡࡷࡳࡰࡴࡧࡤ࠯ࠢࡾࢁࠬ੔")
bstack11111lll_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡱࡵࡡࡥࠢࡄࡴࡵ࠴ࠠࡊࡰࡹࡥࡱ࡯ࡤࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡻࡾ࠰ࠪ੕")
bstack1l1111_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡌࡧࡼࡷࠥࡩࡡ࡯ࡰࡲࡸࠥࡩ࡯࠮ࡧࡻ࡭ࡸࡺࠠࡢࡵࠣࡥࡵࡶࠠࡷࡣ࡯ࡹࡪࡹࠬࠡࡷࡶࡩࠥࡧ࡮ࡺࠢࡲࡲࡪࠦࡰࡳࡱࡳࡩࡷࡺࡹࠡࡨࡵࡳࡲࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠰ࠥࡵ࡮࡭ࡻࠣࠦࡵࡧࡴࡩࠤࠣࡥࡳࡪࠠࠣࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠦࠥࡩࡡ࡯ࠢࡦࡳ࠲࡫ࡸࡪࡵࡷࠤࡹࡵࡧࡦࡶ࡫ࡩࡷ࠴ࠧ੖")
bstack11ll1l_opy_ = bstack1ll1lllll_opy_ (u"ࠨ࡝ࡌࡲࡻࡧ࡬ࡪࡦࠣࡥࡵࡶࠠࡱࡴࡲࡴࡪࡸࡴࡺ࡟ࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠣࡥࡷ࡫ࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠳ࠦࡆࡰࡴࠣࡱࡴࡸࡥࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡳࡰࡪࡧࡳࡦࠢࡹ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱࡲ࡬ࡹࡲ࠵ࡳࡦࡶ࠰ࡹࡵ࠳ࡴࡦࡵࡷࡷ࠴ࡹࡰࡦࡥ࡬ࡪࡾ࠳ࡡࡱࡲࠪ੗")
bstack1ll1l111_opy_ = bstack1ll1lllll_opy_ (u"ࠩ࡞ࡍࡳࡼࡡ࡭࡫ࡧࠤࡦࡶࡰࠡࡲࡵࡳࡵ࡫ࡲࡵࡻࡠࠤࡘࡻࡰࡱࡱࡵࡸࡪࡪࠠࡷࡣ࡯ࡹࡪࡹࠠࡰࡨࠣࡥࡵࡶࠠࡢࡴࡨࠤࡴ࡬ࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠳ࠦࡆࡰࡴࠣࡱࡴࡸࡥࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡳࡰࡪࡧࡳࡦࠢࡹ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱࡲ࡬ࡹࡲ࠵ࡳࡦࡶ࠰ࡹࡵ࠳ࡴࡦࡵࡷࡷ࠴ࡹࡰࡦࡥ࡬ࡪࡾ࠳ࡡࡱࡲࠪ੘")
bstack1ll11llll_opy_ = bstack1ll1lllll_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡦࡶࡰࠡ࡫ࡧࠤࢀࢃࠠࡧࡱࡵࠤ࡭ࡧࡳࡩࠢ࠽ࠤࢀࢃ࠮ࠨਖ਼")
bstack1ll11l1_opy_ = bstack1ll1lllll_opy_ (u"ࠫࡆࡶࡰࠡࡗࡳࡰࡴࡧࡤࡦࡦࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠣࡍࡉࠦ࠺ࠡࡽࢀࠫਗ਼")
bstack1llll111l_opy_ = bstack1ll1lllll_opy_ (u"࡛ࠬࡳࡪࡰࡪࠤࡆࡶࡰࠡ࠼ࠣࡿࢂ࠴ࠧਜ਼")
bstack1l1111l11_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲࠦࡩࡴࠢࡱࡳࡹࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡳࡷࠦࡶࡢࡰ࡬ࡰࡱࡧࠠࡱࡻࡷ࡬ࡴࡴࠠࡵࡧࡶࡸࡸ࠲ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡰࡢࡴࡤࡰࡱ࡫࡬ࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠥࡃࠠ࠲ࠩੜ")
bstack111ll11_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࡀࠠࡼࡿࠪ੝")
bstack1l11llll1_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡨࡲ࡯ࡴࡧࠣࡦࡷࡵࡷࡴࡧࡵ࠾ࠥࢁࡽࠨਫ਼")
bstack111l111l1_opy_ = bstack1ll1lllll_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥ࡭ࡥࡵࠢࡵࡩࡦࡹ࡯࡯ࠢࡩࡳࡷࠦࡢࡦࡪࡤࡺࡪࠦࡦࡦࡣࡷࡹࡷ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥ࠯ࠢࡾࢁࠬ੟")
bstack11ll111_opy_ = bstack1ll1lllll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡤࡴ࡮ࠦࡣࡢ࡮࡯࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ੠")
bstack11ll1l111_opy_ = bstack1ll1lllll_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡪࡲࡻࠥࡨࡵࡪ࡮ࡧࠤ࡚ࡘࡌ࠭ࠢࡤࡷࠥࡨࡵࡪ࡮ࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡷࡶࡩࡩ࠴ࠧ੡")
bstack1lll1ll_opy_ = bstack1ll1lllll_opy_ (u"࡙ࠬࡥࡳࡸࡨࡶࠥࡹࡩࡥࡧࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠮ࡻࡾࠫࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡷࡦࡳࡥࠡࡣࡶࠤࡨࡲࡩࡦࡰࡷࠤࡸ࡯ࡤࡦࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ࠭ࢁࡽࠪࠩ੢")
bstack1lllll11l_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡖࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡳࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡪࡡࡴࡪࡥࡳࡦࡸࡤ࠻ࠢࡾࢁࠬ੣")
bstack1l11l1l_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡥࡨࡩࡥࡴࡵࠣࡥࠥࡶࡲࡪࡸࡤࡸࡪࠦࡤࡰ࡯ࡤ࡭ࡳࡀࠠࡼࡿࠣ࠲࡙ࠥࡥࡵࠢࡷ࡬ࡪࠦࡦࡰ࡮࡯ࡳࡼ࡯࡮ࡨࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡲࠥࡿ࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨ࠾ࠥࡢ࡮࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰࠱ࠥࡢ࡮ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰ࠿ࠦࡴࡳࡷࡨࠤࡡࡴ࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰ࠫ੤")
bstack1l1111lll_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࡤ࡫ࡲࡳࡱࡵࠤ࠿ࠦࡻࡾࠩ੥")
bstack11lll1lll_opy_ = bstack1ll1lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡࡤࡱࡵࡲࡩࡵࡷࡧࡩࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡵࡲࠡࡕࡇࡏࡘ࡫ࡴࡶࡲࠣࡿࢂࠨ੦")
bstack1llll1l1_opy_ = bstack1ll1lllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥ࡯ࡦࡢࡥࡲࡶ࡬ࡪࡶࡸࡨࡪࡥࡥࡷࡧࡱࡸࠥ࡬࡯ࡳࠢࡖࡈࡐ࡚ࡥࡴࡶࡄࡸࡹ࡫࡭ࡱࡶࡨࡨࠥࢁࡽࠣ੧")
bstack11l11ll11_opy_ = bstack1ll1lllll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡰࡧࡣࡦࡳࡰ࡭࡫ࡷࡹࡩ࡫࡟ࡦࡸࡨࡲࡹࠦࡦࡰࡴࠣࡗࡉࡑࡔࡦࡵࡷࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠠࡼࡿࠥ੨")
bstack111ll111l_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡵࡩࡤࡸࡥࡲࡷࡨࡷࡹࠦࡻࡾࠤ੩")
bstack11lll111_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡐࡐࡕࡗࠤࡊࡼࡥ࡯ࡶࠣࡿࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡ࠼ࠣࡿࢂࠨ੪")
bstack11l1l11ll_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦࡰࡳࡱࡻࡽࠥࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ੫")
bstack11l1111l1_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡ࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠥࢁࡽࠨ੬")
bstack1lll1l111_opy_ = bstack1ll1lllll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴ࠼ࠣࡿࢂ࠭੭")
bstack1l11l1l1l_opy_ = bstack1ll1lllll_opy_ (u"ࠪࡒࡪࡧࡲࡦࡵࡷࠤ࡭ࡻࡢࠡࡣ࡯ࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡹ࠺ࠡࡽࢀࠫ੮")
bstack1ll1l11ll_opy_ = bstack1ll1lllll_opy_ (u"ࠫࡊࡘࡒࡐࡔࠣࡍࡓࠦࡁࡍࡎࡒࡇࡆ࡚ࡅࠡࡊࡘࡆࠥࢁࡽࠨ੯")
bstack11lll1l1_opy_ = bstack1ll1lllll_opy_ (u"ࠬࡒࡡࡵࡧࡱࡧࡾࠦ࡯ࡧࠢ࡫ࡹࡧࡀࠠࡼࡿࠣ࡭ࡸࡀࠠࡼࡿࠪੰ")
bstack11l1111ll_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢ࡯ࡥࡹ࡫࡮ࡤࡻࠣࡪࡴࡸࠠࡼࡿࠣ࡬ࡺࡨ࠺ࠡࡽࢀࠫੱ")
bstack11llll_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡉࡷࡥࠤࡺࡸ࡬ࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢࡲࡴࡹ࡯࡭ࡢ࡮ࠣ࡬ࡺࡨ࠺ࠡࡽࢀࠫੲ")
bstack111l1ll1l_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡴࡶࡴࡪ࡯ࡤࡰࠥ࡮ࡵࡣࠢࡸࡶࡱࡀࠠࡼࡿࠪੳ")
bstack1ll11111l_opy_ = bstack1ll1lllll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡰ࡮ࡹࡴࡴ࠼ࠣࡿࢂ࠭ੴ")
bstack1l11lll11_opy_ = bstack1ll1lllll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴ࠼ࠣࡿࢂ࠭ੵ")
bstack1llll1111_opy_ = bstack1ll1lllll_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡰࡢࡥࠣࡪ࡮ࡲࡥࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࡻࡾࠩ੶")
bstack1l11ll_opy_ = bstack1ll1lllll_opy_ (u"ࠬࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠥࠦࡩࡧࠪࡳࡥ࡬࡫ࠠ࠾࠿ࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠥࢁ࡜࡯ࠢࠣࠤࡹࡸࡹࡼ࡞ࡱࠤࡨࡵ࡮ࡴࡶࠣࡪࡸࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪ࡟ࠫ࡫ࡹ࡜ࠨࠫ࠾ࡠࡳࠦࠠࠡࠢࠣࡪࡸ࠴ࡡࡱࡲࡨࡲࡩࡌࡩ࡭ࡧࡖࡽࡳࡩࠨࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬࠱ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡱࡡ࡬ࡲࡩ࡫ࡸࠪࠢ࠮ࠤࠧࡀࠢࠡ࠭ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࠪࡤࡻࡦ࡯ࡴࠡࡰࡨࡻࡕࡧࡧࡦ࠴࠱ࡩࡻࡧ࡬ࡶࡣࡷࡩ࠭ࠨࠨࠪࠢࡀࡂࠥࢁࡽࠣ࠮ࠣࡠࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࡠࠬ࠯ࠩࠪ࡝ࠥ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩࠨ࡝ࠪࠢ࠮ࠤࠧ࠲࡜࡝ࡰࠥ࠭ࡡࡴࠠࠡࠢࠣࢁࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠬ੷")
bstack1l111lll_opy_ = bstack1ll1lllll_opy_ (u"࠭࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࡢ࡮࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࡜࡯ࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࠡࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻ࡝ࡰࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࡥࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠤࡼࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࡽࡡ࠮࡟ࡲࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࡠࡳࠦࠠࡾࠫ࡟ࡲࢂࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬ੸")
from ._version import __version__
bstack11llll1ll_opy_ = None
CONFIG = {}
bstack1l1l111_opy_ = {}
bstack1ll11l1l1_opy_ = {}
bstack11l1l1l11_opy_ = None
bstack1l11l_opy_ = None
bstack1lll1l_opy_ = None
bstack111ll111_opy_ = -1
bstack1ll1l1l11_opy_ = bstack11llllll1_opy_
bstack11ll11_opy_ = 1
bstack1l111l1l1_opy_ = False
bstack1ll11ll1l_opy_ = False
bstack1ll1ll1l_opy_ = bstack1ll1lllll_opy_ (u"ࠧࠨ੹")
bstack111l1l111_opy_ = bstack1ll1lllll_opy_ (u"ࠨࠩ੺")
bstack1l111l_opy_ = False
bstack1l1111ll_opy_ = True
bstack111l1_opy_ = bstack1ll1lllll_opy_ (u"ࠩࠪ੻")
bstack11ll111ll_opy_ = []
bstack1l11l1ll_opy_ = bstack1ll1lllll_opy_ (u"ࠪࠫ੼")
bstack1111llll_opy_ = False
bstack1llll1l_opy_ = None
bstack11llll1_opy_ = None
bstack1l1l11ll_opy_ = -1
bstack11ll1llll_opy_ = os.path.join(os.path.expanduser(bstack1ll1lllll_opy_ (u"ࠫࢃ࠭੽")), bstack1ll1lllll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੾"), bstack1ll1lllll_opy_ (u"࠭࠮ࡳࡱࡥࡳࡹ࠳ࡲࡦࡲࡲࡶࡹ࠳ࡨࡦ࡮ࡳࡩࡷ࠴ࡪࡴࡱࡱࠫ੿"))
bstack11lll11l1_opy_ = []
bstack1llll11l_opy_ = False
bstack1l1ll1l1_opy_ = False
bstack1l1lll111_opy_ = None
bstack1l11lllll_opy_ = None
bstack1ll11111_opy_ = None
bstack11l11l11l_opy_ = None
bstack1lllll_opy_ = None
bstack11l1l1l_opy_ = None
bstack1l1ll_opy_ = None
bstack111l1lll_opy_ = None
bstack1l11ll11l_opy_ = None
bstack1l11l11ll_opy_ = None
bstack1ll1_opy_ = None
bstack1ll1l1111_opy_ = None
bstack111_opy_ = None
bstack1111_opy_ = None
bstack1lll1ll11_opy_ = None
bstack11lll1ll_opy_ = None
bstack111ll1_opy_ = None
bstack1ll11ll11_opy_ = None
bstack1l11ll111_opy_ = bstack1ll1lllll_opy_ (u"ࠢࠣ઀")
class bstack1l1l1l1l1_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack1l1l1l1l1_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1ll1l1l11_opy_,
                    format=bstack1ll1lllll_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ઁ"),
                    datefmt=bstack1ll1lllll_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫં"))
def bstack1l1ll1ll1_opy_():
  global CONFIG
  global bstack1ll1l1l11_opy_
  if bstack1ll1lllll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬઃ") in CONFIG:
    bstack1ll1l1l11_opy_ = bstack111llll11_opy_[CONFIG[bstack1ll1lllll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭઄")]]
    logging.getLogger().setLevel(bstack1ll1l1l11_opy_)
def bstack1l111ll11_opy_():
  global CONFIG
  global bstack1llll11l_opy_
  bstack1lll11111_opy_ = bstack1lllll1l1_opy_(CONFIG)
  if(bstack1ll1lllll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧઅ") in bstack1lll11111_opy_ and str(bstack1lll11111_opy_[bstack1ll1lllll_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨઆ")]).lower() == bstack1ll1lllll_opy_ (u"ࠧࡵࡴࡸࡩࠬઇ")):
    bstack1llll11l_opy_ = True
def bstack1l1lll11_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll1111ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11l1l11l1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll1lllll_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧઈ") == args[i].lower() or bstack1ll1lllll_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥઉ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack111l1_opy_
      bstack111l1_opy_ += bstack1ll1lllll_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨઊ") + path
      return path
  return None
bstack1l1l11l1l_opy_ = re.compile(bstack1ll1lllll_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢઋ"))
def bstack11_opy_(loader, node):
    value = loader.construct_scalar(node)
    for group in bstack1l1l11l1l_opy_.findall(value):
        if group is not None and os.environ.get(group) is not None:
          value = value.replace(bstack1ll1lllll_opy_ (u"ࠧࠪࡻࠣઌ") + group + bstack1ll1lllll_opy_ (u"ࠨࡽࠣઍ"), os.environ.get(group))
    return value
def bstack1lll11l11_opy_():
  bstack1111lll1_opy_ = bstack11l1l11l1_opy_()
  if bstack1111lll1_opy_ and os.path.exists(os.path.abspath(bstack1111lll1_opy_)):
    fileName = bstack1111lll1_opy_
  if bstack1ll1lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ઎") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack1ll1lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬએ")])) and not bstack1ll1lllll_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫઐ") in locals():
    fileName = os.environ[bstack1ll1lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧઑ")]
  if bstack1ll1lllll_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࠭઒") in locals():
    bstack1l111l1l_opy_ = os.path.abspath(fileName)
  else:
    bstack1l111l1l_opy_ = bstack1ll1lllll_opy_ (u"ࠬ࠭ઓ")
  bstack11ll11l_opy_ = os.getcwd()
  bstack11ll11111_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩઔ")
  bstack1lll111_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫક")
  while (not os.path.exists(bstack1l111l1l_opy_)) and bstack11ll11l_opy_ != bstack1ll1lllll_opy_ (u"ࠣࠤખ"):
    bstack1l111l1l_opy_ = os.path.join(bstack11ll11l_opy_, bstack11ll11111_opy_)
    if not os.path.exists(bstack1l111l1l_opy_):
      bstack1l111l1l_opy_ = os.path.join(bstack11ll11l_opy_, bstack1lll111_opy_)
    if bstack11ll11l_opy_ != os.path.dirname(bstack11ll11l_opy_):
      bstack11ll11l_opy_ = os.path.dirname(bstack11ll11l_opy_)
    else:
      bstack11ll11l_opy_ = bstack1ll1lllll_opy_ (u"ࠤࠥગ")
  if not os.path.exists(bstack1l111l1l_opy_):
    bstack1ll11l1l_opy_(
      bstack1l1l11ll1_opy_.format(os.getcwd()))
  try:
    with open(bstack1l111l1l_opy_, bstack1ll1lllll_opy_ (u"ࠪࡶࠬઘ")) as stream:
        yaml.add_implicit_resolver(bstack1ll1lllll_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧઙ"), bstack1l1l11l1l_opy_)
        yaml.add_constructor(bstack1ll1lllll_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨચ"), bstack11_opy_)
        config = yaml.load(stream, yaml.FullLoader)
        return config
  except:
    with open(bstack1l111l1l_opy_, bstack1ll1lllll_opy_ (u"࠭ࡲࠨછ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1ll11l1l_opy_(bstack1l111llll_opy_.format(str(exc)))
def bstack1lllll1_opy_(config):
  bstack111lll_opy_ = bstack111l_opy_(config)
  for option in list(bstack111lll_opy_):
    if option.lower() in bstack1l11l111_opy_ and option != bstack1l11l111_opy_[option.lower()]:
      bstack111lll_opy_[bstack1l11l111_opy_[option.lower()]] = bstack111lll_opy_[option]
      del bstack111lll_opy_[option]
  return config
def bstack11l11ll1_opy_():
  global bstack1ll11l1l1_opy_
  for key, bstack1l11l1lll_opy_ in bstack111l11lll_opy_.items():
    if isinstance(bstack1l11l1lll_opy_, list):
      for var in bstack1l11l1lll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll11l1l1_opy_[key] = os.environ[var]
          break
    elif bstack1l11l1lll_opy_ in os.environ and os.environ[bstack1l11l1lll_opy_] and str(os.environ[bstack1l11l1lll_opy_]).strip():
      bstack1ll11l1l1_opy_[key] = os.environ[bstack1l11l1lll_opy_]
  if bstack1ll1lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩજ") in os.environ:
    bstack1ll11l1l1_opy_[bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬઝ")] = {}
    bstack1ll11l1l1_opy_[bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ઞ")][bstack1ll1lllll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬટ")] = os.environ[bstack1ll1lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ઠ")]
def bstack11111111_opy_():
  global bstack1l1l111_opy_
  global bstack111l1_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstack1ll1lllll_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨડ").lower() == val.lower():
      bstack1l1l111_opy_[bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪઢ")] = {}
      bstack1l1l111_opy_[bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫણ")][bstack1ll1lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪત")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack1l111l1_opy_ in bstack11l1lll_opy_.items():
    if isinstance(bstack1l111l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l111l1_opy_:
          if idx<len(sys.argv) and bstack1ll1lllll_opy_ (u"ࠩ࠰࠱ࠬથ") + var.lower() == val.lower() and not key in bstack1l1l111_opy_:
            bstack1l1l111_opy_[key] = sys.argv[idx+1]
            bstack111l1_opy_ += bstack1ll1lllll_opy_ (u"ࠪࠤ࠲࠳ࠧદ") + var + bstack1ll1lllll_opy_ (u"ࠫࠥ࠭ધ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstack1ll1lllll_opy_ (u"ࠬ࠳࠭ࠨન") + bstack1l111l1_opy_.lower() == val.lower() and not key in bstack1l1l111_opy_:
          bstack1l1l111_opy_[key] = sys.argv[idx+1]
          bstack111l1_opy_ += bstack1ll1lllll_opy_ (u"࠭ࠠ࠮࠯ࠪ઩") + bstack1l111l1_opy_ + bstack1ll1lllll_opy_ (u"ࠧࠡࠩપ") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack11l11l111_opy_(config):
  bstack111111l1_opy_ = config.keys()
  for bstack11l1ll1l_opy_, bstack1ll1l1l1_opy_ in bstack1ll11ll1_opy_.items():
    if bstack1ll1l1l1_opy_ in bstack111111l1_opy_:
      config[bstack11l1ll1l_opy_] = config[bstack1ll1l1l1_opy_]
      del config[bstack1ll1l1l1_opy_]
  for bstack11l1ll1l_opy_, bstack1ll1l1l1_opy_ in bstack11l111_opy_.items():
    if isinstance(bstack1ll1l1l1_opy_, list):
      for bstack11l1ll1ll_opy_ in bstack1ll1l1l1_opy_:
        if bstack11l1ll1ll_opy_ in bstack111111l1_opy_:
          config[bstack11l1ll1l_opy_] = config[bstack11l1ll1ll_opy_]
          del config[bstack11l1ll1ll_opy_]
          break
    elif bstack1ll1l1l1_opy_ in bstack111111l1_opy_:
        config[bstack11l1ll1l_opy_] = config[bstack1ll1l1l1_opy_]
        del config[bstack1ll1l1l1_opy_]
  for bstack11l1ll1ll_opy_ in list(config):
    for bstack11l111l_opy_ in bstack1l1lllll_opy_:
      if bstack11l1ll1ll_opy_.lower() == bstack11l111l_opy_.lower() and bstack11l1ll1ll_opy_ != bstack11l111l_opy_:
        config[bstack11l111l_opy_] = config[bstack11l1ll1ll_opy_]
        del config[bstack11l1ll1ll_opy_]
  bstack11l1ll_opy_ = []
  if bstack1ll1lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫફ") in config:
    bstack11l1ll_opy_ = config[bstack1ll1lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬબ")]
  for platform in bstack11l1ll_opy_:
    for bstack11l1ll1ll_opy_ in list(platform):
      for bstack11l111l_opy_ in bstack1l1lllll_opy_:
        if bstack11l1ll1ll_opy_.lower() == bstack11l111l_opy_.lower() and bstack11l1ll1ll_opy_ != bstack11l111l_opy_:
          platform[bstack11l111l_opy_] = platform[bstack11l1ll1ll_opy_]
          del platform[bstack11l1ll1ll_opy_]
  for bstack11l1ll1l_opy_, bstack1ll1l1l1_opy_ in bstack11l111_opy_.items():
    for platform in bstack11l1ll_opy_:
      if isinstance(bstack1ll1l1l1_opy_, list):
        for bstack11l1ll1ll_opy_ in bstack1ll1l1l1_opy_:
          if bstack11l1ll1ll_opy_ in platform:
            platform[bstack11l1ll1l_opy_] = platform[bstack11l1ll1ll_opy_]
            del platform[bstack11l1ll1ll_opy_]
            break
      elif bstack1ll1l1l1_opy_ in platform:
        platform[bstack11l1ll1l_opy_] = platform[bstack1ll1l1l1_opy_]
        del platform[bstack1ll1l1l1_opy_]
  for bstack1l11ll1l1_opy_ in bstack1l1llllll_opy_:
    if bstack1l11ll1l1_opy_ in config:
      if not bstack1l1llllll_opy_[bstack1l11ll1l1_opy_] in config:
        config[bstack1l1llllll_opy_[bstack1l11ll1l1_opy_]] = {}
      config[bstack1l1llllll_opy_[bstack1l11ll1l1_opy_]].update(config[bstack1l11ll1l1_opy_])
      del config[bstack1l11ll1l1_opy_]
  for platform in bstack11l1ll_opy_:
    for bstack1l11ll1l1_opy_ in bstack1l1llllll_opy_:
      if bstack1l11ll1l1_opy_ in list(platform):
        if not bstack1l1llllll_opy_[bstack1l11ll1l1_opy_] in platform:
          platform[bstack1l1llllll_opy_[bstack1l11ll1l1_opy_]] = {}
        platform[bstack1l1llllll_opy_[bstack1l11ll1l1_opy_]].update(platform[bstack1l11ll1l1_opy_])
        del platform[bstack1l11ll1l1_opy_]
  config = bstack1lllll1_opy_(config)
  return config
def bstack1l1ll11ll_opy_(config):
  global bstack111l1l111_opy_
  if bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧભ") in config and str(config[bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨમ")]).lower() != bstack1ll1lllll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫય"):
    if not bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪર") in config:
      config[bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ઱")] = {}
    if not bstack1ll1lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪલ") in config[bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ળ")]:
      bstack11ll111l_opy_ = datetime.datetime.now()
      bstack1l1l1l11l_opy_ = bstack11ll111l_opy_.strftime(bstack1ll1lllll_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧ઴"))
      hostname = socket.gethostname()
      bstack1l11111_opy_ = bstack1ll1lllll_opy_ (u"ࠫࠬવ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll1lllll_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧશ").format(bstack1l1l1l11l_opy_, hostname, bstack1l11111_opy_)
      config[bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪષ")][bstack1ll1lllll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩસ")] = identifier
    bstack111l1l111_opy_ = config[bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬહ")][bstack1ll1lllll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ઺")]
  return config
def bstack11l1l111l_opy_():
  if (
    isinstance(os.getenv(bstack1ll1lllll_opy_ (u"ࠪࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠨ઻")), str) and len(os.getenv(bstack1ll1lllll_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍ઼ࠩ"))) > 0
  ) or (
    isinstance(os.getenv(bstack1ll1lllll_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠫઽ")), str) and len(os.getenv(bstack1ll1lllll_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠬા"))) > 0
  ):
    return os.getenv(bstack1ll1lllll_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭િ"), 0)
  if str(os.getenv(bstack1ll1lllll_opy_ (u"ࠨࡅࡌࠫી"))).lower() == bstack1ll1lllll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧુ") and str(os.getenv(bstack1ll1lllll_opy_ (u"ࠪࡇࡎࡘࡃࡍࡇࡆࡍࠬૂ"))).lower() == bstack1ll1lllll_opy_ (u"ࠫࡹࡸࡵࡦࠩૃ"):
    return os.getenv(bstack1ll1lllll_opy_ (u"ࠬࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠨૄ"), 0)
  if str(os.getenv(bstack1ll1lllll_opy_ (u"࠭ࡃࡊࠩૅ"))).lower() == bstack1ll1lllll_opy_ (u"ࠧࡵࡴࡸࡩࠬ૆") and str(os.getenv(bstack1ll1lllll_opy_ (u"ࠨࡖࡕࡅ࡛ࡏࡓࠨે"))).lower() == bstack1ll1lllll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧૈ"):
    return os.getenv(bstack1ll1lllll_opy_ (u"ࠪࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩૉ"), 0)
  if str(os.getenv(bstack1ll1lllll_opy_ (u"ࠫࡈࡏࠧ૊"))).lower() == bstack1ll1lllll_opy_ (u"ࠬࡺࡲࡶࡧࠪો") and str(os.getenv(bstack1ll1lllll_opy_ (u"࠭ࡃࡊࡡࡑࡅࡒࡋࠧૌ"))).lower() == bstack1ll1lllll_opy_ (u"ࠧࡤࡱࡧࡩࡸ࡮ࡩࡱ્ࠩ"):
    return 0 # bstack1l11111l_opy_ bstack1l1l1lll_opy_ not set build number env
  if os.getenv(bstack1ll1lllll_opy_ (u"ࠨࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠫ૎")) and os.getenv(bstack1ll1lllll_opy_ (u"ࠩࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠬ૏")):
    return os.getenv(bstack1ll1lllll_opy_ (u"ࠪࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬૐ"), 0)
  if str(os.getenv(bstack1ll1lllll_opy_ (u"ࠫࡈࡏࠧ૑"))).lower() == bstack1ll1lllll_opy_ (u"ࠬࡺࡲࡶࡧࠪ૒") and str(os.getenv(bstack1ll1lllll_opy_ (u"࠭ࡄࡓࡑࡑࡉࠬ૓"))).lower() == bstack1ll1lllll_opy_ (u"ࠧࡵࡴࡸࡩࠬ૔"):
    return os.getenv(bstack1ll1lllll_opy_ (u"ࠨࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭૕"), 0)
  if str(os.getenv(bstack1ll1lllll_opy_ (u"ࠩࡆࡍࠬ૖"))).lower() == bstack1ll1lllll_opy_ (u"ࠪࡸࡷࡻࡥࠨ૗") and str(os.getenv(bstack1ll1lllll_opy_ (u"ࠫࡘࡋࡍࡂࡒࡋࡓࡗࡋࠧ૘"))).lower() == bstack1ll1lllll_opy_ (u"ࠬࡺࡲࡶࡧࠪ૙"):
    return os.getenv(bstack1ll1lllll_opy_ (u"࠭ࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠩ૚"), 0)
  if str(os.getenv(bstack1ll1lllll_opy_ (u"ࠧࡄࡋࠪ૛"))).lower() == bstack1ll1lllll_opy_ (u"ࠨࡶࡵࡹࡪ࠭૜") and str(os.getenv(bstack1ll1lllll_opy_ (u"ࠩࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠬ૝"))).lower() == bstack1ll1lllll_opy_ (u"ࠪࡸࡷࡻࡥࠨ૞"):
    return os.getenv(bstack1ll1lllll_opy_ (u"ࠫࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠧ૟"), 0)
  if str(os.getenv(bstack1ll1lllll_opy_ (u"ࠬࡉࡉࠨૠ"))).lower() == bstack1ll1lllll_opy_ (u"࠭ࡴࡳࡷࡨࠫૡ") and str(os.getenv(bstack1ll1lllll_opy_ (u"ࠧࡃࡗࡌࡐࡉࡑࡉࡕࡇࠪૢ"))).lower() == bstack1ll1lllll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ૣ"):
    return os.getenv(bstack1ll1lllll_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫ૤"), 0)
  if str(os.getenv(bstack1ll1lllll_opy_ (u"ࠪࡘࡋࡥࡂࡖࡋࡏࡈࠬ૥"))).lower() == bstack1ll1lllll_opy_ (u"ࠫࡹࡸࡵࡦࠩ૦"):
    return os.getenv(bstack1ll1lllll_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬ૧"), 0)
  return -1
def bstack1ll1l1_opy_(bstack11111ll_opy_):
  global CONFIG
  if not bstack1ll1lllll_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨ૨") in CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૩")]:
    return
  CONFIG[bstack1ll1lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૪")] = CONFIG[bstack1ll1lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૫")].replace(
    bstack1ll1lllll_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬ૬"),
    str(bstack11111ll_opy_)
  )
def bstack111l11l_opy_():
  global CONFIG
  if not bstack1ll1lllll_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪ૭") in CONFIG[bstack1ll1lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮")]:
    return
  bstack11ll111l_opy_ = datetime.datetime.now()
  bstack1l1l1l11l_opy_ = bstack11ll111l_opy_.strftime(bstack1ll1lllll_opy_ (u"࠭ࠥࡥ࠯ࠨࡦ࠲ࠫࡈ࠻ࠧࡐࠫ૯"))
  CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૰")] = CONFIG[bstack1ll1lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૱")].replace(
    bstack1ll1lllll_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨ૲"),
    bstack1l1l1l11l_opy_
  )
def bstack111l1111_opy_():
  global CONFIG
  if bstack1ll1lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૳") in CONFIG and not bool(CONFIG[bstack1ll1lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૴")]):
    del CONFIG[bstack1ll1lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૵")]
    return
  if not bstack1ll1lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૶") in CONFIG:
    CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૷")] = bstack1ll1lllll_opy_ (u"ࠨࠥࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫ૸")
  if bstack1ll1lllll_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨૹ") in CONFIG[bstack1ll1lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬૺ")]:
    bstack111l11l_opy_()
    os.environ[bstack1ll1lllll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨૻ")] = CONFIG[bstack1ll1lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧૼ")]
  if not bstack1ll1lllll_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨ૽") in CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૾")]:
    return
  bstack11111ll_opy_ = bstack1ll1lllll_opy_ (u"ࠨࠩ૿")
  bstack111l1l1l_opy_ = bstack11l1l111l_opy_()
  if bstack111l1l1l_opy_ != -1:
    bstack11111ll_opy_ = bstack1ll1lllll_opy_ (u"ࠩࡆࡍࠥ࠭଀") + str(bstack111l1l1l_opy_)
  if bstack11111ll_opy_ == bstack1ll1lllll_opy_ (u"ࠪࠫଁ"):
    bstack11111ll1_opy_ = bstack111llll1_opy_(CONFIG[bstack1ll1lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧଂ")])
    if bstack11111ll1_opy_ != -1:
      bstack11111ll_opy_ = str(bstack11111ll1_opy_)
  if bstack11111ll_opy_:
    bstack1ll1l1_opy_(bstack11111ll_opy_)
    os.environ[bstack1ll1lllll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩଃ")] = CONFIG[bstack1ll1lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ଄")]
def bstack11l1lll1l_opy_(bstack1l1l1l1l_opy_, bstack111111ll_opy_, path):
  bstack11ll1ll11_opy_ = {
    bstack1ll1lllll_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫଅ"): bstack111111ll_opy_
  }
  if os.path.exists(path):
    bstack111l111l_opy_ = json.load(open(path, bstack1ll1lllll_opy_ (u"ࠨࡴࡥࠫଆ")))
  else:
    bstack111l111l_opy_ = {}
  bstack111l111l_opy_[bstack1l1l1l1l_opy_] = bstack11ll1ll11_opy_
  with open(path, bstack1ll1lllll_opy_ (u"ࠤࡺ࠯ࠧଇ")) as outfile:
    json.dump(bstack111l111l_opy_, outfile)
def bstack111llll1_opy_(bstack1l1l1l1l_opy_):
  bstack1l1l1l1l_opy_ = str(bstack1l1l1l1l_opy_)
  bstack1llll11_opy_ = os.path.join(os.path.expanduser(bstack1ll1lllll_opy_ (u"ࠪࢂࠬଈ")), bstack1ll1lllll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫଉ"))
  try:
    if not os.path.exists(bstack1llll11_opy_):
      os.makedirs(bstack1llll11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll1lllll_opy_ (u"ࠬࢄࠧଊ")), bstack1ll1lllll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ଋ"), bstack1ll1lllll_opy_ (u"ࠧ࠯ࡤࡸ࡭ࡱࡪ࠭࡯ࡣࡰࡩ࠲ࡩࡡࡤࡪࡨ࠲࡯ࡹ࡯࡯ࠩଌ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll1lllll_opy_ (u"ࠨࡹࠪ଍")):
        pass
      with open(file_path, bstack1ll1lllll_opy_ (u"ࠤࡺ࠯ࠧ଎")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll1lllll_opy_ (u"ࠪࡶࠬଏ")) as bstack111lll1_opy_:
      bstack11111l1l_opy_ = json.load(bstack111lll1_opy_)
    if bstack1l1l1l1l_opy_ in bstack11111l1l_opy_:
      bstack11lll1l_opy_ = bstack11111l1l_opy_[bstack1l1l1l1l_opy_][bstack1ll1lllll_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨଐ")]
      bstack11llll111_opy_ = int(bstack11lll1l_opy_) + 1
      bstack11l1lll1l_opy_(bstack1l1l1l1l_opy_, bstack11llll111_opy_, file_path)
      return bstack11llll111_opy_
    else:
      bstack11l1lll1l_opy_(bstack1l1l1l1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack111ll11_opy_.format(str(e)))
    return -1
def bstack1lllll111_opy_(config):
  if not config[bstack1ll1lllll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ଑")] or not config[bstack1ll1lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ଒")]:
    return True
  else:
    return False
def bstack1l1l111l1_opy_(config):
  if bstack1ll1lllll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ଓ") in config:
    del(config[bstack1ll1lllll_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧଔ")])
    return False
  if bstack1ll1111ll_opy_() < version.parse(bstack1ll1lllll_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨକ")):
    return False
  if bstack1ll1111ll_opy_() >= version.parse(bstack1ll1lllll_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩଖ")):
    return True
  if bstack1ll1lllll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫଗ") in config and config[bstack1ll1lllll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬଘ")] == False:
    return False
  else:
    return True
def bstack11l11111l_opy_(config, index = 0):
  global bstack1l111l_opy_
  bstack1111ll1l_opy_ = {}
  caps = bstack111l111_opy_ + bstack1111lll1l_opy_
  if bstack1l111l_opy_:
    caps += bstack11l111lll_opy_
  for key in config:
    if key in caps + [bstack1ll1lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଙ")]:
      continue
    bstack1111ll1l_opy_[key] = config[key]
  if bstack1ll1lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଚ") in config:
    for bstack1llll1l1l_opy_ in config[bstack1ll1lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଛ")][index]:
      if bstack1llll1l1l_opy_ in caps + [bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧଜ"), bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫଝ")]:
        continue
      bstack1111ll1l_opy_[bstack1llll1l1l_opy_] = config[bstack1ll1lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଞ")][index][bstack1llll1l1l_opy_]
  bstack1111ll1l_opy_[bstack1ll1lllll_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧଟ")] = socket.gethostname()
  if bstack1ll1lllll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧଠ") in bstack1111ll1l_opy_:
    del(bstack1111ll1l_opy_[bstack1ll1lllll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨଡ")])
  return bstack1111ll1l_opy_
def bstack1llll1ll1_opy_(config):
  global bstack1l111l_opy_
  bstack1lll11ll1_opy_ = {}
  caps = bstack1111lll1l_opy_
  if bstack1l111l_opy_:
    caps+= bstack11l111lll_opy_
  for key in caps:
    if key in config:
      bstack1lll11ll1_opy_[key] = config[key]
  return bstack1lll11ll1_opy_
def bstack111l11111_opy_(bstack1111ll1l_opy_, bstack1lll11ll1_opy_):
  bstack11l111111_opy_ = {}
  for key in bstack1111ll1l_opy_.keys():
    if key in bstack1ll11ll1_opy_:
      bstack11l111111_opy_[bstack1ll11ll1_opy_[key]] = bstack1111ll1l_opy_[key]
    else:
      bstack11l111111_opy_[key] = bstack1111ll1l_opy_[key]
  for key in bstack1lll11ll1_opy_:
    if key in bstack1ll11ll1_opy_:
      bstack11l111111_opy_[bstack1ll11ll1_opy_[key]] = bstack1lll11ll1_opy_[key]
    else:
      bstack11l111111_opy_[key] = bstack1lll11ll1_opy_[key]
  return bstack11l111111_opy_
def bstack111ll1111_opy_(config, index = 0):
  global bstack1l111l_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack1lll11ll1_opy_ = bstack1llll1ll1_opy_(config)
  bstack11l1l1ll_opy_ = bstack1111lll1l_opy_
  bstack11l1l1ll_opy_ += bstack1l1l1lll1_opy_
  if bstack1l111l_opy_:
    bstack11l1l1ll_opy_ += bstack11l111lll_opy_
  if bstack1ll1lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଢ") in config:
    if bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧଣ") in config[bstack1ll1lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ତ")][index]:
      caps[bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଥ")] = config[bstack1ll1lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଦ")][index][bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫଧ")]
    if bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨନ") in config[bstack1ll1lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଩")][index]:
      caps[bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪପ")] = str(config[bstack1ll1lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଫ")][index][bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬବ")])
    bstack11l11_opy_ = {}
    for bstack1l1ll11l_opy_ in bstack11l1l1ll_opy_:
      if bstack1l1ll11l_opy_ in config[bstack1ll1lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଭ")][index]:
        if bstack1l1ll11l_opy_ == bstack1ll1lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨମ"):
          bstack11l11_opy_[bstack1l1ll11l_opy_] = str(config[bstack1ll1lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଯ")][index][bstack1l1ll11l_opy_] * 1.0)
        else:
          bstack11l11_opy_[bstack1l1ll11l_opy_] = config[bstack1ll1lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫର")][index][bstack1l1ll11l_opy_]
        del(config[bstack1ll1lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ଱")][index][bstack1l1ll11l_opy_])
    bstack1lll11ll1_opy_ = update(bstack1lll11ll1_opy_, bstack11l11_opy_)
  bstack1111ll1l_opy_ = bstack11l11111l_opy_(config, index)
  for bstack11l1ll1ll_opy_ in bstack1111lll1l_opy_ + [bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଲ"), bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬଳ")]:
    if bstack11l1ll1ll_opy_ in bstack1111ll1l_opy_:
      bstack1lll11ll1_opy_[bstack11l1ll1ll_opy_] = bstack1111ll1l_opy_[bstack11l1ll1ll_opy_]
      del(bstack1111ll1l_opy_[bstack11l1ll1ll_opy_])
  if bstack1l1l111l1_opy_(config):
    bstack1111ll1l_opy_[bstack1ll1lllll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ଴")] = True
    caps.update(bstack1lll11ll1_opy_)
    caps[bstack1ll1lllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧଵ")] = bstack1111ll1l_opy_
  else:
    bstack1111ll1l_opy_[bstack1ll1lllll_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧଶ")] = False
    caps.update(bstack111l11111_opy_(bstack1111ll1l_opy_, bstack1lll11ll1_opy_))
    if bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ଷ") in caps:
      caps[bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪସ")] = caps[bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨହ")]
      del(caps[bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ଺")])
    if bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭଻") in caps:
      caps[bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ଼")] = caps[bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨଽ")]
      del(caps[bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩା")])
  return caps
def bstack11lllll1l_opy_():
  global bstack1l11l1ll_opy_
  if bstack1ll1111ll_opy_() <= version.parse(bstack1ll1lllll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩି")):
    if bstack1l11l1ll_opy_ != bstack1ll1lllll_opy_ (u"ࠪࠫୀ"):
      return bstack1ll1lllll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧୁ") + bstack1l11l1ll_opy_ + bstack1ll1lllll_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤୂ")
    return bstack1l1lll11l_opy_
  if  bstack1l11l1ll_opy_ != bstack1ll1lllll_opy_ (u"࠭ࠧୃ"):
    return bstack1ll1lllll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤୄ") + bstack1l11l1ll_opy_ + bstack1ll1lllll_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ୅")
  return bstack1lll1l1l_opy_
def bstack1l1ll1l11_opy_(options):
  return hasattr(options, bstack1ll1lllll_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪ୆"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11lll1l11_opy_(options, bstack11lll11_opy_):
  for bstack1l11l1l1_opy_ in bstack11lll11_opy_:
    if bstack1l11l1l1_opy_ in [bstack1ll1lllll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨେ"), bstack1ll1lllll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨୈ")]:
      next
    if bstack1l11l1l1_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11l1l1_opy_]= update(options._experimental_options[bstack1l11l1l1_opy_], bstack11lll11_opy_[bstack1l11l1l1_opy_])
    else:
      options.add_experimental_option(bstack1l11l1l1_opy_, bstack11lll11_opy_[bstack1l11l1l1_opy_])
  if bstack1ll1lllll_opy_ (u"ࠬࡧࡲࡨࡵࠪ୉") in bstack11lll11_opy_:
    for arg in bstack11lll11_opy_[bstack1ll1lllll_opy_ (u"࠭ࡡࡳࡩࡶࠫ୊")]:
      options.add_argument(arg)
    del(bstack11lll11_opy_[bstack1ll1lllll_opy_ (u"ࠧࡢࡴࡪࡷࠬୋ")])
  if bstack1ll1lllll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬୌ") in bstack11lll11_opy_:
    for ext in bstack11lll11_opy_[bstack1ll1lllll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ୍࠭")]:
      options.add_extension(ext)
    del(bstack11lll11_opy_[bstack1ll1lllll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ୎")])
def bstack11lll1ll1_opy_(options, bstack11111l_opy_):
  if bstack1ll1lllll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ୏") in bstack11111l_opy_:
    for bstack11llll1l1_opy_ in bstack11111l_opy_[bstack1ll1lllll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ୐")]:
      if bstack11llll1l1_opy_ in options._preferences:
        options._preferences[bstack11llll1l1_opy_] = update(options._preferences[bstack11llll1l1_opy_], bstack11111l_opy_[bstack1ll1lllll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ୑")][bstack11llll1l1_opy_])
      else:
        options.set_preference(bstack11llll1l1_opy_, bstack11111l_opy_[bstack1ll1lllll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭୒")][bstack11llll1l1_opy_])
  if bstack1ll1lllll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୓") in bstack11111l_opy_:
    for arg in bstack11111l_opy_[bstack1ll1lllll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ୔")]:
      options.add_argument(arg)
def bstack1l11lll_opy_(options, bstack1l1l11l11_opy_):
  if bstack1ll1lllll_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫ୕") in bstack1l1l11l11_opy_:
    options.use_webview(bool(bstack1l1l11l11_opy_[bstack1ll1lllll_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬୖ")]))
  bstack11lll1l11_opy_(options, bstack1l1l11l11_opy_)
def bstack111lll11l_opy_(options, bstack1l11l11l1_opy_):
  for bstack11ll11ll_opy_ in bstack1l11l11l1_opy_:
    if bstack11ll11ll_opy_ in [bstack1ll1lllll_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩୗ"), bstack1ll1lllll_opy_ (u"࠭ࡡࡳࡩࡶࠫ୘")]:
      next
    options.set_capability(bstack11ll11ll_opy_, bstack1l11l11l1_opy_[bstack11ll11ll_opy_])
  if bstack1ll1lllll_opy_ (u"ࠧࡢࡴࡪࡷࠬ୙") in bstack1l11l11l1_opy_:
    for arg in bstack1l11l11l1_opy_[bstack1ll1lllll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୚")]:
      options.add_argument(arg)
  if bstack1ll1lllll_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭୛") in bstack1l11l11l1_opy_:
    options.use_technology_preview(bool(bstack1l11l11l1_opy_[bstack1ll1lllll_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧଡ଼")]))
def bstack111lllll_opy_(options, bstack1l11lll1l_opy_):
  for bstack11l1l1111_opy_ in bstack1l11lll1l_opy_:
    if bstack11l1l1111_opy_ in [bstack1ll1lllll_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨଢ଼"), bstack1ll1lllll_opy_ (u"ࠬࡧࡲࡨࡵࠪ୞")]:
      next
    options._options[bstack11l1l1111_opy_] = bstack1l11lll1l_opy_[bstack11l1l1111_opy_]
  if bstack1ll1lllll_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪୟ") in bstack1l11lll1l_opy_:
    for bstack1l1llll1_opy_ in bstack1l11lll1l_opy_[bstack1ll1lllll_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫୠ")]:
      options.bstack1lll11ll_opy_(
          bstack1l1llll1_opy_, bstack1l11lll1l_opy_[bstack1ll1lllll_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬୡ")][bstack1l1llll1_opy_])
  if bstack1ll1lllll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧୢ") in bstack1l11lll1l_opy_:
    for arg in bstack1l11lll1l_opy_[bstack1ll1lllll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨୣ")]:
      options.add_argument(arg)
def bstack11l11l_opy_(options, caps):
  if not hasattr(options, bstack1ll1lllll_opy_ (u"ࠫࡐࡋ࡙ࠨ୤")):
    return
  if options.KEY == bstack1ll1lllll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ୥") and options.KEY in caps:
    bstack11lll1l11_opy_(options, caps[bstack1ll1lllll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ୦")])
  elif options.KEY == bstack1ll1lllll_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬ୧") and options.KEY in caps:
    bstack11lll1ll1_opy_(options, caps[bstack1ll1lllll_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭୨")])
  elif options.KEY == bstack1ll1lllll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ୩") and options.KEY in caps:
    bstack111lll11l_opy_(options, caps[bstack1ll1lllll_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫ୪")])
  elif options.KEY == bstack1ll1lllll_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬ୫") and options.KEY in caps:
    bstack1l11lll_opy_(options, caps[bstack1ll1lllll_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭୬")])
  elif options.KEY == bstack1ll1lllll_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ୭") and options.KEY in caps:
    bstack111lllll_opy_(options, caps[bstack1ll1lllll_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭୮")])
def bstack111l111ll_opy_(caps):
  global bstack1l111l_opy_
  if bstack1l111l_opy_:
    if bstack1l1lll11_opy_() < version.parse(bstack1ll1lllll_opy_ (u"ࠨ࠴࠱࠷࠳࠶ࠧ୯")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1ll1lllll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ୰")
    if bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨୱ") in caps:
      browser = caps[bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ୲")]
    elif bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭୳") in caps:
      browser = caps[bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ୴")]
    browser = str(browser).lower()
    if browser == bstack1ll1lllll_opy_ (u"ࠧࡪࡲ࡫ࡳࡳ࡫ࠧ୵") or browser == bstack1ll1lllll_opy_ (u"ࠨ࡫ࡳࡥࡩ࠭୶"):
      browser = bstack1ll1lllll_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩ୷")
    if browser == bstack1ll1lllll_opy_ (u"ࠪࡷࡦࡳࡳࡶࡰࡪࠫ୸"):
      browser = bstack1ll1lllll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ୹")
    if browser not in [bstack1ll1lllll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ୺"), bstack1ll1lllll_opy_ (u"࠭ࡥࡥࡩࡨࠫ୻"), bstack1ll1lllll_opy_ (u"ࠧࡪࡧࠪ୼"), bstack1ll1lllll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ୽"), bstack1ll1lllll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ୾")]:
      return None
    try:
      package = bstack1ll1lllll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࢀ࠲ࡴࡶࡴࡪࡱࡱࡷࠬ୿").format(browser)
      name = bstack1ll1lllll_opy_ (u"ࠫࡔࡶࡴࡪࡱࡱࡷࠬ஀")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1ll1l11_opy_(options):
        return None
      for bstack11l1ll1ll_opy_ in caps.keys():
        options.set_capability(bstack11l1ll1ll_opy_, caps[bstack11l1ll1ll_opy_])
      bstack11l11l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1llll1l_opy_(options, bstack11l1l111_opy_):
  if not bstack1l1ll1l11_opy_(options):
    return
  for bstack11l1ll1ll_opy_ in bstack11l1l111_opy_.keys():
    if bstack11l1ll1ll_opy_ in bstack1l1l1lll1_opy_:
      next
    if bstack11l1ll1ll_opy_ in options._caps and type(options._caps[bstack11l1ll1ll_opy_]) in [dict, list]:
      options._caps[bstack11l1ll1ll_opy_] = update(options._caps[bstack11l1ll1ll_opy_], bstack11l1l111_opy_[bstack11l1ll1ll_opy_])
    else:
      options.set_capability(bstack11l1ll1ll_opy_, bstack11l1l111_opy_[bstack11l1ll1ll_opy_])
  bstack11l11l_opy_(options, bstack11l1l111_opy_)
  if bstack1ll1lllll_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡧࡩࡧࡻࡧࡨࡧࡵࡅࡩࡪࡲࡦࡵࡶࠫ஁") in options._caps:
    if options._caps[bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫஂ")] and options._caps[bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬஃ")].lower() != bstack1ll1lllll_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩ஄"):
      del options._caps[bstack1ll1lllll_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨஅ")]
def bstack111lll1ll_opy_(proxy_config):
  if bstack1ll1lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧஆ") in proxy_config:
    proxy_config[bstack1ll1lllll_opy_ (u"ࠫࡸࡹ࡬ࡑࡴࡲࡼࡾ࠭இ")] = proxy_config[bstack1ll1lllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩஈ")]
    del(proxy_config[bstack1ll1lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪஉ")])
  if bstack1ll1lllll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪஊ") in proxy_config and proxy_config[bstack1ll1lllll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ஋")].lower() != bstack1ll1lllll_opy_ (u"ࠩࡧ࡭ࡷ࡫ࡣࡵࠩ஌"):
    proxy_config[bstack1ll1lllll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭஍")] = bstack1ll1lllll_opy_ (u"ࠫࡲࡧ࡮ࡶࡣ࡯ࠫஎ")
  if bstack1ll1lllll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡅࡺࡺ࡯ࡤࡱࡱࡪ࡮࡭ࡕࡳ࡮ࠪஏ") in proxy_config:
    proxy_config[bstack1ll1lllll_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩஐ")] = bstack1ll1lllll_opy_ (u"ࠧࡱࡣࡦࠫ஑")
  return proxy_config
def bstack1lll11l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll1lllll_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧஒ") in config:
    return proxy
  config[bstack1ll1lllll_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨஓ")] = bstack111lll1ll_opy_(config[bstack1ll1lllll_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩஔ")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll1lllll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪக")])
  return proxy
def bstack1ll111l1_opy_(self):
  global CONFIG
  global bstack1ll1_opy_
  try:
    proxy = bstack1l1l1l11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll1lllll_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ஖")):
        proxies = bstack1ll1ll11l_opy_(proxy, bstack11lllll1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111ll1l_opy_ = proxies.popitem()
          if bstack1ll1lllll_opy_ (u"ࠨ࠺࠰࠱ࠥ஗") in bstack1l111ll1l_opy_:
            return bstack1l111ll1l_opy_
          else:
            return bstack1ll1lllll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ஘") + bstack1l111ll1l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll1lllll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧங").format(str(e)))
  return bstack1ll1_opy_(self)
def bstack1l111_opy_():
  global CONFIG
  return bstack1ll1lllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬச") in CONFIG or bstack1ll1lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ஛") in CONFIG
def bstack1l1l1l11_opy_(config):
  if not bstack1l111_opy_():
    return
  if config.get(bstack1ll1lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧஜ")):
    return config.get(bstack1ll1lllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ஝"))
  if config.get(bstack1ll1lllll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪஞ")):
    return config.get(bstack1ll1lllll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫட"))
def bstack1l1111l1_opy_(url):
  try:
      result = urlparse(url)
      return all([result.scheme, result.netloc])
  except:
      return False
def bstack1l1l11_opy_(bstack111l11l1_opy_, bstack1l111l111_opy_):
  from pypac import get_pac
  from pypac import PACSession
  from pypac.parser import PACFile
  import socket
  if os.path.isfile(bstack111l11l1_opy_):
    with open(bstack111l11l1_opy_) as f:
      pac = PACFile(f.read())
  elif bstack1l1111l1_opy_(bstack111l11l1_opy_):
    pac = get_pac(url=bstack111l11l1_opy_)
  else:
    raise Exception(bstack1ll1lllll_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨ஠").format(bstack111l11l1_opy_))
  session = PACSession(pac)
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((bstack1ll1lllll_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺ࠥ஡"), 80))
    bstack11l1ll11l_opy_ = s.getsockname()[0]
    s.close()
  except:
    bstack11l1ll11l_opy_ = bstack1ll1lllll_opy_ (u"ࠪ࠴࠳࠶࠮࠱࠰࠳ࠫ஢")
  proxy_url = session.get_pac().find_proxy_for_url(bstack1l111l111_opy_, bstack11l1ll11l_opy_)
  return proxy_url
def bstack1ll1ll11l_opy_(bstack111l11l1_opy_, bstack1l111l111_opy_):
  proxies = {}
  global bstack11l1l1l1_opy_
  if bstack1ll1lllll_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧண") in globals():
    return bstack11l1l1l1_opy_
  try:
    proxy = bstack1l1l11_opy_(bstack111l11l1_opy_,bstack1l111l111_opy_)
    if bstack1ll1lllll_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧத") in proxy:
      proxies = {}
    elif bstack1ll1lllll_opy_ (u"ࠨࡈࡕࡖࡓࠦ஥") in proxy or bstack1ll1lllll_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨ஦") in proxy or bstack1ll1lllll_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢ஧") in proxy:
      bstack1l111ll1_opy_ = proxy.split(bstack1ll1lllll_opy_ (u"ࠤࠣࠦந"))
      if bstack1ll1lllll_opy_ (u"ࠥ࠾࠴࠵ࠢன") in bstack1ll1lllll_opy_ (u"ࠦࠧப").join(bstack1l111ll1_opy_[1:]):
        proxies = {
          bstack1ll1lllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ஫"): bstack1ll1lllll_opy_ (u"ࠨࠢ஬").join(bstack1l111ll1_opy_[1:])
        }
      else:
        proxies = {
          bstack1ll1lllll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭஭") : str(bstack1l111ll1_opy_[0]).lower()+ bstack1ll1lllll_opy_ (u"ࠣ࠼࠲࠳ࠧம") + bstack1ll1lllll_opy_ (u"ࠤࠥய").join(bstack1l111ll1_opy_[1:])
        }
    elif bstack1ll1lllll_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤர") in proxy:
      bstack1l111ll1_opy_ = proxy.split(bstack1ll1lllll_opy_ (u"ࠦࠥࠨற"))
      if bstack1ll1lllll_opy_ (u"ࠧࡀ࠯࠰ࠤல") in bstack1ll1lllll_opy_ (u"ࠨࠢள").join(bstack1l111ll1_opy_[1:]):
        proxies = {
          bstack1ll1lllll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ழ"): bstack1ll1lllll_opy_ (u"ࠣࠤவ").join(bstack1l111ll1_opy_[1:])
        }
      else:
        proxies = {
          bstack1ll1lllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨஶ"): bstack1ll1lllll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦஷ") + bstack1ll1lllll_opy_ (u"ࠦࠧஸ").join(bstack1l111ll1_opy_[1:])
        }
    else:
      proxies = {
        bstack1ll1lllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫஹ"): proxy
      }
  except Exception as e:
    logger.error(bstack1llll1111_opy_.format(bstack111l11l1_opy_, str(e)))
  bstack11l1l1l1_opy_ = proxies
  return proxies
def bstack11ll1l1l_opy_(config, bstack1l111l111_opy_):
  proxy = bstack1l1l1l11_opy_(config)
  proxies = {}
  if config.get(bstack1ll1lllll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ஺")) or config.get(bstack1ll1lllll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ஻")):
    if proxy.endswith(bstack1ll1lllll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭஼")):
      proxies = bstack1ll1ll11l_opy_(proxy,bstack1l111l111_opy_)
    else:
      proxies = {
        bstack1ll1lllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ஽"): proxy
      }
  return proxies
def bstack1ll111111_opy_():
  return bstack1l111_opy_() and bstack1ll1111ll_opy_() >= version.parse(bstack1l1lllll1_opy_)
def bstack111l_opy_(config):
  bstack111lll_opy_ = {}
  if bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧா") in config:
    bstack111lll_opy_ =  config[bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨி")]
  if bstack1ll1lllll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫீ") in config:
    bstack111lll_opy_ = config[bstack1ll1lllll_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬு")]
  proxy = bstack1l1l1l11_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll1lllll_opy_ (u"ࠧ࠯ࡲࡤࡧࠬூ")) and os.path.isfile(proxy):
      bstack111lll_opy_[bstack1ll1lllll_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ௃")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll1lllll_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ௄")):
        proxies = bstack11ll1l1l_opy_(config, bstack11lllll1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l111ll1l_opy_ = proxies.popitem()
          if bstack1ll1lllll_opy_ (u"ࠥ࠾࠴࠵ࠢ௅") in bstack1l111ll1l_opy_:
            parsed_url = urlparse(bstack1l111ll1l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll1lllll_opy_ (u"ࠦ࠿࠵࠯ࠣெ") + bstack1l111ll1l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack111lll_opy_[bstack1ll1lllll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨே")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack111lll_opy_[bstack1ll1lllll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩை")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack111lll_opy_[bstack1ll1lllll_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ௉")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack111lll_opy_[bstack1ll1lllll_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫொ")] = str(parsed_url.password)
  return bstack111lll_opy_
def bstack1lllll1l1_opy_(config):
  if bstack1ll1lllll_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧோ") in config:
    return config[bstack1ll1lllll_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨௌ")]
  return {}
def bstack111llllll_opy_(caps):
  global bstack111l1l111_opy_
  if bstack1ll1lllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷ்ࠬ") in caps:
    caps[bstack1ll1lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭௎")][bstack1ll1lllll_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ௏")] = True
    if bstack111l1l111_opy_:
      caps[bstack1ll1lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨௐ")][bstack1ll1lllll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ௑")] = bstack111l1l111_opy_
  else:
    caps[bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ௒")] = True
    if bstack111l1l111_opy_:
      caps[bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ௓")] = bstack111l1l111_opy_
def bstack1l111ll_opy_():
  global CONFIG
  if bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ௔") in CONFIG and CONFIG[bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ௕")]:
    bstack111lll_opy_ = bstack111l_opy_(CONFIG)
    bstack11ll11l11_opy_(CONFIG[bstack1ll1lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ௖")], bstack111lll_opy_)
def bstack11ll11l11_opy_(key, bstack111lll_opy_):
  global bstack11llll1ll_opy_
  logger.info(bstack11111_opy_)
  try:
    bstack11llll1ll_opy_ = Local()
    bstack1llll11ll_opy_ = {bstack1ll1lllll_opy_ (u"ࠧ࡬ࡧࡼࠫௗ"): key}
    bstack1llll11ll_opy_.update(bstack111lll_opy_)
    logger.debug(bstack11ll111l1_opy_.format(str(bstack1llll11ll_opy_)))
    bstack11llll1ll_opy_.start(**bstack1llll11ll_opy_)
    if bstack11llll1ll_opy_.isRunning():
      logger.info(bstack11l111ll_opy_)
  except Exception as e:
    bstack1ll11l1l_opy_(bstack1ll111ll_opy_.format(str(e)))
def bstack11l11l1ll_opy_():
  global bstack11llll1ll_opy_
  if bstack11llll1ll_opy_.isRunning():
    logger.info(bstack111ll1l_opy_)
    bstack11llll1ll_opy_.stop()
  bstack11llll1ll_opy_ = None
def bstack1l11l111l_opy_(bstack1l1ll1111_opy_=[]):
  global CONFIG
  bstack1ll1l1lll_opy_ = []
  bstack1l11ll1l_opy_ = [bstack1ll1lllll_opy_ (u"ࠨࡱࡶࠫ௘"), bstack1ll1lllll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ௙"), bstack1ll1lllll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ௚"), bstack1ll1lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭௛"), bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ௜"), bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ௝")]
  try:
    for err in bstack1l1ll1111_opy_:
      bstack111l1l_opy_ = {}
      for k in bstack1l11ll1l_opy_:
        val = CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௞")][int(err[bstack1ll1lllll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ௟")])].get(k)
        if val:
          bstack111l1l_opy_[k] = val
      bstack111l1l_opy_[bstack1ll1lllll_opy_ (u"ࠩࡷࡩࡸࡺࡳࠨ௠")] = {
        err[bstack1ll1lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨ௡")]: err[bstack1ll1lllll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ௢")]
      }
      bstack1ll1l1lll_opy_.append(bstack111l1l_opy_)
  except Exception as e:
    logger.debug(bstack1ll1lllll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡱࡵࡱࡦࡺࡴࡪࡰࡪࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸ࠿ࠦࠧ௣") +str(e))
  finally:
    return bstack1ll1l1lll_opy_
def bstack1111l1l1_opy_():
  global bstack1l11ll111_opy_
  global bstack11ll111ll_opy_
  global bstack11lll11l1_opy_
  if bstack1l11ll111_opy_:
    logger.warning(bstack1l11l1l_opy_.format(str(bstack1l11ll111_opy_)))
  logger.info(bstack1l1ll111_opy_)
  global bstack11llll1ll_opy_
  if bstack11llll1ll_opy_:
    bstack11l11l1ll_opy_()
  try:
    for driver in bstack11ll111ll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1ll111l_opy_)
  bstack1ll1l_opy_()
  if len(bstack11lll11l1_opy_) > 0:
    message = bstack1l11l111l_opy_(bstack11lll11l1_opy_)
    bstack1ll1l_opy_(message)
  else:
    bstack1ll1l_opy_()
def bstack11lll11ll_opy_(self, *args):
  logger.error(bstack1lll111l_opy_)
  bstack1111l1l1_opy_()
  sys.exit(1)
def bstack1ll11l1l_opy_(err):
  logger.critical(bstack111l1l1_opy_.format(str(err)))
  bstack1ll1l_opy_(bstack111l1l1_opy_.format(str(err)))
  atexit.unregister(bstack1111l1l1_opy_)
  sys.exit(1)
def bstack111l1l1ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1ll1l_opy_(message)
  atexit.unregister(bstack1111l1l1_opy_)
  sys.exit(1)
def bstack11l1l1_opy_():
  global CONFIG
  global bstack1l1l111_opy_
  global bstack1ll11l1l1_opy_
  global bstack1l1111ll_opy_
  CONFIG = bstack1lll11l11_opy_()
  bstack11l11ll1_opy_()
  bstack11111111_opy_()
  CONFIG = bstack11l11l111_opy_(CONFIG)
  update(CONFIG, bstack1ll11l1l1_opy_)
  update(CONFIG, bstack1l1l111_opy_)
  CONFIG = bstack1l1ll11ll_opy_(CONFIG)
  if bstack1ll1lllll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ௤") in CONFIG and str(CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ௥")]).lower() == bstack1ll1lllll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ௦"):
    bstack1l1111ll_opy_ = False
  if (bstack1ll1lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ௧") in CONFIG and bstack1ll1lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭௨") in bstack1l1l111_opy_) or (bstack1ll1lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ௩") in CONFIG and bstack1ll1lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௪") not in bstack1ll11l1l1_opy_):
    if os.getenv(bstack1ll1lllll_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ௫")):
      CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௬")] = os.getenv(bstack1ll1lllll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬ௭"))
    else:
      bstack111l1111_opy_()
  elif (bstack1ll1lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ௮") not in CONFIG and bstack1ll1lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ௯") in CONFIG) or (bstack1ll1lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ௰") in bstack1ll11l1l1_opy_ and bstack1ll1lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௱") not in bstack1l1l111_opy_):
    del(CONFIG[bstack1ll1lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ௲")])
  if bstack1lllll111_opy_(CONFIG):
    bstack1ll11l1l_opy_(bstack11111l11_opy_)
  bstack1lll1l11_opy_()
  bstack1llll111_opy_()
  if bstack1l111l_opy_:
    CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡢࡲࡳࠫ௳")] = bstack11l11l1l_opy_(CONFIG)
    logger.info(bstack1llll111l_opy_.format(CONFIG[bstack1ll1lllll_opy_ (u"ࠨࡣࡳࡴࠬ௴")]))
def bstack1llll111_opy_():
  global CONFIG
  global bstack1l111l_opy_
  if bstack1ll1lllll_opy_ (u"ࠩࡤࡴࡵ࠭௵") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack111l1l1ll_opy_(e, bstack1l1l1111_opy_)
    bstack1l111l_opy_ = True
def bstack11l11l1l_opy_(config):
  bstack1ll11_opy_ = bstack1ll1lllll_opy_ (u"ࠪࠫ௶")
  app = config[bstack1ll1lllll_opy_ (u"ࠫࡦࡶࡰࠨ௷")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack11l1l1ll1_opy_:
      if os.path.exists(app):
        bstack1ll11_opy_ = bstack1lllllll1_opy_(config, app)
      elif bstack1l11l11_opy_(app):
        bstack1ll11_opy_ = app
      else:
        bstack1ll11l1l_opy_(bstack11111lll_opy_.format(app))
    else:
      if bstack1l11l11_opy_(app):
        bstack1ll11_opy_ = app
      elif os.path.exists(app):
        bstack1ll11_opy_ = bstack1lllllll1_opy_(app)
      else:
        bstack1ll11l1l_opy_(bstack1ll1l111_opy_)
  else:
    if len(app) > 2:
      bstack1ll11l1l_opy_(bstack1l1111_opy_)
    elif len(app) == 2:
      if bstack1ll1lllll_opy_ (u"ࠬࡶࡡࡵࡪࠪ௸") in app and bstack1ll1lllll_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ௹") in app:
        if os.path.exists(app[bstack1ll1lllll_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ௺")]):
          bstack1ll11_opy_ = bstack1lllllll1_opy_(config, app[bstack1ll1lllll_opy_ (u"ࠨࡲࡤࡸ࡭࠭௻")], app[bstack1ll1lllll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ௼")])
        else:
          bstack1ll11l1l_opy_(bstack11111lll_opy_.format(app))
      else:
        bstack1ll11l1l_opy_(bstack1l1111_opy_)
    else:
      for key in app:
        if key in bstack1ll1lll1_opy_:
          if key == bstack1ll1lllll_opy_ (u"ࠪࡴࡦࡺࡨࠨ௽"):
            if os.path.exists(app[key]):
              bstack1ll11_opy_ = bstack1lllllll1_opy_(config, app[key])
            else:
              bstack1ll11l1l_opy_(bstack11111lll_opy_.format(app))
          else:
            bstack1ll11_opy_ = app[key]
        else:
          bstack1ll11l1l_opy_(bstack11ll1l_opy_)
  return bstack1ll11_opy_
def bstack1l11l11_opy_(bstack1ll11_opy_):
  import re
  bstack11l1ll111_opy_ = re.compile(bstack1ll1lllll_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ௾"))
  bstack1ll111l_opy_ = re.compile(bstack1ll1lllll_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ௿"))
  if bstack1ll1lllll_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬఀ") in bstack1ll11_opy_ or re.fullmatch(bstack11l1ll111_opy_, bstack1ll11_opy_) or re.fullmatch(bstack1ll111l_opy_, bstack1ll11_opy_):
    return True
  else:
    return False
def bstack1lllllll1_opy_(config, path, bstack111ll11ll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll1lllll_opy_ (u"ࠧࡳࡤࠪఁ")).read()).hexdigest()
  bstack111111_opy_ = bstack11l1l11_opy_(md5_hash)
  bstack1ll11_opy_ = None
  if bstack111111_opy_:
    logger.info(bstack1ll11llll_opy_.format(bstack111111_opy_, md5_hash))
    return bstack111111_opy_
  bstack1ll1lll1l_opy_ = MultipartEncoder(
    fields={
        bstack1ll1lllll_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭ం"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll1lllll_opy_ (u"ࠩࡵࡦࠬః")), bstack1ll1lllll_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧఄ")),
        bstack1ll1lllll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧఅ"): bstack111ll11ll_opy_
    }
  )
  response = requests.post(bstack11l1lll11_opy_, data=bstack1ll1lll1l_opy_,
                         headers={bstack1ll1lllll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫఆ"): bstack1ll1lll1l_opy_.content_type}, auth=(config[bstack1ll1lllll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨఇ")], config[bstack1ll1lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪఈ")]))
  try:
    res = json.loads(response.text)
    bstack1ll11_opy_ = res[bstack1ll1lllll_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩఉ")]
    logger.info(bstack1ll11l1_opy_.format(bstack1ll11_opy_))
    bstack11111l1_opy_(md5_hash, bstack1ll11_opy_)
  except ValueError as err:
    bstack1ll11l1l_opy_(bstack1ll111_opy_.format(str(err)))
  return bstack1ll11_opy_
def bstack1lll1l11_opy_():
  global CONFIG
  global bstack11ll11_opy_
  bstack11lll111l_opy_ = 0
  bstack1llll1l11_opy_ = 1
  if bstack1ll1lllll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩఊ") in CONFIG:
    bstack1llll1l11_opy_ = CONFIG[bstack1ll1lllll_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪఋ")]
  if bstack1ll1lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧఌ") in CONFIG:
    bstack11lll111l_opy_ = len(CONFIG[bstack1ll1lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ఍")])
  bstack11ll11_opy_ = int(bstack1llll1l11_opy_) * int(bstack11lll111l_opy_)
def bstack11l1l11_opy_(md5_hash):
  bstack1_opy_ = os.path.join(os.path.expanduser(bstack1ll1lllll_opy_ (u"࠭ࡾࠨఎ")), bstack1ll1lllll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧఏ"), bstack1ll1lllll_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩఐ"))
  if os.path.exists(bstack1_opy_):
    bstack1l111lll1_opy_ = json.load(open(bstack1_opy_,bstack1ll1lllll_opy_ (u"ࠩࡵࡦࠬ఑")))
    if md5_hash in bstack1l111lll1_opy_:
      bstack1lll1l1ll_opy_ = bstack1l111lll1_opy_[md5_hash]
      bstack1l1111ll1_opy_ = datetime.datetime.now()
      bstack1lll1_opy_ = datetime.datetime.strptime(bstack1lll1l1ll_opy_[bstack1ll1lllll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ఒ")], bstack1ll1lllll_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨఓ"))
      if (bstack1l1111ll1_opy_ - bstack1lll1_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1lll1l1ll_opy_[bstack1ll1lllll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪఔ")]):
        return None
      return bstack1lll1l1ll_opy_[bstack1ll1lllll_opy_ (u"࠭ࡩࡥࠩక")]
  else:
    return None
def bstack11111l1_opy_(md5_hash, bstack1ll11_opy_):
  bstack1llll11_opy_ = os.path.join(os.path.expanduser(bstack1ll1lllll_opy_ (u"ࠧࡿࠩఖ")), bstack1ll1lllll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨగ"))
  if not os.path.exists(bstack1llll11_opy_):
    os.makedirs(bstack1llll11_opy_)
  bstack1_opy_ = os.path.join(os.path.expanduser(bstack1ll1lllll_opy_ (u"ࠩࢁࠫఘ")), bstack1ll1lllll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪఙ"), bstack1ll1lllll_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬచ"))
  bstack111l1llll_opy_ = {
    bstack1ll1lllll_opy_ (u"ࠬ࡯ࡤࠨఛ"): bstack1ll11_opy_,
    bstack1ll1lllll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩజ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll1lllll_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫఝ")),
    bstack1ll1lllll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ఞ"): str(__version__)
  }
  if os.path.exists(bstack1_opy_):
    bstack1l111lll1_opy_ = json.load(open(bstack1_opy_,bstack1ll1lllll_opy_ (u"ࠩࡵࡦࠬట")))
  else:
    bstack1l111lll1_opy_ = {}
  bstack1l111lll1_opy_[md5_hash] = bstack111l1llll_opy_
  with open(bstack1_opy_, bstack1ll1lllll_opy_ (u"ࠥࡻ࠰ࠨఠ")) as outfile:
    json.dump(bstack1l111lll1_opy_, outfile)
def bstack11l1l1lll_opy_(self):
  return
def bstack11ll1111_opy_(self):
  return
def bstack1l11l1_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack111ll1l1_opy_(self):
  global bstack1ll1ll1l_opy_
  global bstack11l1l1l11_opy_
  global bstack1l11lllll_opy_
  try:
    if bstack1ll1lllll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫడ") in bstack1ll1ll1l_opy_ and self.session_id != None:
      bstack1ll11lll_opy_ = bstack1ll1lllll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬఢ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll1lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ణ")
      bstack11ll1ll1l_opy_ = bstack111l11ll_opy_(bstack1ll1lllll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪత"), bstack1ll1lllll_opy_ (u"ࠨࠩథ"), bstack1ll11lll_opy_, bstack1ll1lllll_opy_ (u"ࠩ࠯ࠤࠬద").join(threading.current_thread().bstackTestErrorMessages), bstack1ll1lllll_opy_ (u"ࠪࠫధ"), bstack1ll1lllll_opy_ (u"ࠫࠬన"))
      if self != None:
        self.execute_script(bstack11ll1ll1l_opy_)
  except Exception as e:
    logger.debug(bstack1ll1lllll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨ఩") + str(e))
  bstack1l11lllll_opy_(self)
  self.session_id = None
def bstack11llll11l_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11l1l1l11_opy_
  global bstack111ll111_opy_
  global bstack1lll1l_opy_
  global bstack1l111l1l1_opy_
  global bstack1ll11ll1l_opy_
  global bstack1ll1ll1l_opy_
  global bstack1l1lll111_opy_
  global bstack11ll111ll_opy_
  global bstack1l1l11ll_opy_
  CONFIG[bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨప")] = str(bstack1ll1ll1l_opy_) + str(__version__)
  command_executor = bstack11lllll1l_opy_()
  logger.debug(bstack1ll1111_opy_.format(command_executor))
  proxy = bstack1lll11l1_opy_(CONFIG, proxy)
  bstack11ll1_opy_ = 0 if bstack111ll111_opy_ < 0 else bstack111ll111_opy_
  try:
    if bstack1l111l1l1_opy_ is True:
      bstack11ll1_opy_ = int(multiprocessing.current_process().name)
    elif bstack1ll11ll1l_opy_ is True:
      bstack11ll1_opy_ = int(threading.current_thread().name)
  except:
    bstack11ll1_opy_ = 0
  bstack11l1l111_opy_ = bstack111ll1111_opy_(CONFIG, bstack11ll1_opy_)
  logger.debug(bstack1llllll11_opy_.format(str(bstack11l1l111_opy_)))
  if bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫఫ") in CONFIG and CONFIG[bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬబ")]:
    bstack111llllll_opy_(bstack11l1l111_opy_)
  if desired_capabilities:
    bstack11ll1l1_opy_ = bstack11l11l111_opy_(desired_capabilities)
    bstack11ll1l1_opy_[bstack1ll1lllll_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩభ")] = bstack1l1l111l1_opy_(CONFIG)
    bstack11l_opy_ = bstack111ll1111_opy_(bstack11ll1l1_opy_)
    if bstack11l_opy_:
      bstack11l1l111_opy_ = update(bstack11l_opy_, bstack11l1l111_opy_)
    desired_capabilities = None
  if options:
    bstack1l1llll1l_opy_(options, bstack11l1l111_opy_)
  if not options:
    options = bstack111l111ll_opy_(bstack11l1l111_opy_)
  if proxy and bstack1ll1111ll_opy_() >= version.parse(bstack1ll1lllll_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪమ")):
    options.proxy(proxy)
  if options and bstack1ll1111ll_opy_() >= version.parse(bstack1ll1lllll_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪయ")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1ll1111ll_opy_() < version.parse(bstack1ll1lllll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫర")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11l1l111_opy_)
  logger.info(bstack1lllll1l_opy_)
  if bstack1ll1111ll_opy_() >= version.parse(bstack1ll1lllll_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ఱ")):
    bstack1l1lll111_opy_(self, command_executor=command_executor,
          options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll1111ll_opy_() >= version.parse(bstack1ll1lllll_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ల")):
    bstack1l1lll111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll1111ll_opy_() >= version.parse(bstack1ll1lllll_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨళ")):
    bstack1l1lll111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l1lll111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack1lll_opy_ = bstack1ll1lllll_opy_ (u"ࠩࠪఴ")
    if bstack1ll1111ll_opy_() >= version.parse(bstack1ll1lllll_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫవ")):
      bstack1lll_opy_ = self.caps.get(bstack1ll1lllll_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦశ"))
    else:
      bstack1lll_opy_ = self.capabilities.get(bstack1ll1lllll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧష"))
    if bstack1lll_opy_:
      if bstack1ll1111ll_opy_() <= version.parse(bstack1ll1lllll_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭స")):
        self.command_executor._url = bstack1ll1lllll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣహ") + bstack1l11l1ll_opy_ + bstack1ll1lllll_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ఺")
      else:
        self.command_executor._url = bstack1ll1lllll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ఻") + bstack1lll_opy_ + bstack1ll1lllll_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥ఼ࠦ")
      logger.debug(bstack11llll_opy_.format(bstack1lll_opy_))
    else:
      logger.debug(bstack111l1ll1l_opy_.format(bstack1ll1lllll_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧఽ")))
  except Exception as e:
    logger.debug(bstack111l1ll1l_opy_.format(e))
  if bstack1ll1lllll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫా") in bstack1ll1ll1l_opy_:
    bstack1ll1llll1_opy_(bstack111ll111_opy_, bstack1l1l11ll_opy_)
  bstack11l1l1l11_opy_ = self.session_id
  if bstack1ll1lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ి") in bstack1ll1ll1l_opy_:
    threading.current_thread().bstack1l1lll_opy_ = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack11ll111ll_opy_.append(self)
  if bstack1ll1lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪీ") in CONFIG and bstack1ll1lllll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ు") in CONFIG[bstack1ll1lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬూ")][bstack11ll1_opy_]:
    bstack1lll1l_opy_ = CONFIG[bstack1ll1lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ృ")][bstack11ll1_opy_][bstack1ll1lllll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩౄ")]
  logger.debug(bstack1ll11lll1_opy_.format(bstack11l1l1l11_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack11l11ll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1111llll_opy_
      if(bstack1ll1lllll_opy_ (u"ࠧ࡯࡮ࡥࡧࡻ࠲࡯ࡹࠢ౅") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll1lllll_opy_ (u"࠭ࡾࠨె")), bstack1ll1lllll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧే"), bstack1ll1lllll_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪై")), bstack1ll1lllll_opy_ (u"ࠩࡺࠫ౉")) as fp:
          fp.write(bstack1ll1lllll_opy_ (u"ࠥࠦొ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll1lllll_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨో")))):
          with open(args[1], bstack1ll1lllll_opy_ (u"ࠬࡸࠧౌ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll1lllll_opy_ (u"࠭ࡡࡴࡻࡱࡧࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡠࡰࡨࡻࡕࡧࡧࡦࠪࡦࡳࡳࡺࡥࡹࡶ࠯ࠤࡵࡧࡧࡦࠢࡀࠤࡻࡵࡩࡥࠢ࠳్࠭ࠬ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l11ll_opy_)
            lines.insert(1, bstack1l111lll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll1lllll_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ౎")), bstack1ll1lllll_opy_ (u"ࠨࡹࠪ౏")) as bstack11l1ll1_opy_:
              bstack11l1ll1_opy_.writelines(lines)
        CONFIG[bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ౐")] = str(bstack1ll1ll1l_opy_) + str(__version__)
        bstack11ll1_opy_ = 0 if bstack111ll111_opy_ < 0 else bstack111ll111_opy_
        if bstack1l111l1l1_opy_ is True:
          bstack11ll1_opy_ = int(threading.current_thread().getName())
        CONFIG[bstack1ll1lllll_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥ౑")] = False
        CONFIG[bstack1ll1lllll_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ౒")] = True
        bstack11l1l111_opy_ = bstack111ll1111_opy_(CONFIG, bstack11ll1_opy_)
        logger.debug(bstack1llllll11_opy_.format(str(bstack11l1l111_opy_)))
        if CONFIG[bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ౓")]:
          bstack111llllll_opy_(bstack11l1l111_opy_)
        if bstack1ll1lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౔") in CONFIG and bstack1ll1lllll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩౕࠬ") in CONFIG[bstack1ll1lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶౖࠫ")][bstack11ll1_opy_]:
          bstack1lll1l_opy_ = CONFIG[bstack1ll1lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౗")][bstack11ll1_opy_][bstack1ll1lllll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨౘ")]
        args.append(os.path.join(os.path.expanduser(bstack1ll1lllll_opy_ (u"ࠫࢃ࠭ౙ")), bstack1ll1lllll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬౚ"), bstack1ll1lllll_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ౛")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11l1l111_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll1lllll_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ౜"))
      bstack1111llll_opy_ = True
      return bstack1111_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1ll1l11l1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11l1l1l11_opy_
    global bstack111ll111_opy_
    global bstack1lll1l_opy_
    global bstack1l111l1l1_opy_
    global bstack1ll1ll1l_opy_
    global bstack1l1lll111_opy_
    CONFIG[bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪౝ")] = str(bstack1ll1ll1l_opy_) + str(__version__)
    bstack11ll1_opy_ = 0 if bstack111ll111_opy_ < 0 else bstack111ll111_opy_
    if bstack1l111l1l1_opy_ is True:
      bstack11ll1_opy_ = int(threading.current_thread().getName())
    CONFIG[bstack1ll1lllll_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ౞")] = True
    bstack11l1l111_opy_ = bstack111ll1111_opy_(CONFIG, bstack11ll1_opy_)
    logger.debug(bstack1llllll11_opy_.format(str(bstack11l1l111_opy_)))
    if CONFIG[bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ౟")]:
      bstack111llllll_opy_(bstack11l1l111_opy_)
    if bstack1ll1lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧౠ") in CONFIG and bstack1ll1lllll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪౡ") in CONFIG[bstack1ll1lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩౢ")][bstack11ll1_opy_]:
      bstack1lll1l_opy_ = CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪౣ")][bstack11ll1_opy_][bstack1ll1lllll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭౤")]
    import urllib
    import json
    bstack1l1l1ll_opy_ = bstack1ll1lllll_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ౥") + urllib.parse.quote(json.dumps(bstack11l1l111_opy_))
    browser = self.connect(bstack1l1l1ll_opy_)
    return browser
except Exception as e:
    pass
def bstack111l1ll_opy_():
    global bstack1111llll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll1l11l1_opy_
        bstack1111llll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11l11ll_opy_
      bstack1111llll_opy_ = True
    except Exception as e:
      pass
def bstack1l11111ll_opy_(context, bstack11ll1lll_opy_):
  try:
    context.page.evaluate(bstack1ll1lllll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ౦"), bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨ౧")+ json.dumps(bstack11ll1lll_opy_) + bstack1ll1lllll_opy_ (u"ࠧࢃࡽࠣ౨"))
  except Exception as e:
    logger.debug(bstack1ll1lllll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦ౩"), e)
def bstack1l11l1111_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1ll1lllll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ౪"), bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭౫") + json.dumps(message) + bstack1ll1lllll_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬ౬") + json.dumps(level) + bstack1ll1lllll_opy_ (u"ࠪࢁࢂ࠭౭"))
  except Exception as e:
    logger.debug(bstack1ll1lllll_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢ౮"), e)
def bstack11l1llll1_opy_(context, status, message = bstack1ll1lllll_opy_ (u"ࠧࠨ౯")):
  try:
    if(status == bstack1ll1lllll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ౰")):
      context.page.evaluate(bstack1ll1lllll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ౱"), bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠩ౲") + json.dumps(bstack1ll1lllll_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࠦ౳") + str(message)) + bstack1ll1lllll_opy_ (u"ࠪ࠰ࠧࡹࡴࡢࡶࡸࡷࠧࡀࠧ౴") + json.dumps(status) + bstack1ll1lllll_opy_ (u"ࠦࢂࢃࠢ౵"))
    else:
      context.page.evaluate(bstack1ll1lllll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ౶"), bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠧ౷") + json.dumps(status) + bstack1ll1lllll_opy_ (u"ࠢࡾࡿࠥ౸"))
  except Exception as e:
    logger.debug(bstack1ll1lllll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧ౹"), e)
def bstack111lll111_opy_(self, url):
  global bstack111_opy_
  try:
    bstack1lll1l11l_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1111lll_opy_.format(str(err)))
  try:
    bstack111_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1lll1l_opy_ = str(e)
      if any(err_msg in bstack1l1lll1l_opy_ for err_msg in bstack111l1l11_opy_):
        bstack1lll1l11l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1111lll_opy_.format(str(err)))
    raise e
def bstack1llll_opy_(self):
  global bstack11llll1_opy_
  bstack11llll1_opy_ = self
  return
def bstack1ll1l1ll1_opy_(self):
  global bstack1llll1l_opy_
  bstack1llll1l_opy_ = self
  return
def bstack1l1ll11_opy_(self, test):
  global CONFIG
  global bstack1llll1l_opy_
  global bstack11llll1_opy_
  global bstack11l1l1l11_opy_
  global bstack1l11l_opy_
  global bstack1lll1l_opy_
  global bstack1ll11111_opy_
  global bstack11l11l11l_opy_
  global bstack1lllll_opy_
  global bstack11ll111ll_opy_
  try:
    if not bstack11l1l1l11_opy_:
      with open(os.path.join(os.path.expanduser(bstack1ll1lllll_opy_ (u"ࠩࢁࠫ౺")), bstack1ll1lllll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ౻"), bstack1ll1lllll_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭౼"))) as f:
        bstack1l1l1_opy_ = json.loads(bstack1ll1lllll_opy_ (u"ࠧࢁࠢ౽") + f.read().strip() + bstack1ll1lllll_opy_ (u"࠭ࠢࡹࠤ࠽ࠤࠧࡿࠢࠨ౾") + bstack1ll1lllll_opy_ (u"ࠢࡾࠤ౿"))
        bstack11l1l1l11_opy_ = bstack1l1l1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11ll111ll_opy_:
    for driver in bstack11ll111ll_opy_:
      if bstack11l1l1l11_opy_ == driver.session_id:
        if test:
          bstack1ll1lll11_opy_ = str(test.data)
        if not bstack1llll11l_opy_ and bstack1ll1lll11_opy_:
          bstack11ll1l1l1_opy_ = {
            bstack1ll1lllll_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨಀ"): bstack1ll1lllll_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪಁ"),
            bstack1ll1lllll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ಂ"): {
              bstack1ll1lllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩಃ"): bstack1ll1lll11_opy_
            }
          }
          bstack11lll1111_opy_ = bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ಄").format(json.dumps(bstack11ll1l1l1_opy_))
          driver.execute_script(bstack11lll1111_opy_)
        if bstack1l11l_opy_:
          bstack111llll1l_opy_ = {
            bstack1ll1lllll_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ಅ"): bstack1ll1lllll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩಆ"),
            bstack1ll1lllll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಇ"): {
              bstack1ll1lllll_opy_ (u"ࠩࡧࡥࡹࡧࠧಈ"): bstack1ll1lll11_opy_ + bstack1ll1lllll_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬಉ"),
              bstack1ll1lllll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪಊ"): bstack1ll1lllll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪಋ")
            }
          }
          bstack11ll1l1l1_opy_ = {
            bstack1ll1lllll_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ಌ"): bstack1ll1lllll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ಍"),
            bstack1ll1lllll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಎ"): {
              bstack1ll1lllll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩಏ"): bstack1ll1lllll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪಐ")
            }
          }
          if bstack1l11l_opy_.status == bstack1ll1lllll_opy_ (u"ࠫࡕࡇࡓࡔࠩ಑"):
            bstack1llllll_opy_ = bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪಒ").format(json.dumps(bstack111llll1l_opy_))
            driver.execute_script(bstack1llllll_opy_)
            bstack11lll1111_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫಓ").format(json.dumps(bstack11ll1l1l1_opy_))
            driver.execute_script(bstack11lll1111_opy_)
          elif bstack1l11l_opy_.status == bstack1ll1lllll_opy_ (u"ࠧࡇࡃࡌࡐࠬಔ"):
            reason = bstack1ll1lllll_opy_ (u"ࠣࠤಕ")
            bstack1lllll11_opy_ = bstack1ll1lll11_opy_ + bstack1ll1lllll_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠪಖ")
            if bstack1l11l_opy_.message:
              reason = str(bstack1l11l_opy_.message)
              bstack1lllll11_opy_ = bstack1lllll11_opy_ + bstack1ll1lllll_opy_ (u"ࠪࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࠪಗ") + reason
            bstack111llll1l_opy_[bstack1ll1lllll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧಘ")] = {
              bstack1ll1lllll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫಙ"): bstack1ll1lllll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬಚ"),
              bstack1ll1lllll_opy_ (u"ࠧࡥࡣࡷࡥࠬಛ"): bstack1lllll11_opy_
            }
            bstack11ll1l1l1_opy_[bstack1ll1lllll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಜ")] = {
              bstack1ll1lllll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩಝ"): bstack1ll1lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪಞ"),
              bstack1ll1lllll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫಟ"): reason
            }
            bstack1llllll_opy_ = bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪಠ").format(json.dumps(bstack111llll1l_opy_))
            driver.execute_script(bstack1llllll_opy_)
            bstack11lll1111_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫಡ").format(json.dumps(bstack11ll1l1l1_opy_))
            driver.execute_script(bstack11lll1111_opy_)
  elif bstack11l1l1l11_opy_:
    try:
      data = {}
      bstack1ll1lll11_opy_ = None
      if test:
        bstack1ll1lll11_opy_ = str(test.data)
      if not bstack1llll11l_opy_ and bstack1ll1lll11_opy_:
        data[bstack1ll1lllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಢ")] = bstack1ll1lll11_opy_
      if bstack1l11l_opy_:
        if bstack1l11l_opy_.status == bstack1ll1lllll_opy_ (u"ࠨࡒࡄࡗࡘ࠭ಣ"):
          data[bstack1ll1lllll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩತ")] = bstack1ll1lllll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪಥ")
        elif bstack1l11l_opy_.status == bstack1ll1lllll_opy_ (u"ࠫࡋࡇࡉࡍࠩದ"):
          data[bstack1ll1lllll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬಧ")] = bstack1ll1lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ನ")
          if bstack1l11l_opy_.message:
            data[bstack1ll1lllll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ಩")] = str(bstack1l11l_opy_.message)
      user = CONFIG[bstack1ll1lllll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪಪ")]
      key = CONFIG[bstack1ll1lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬಫ")]
      url = bstack1ll1lllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠯ࡼࡿ࠱࡮ࡸࡵ࡮ࠨಬ").format(user, key, bstack11l1l1l11_opy_)
      headers = {
        bstack1ll1lllll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪಭ"): bstack1ll1lllll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨಮ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack11ll1l11_opy_.format(str(e)))
  if bstack1llll1l_opy_:
    bstack11l11l11l_opy_(bstack1llll1l_opy_)
  if bstack11llll1_opy_:
    bstack1lllll_opy_(bstack11llll1_opy_)
  bstack1ll11111_opy_(self, test)
def bstack11lllll11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11l1l1l_opy_
  bstack11l1l1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l11l_opy_
  bstack1l11l_opy_ = self._test
def bstack1l11llll_opy_():
  global bstack11ll1llll_opy_
  try:
    if os.path.exists(bstack11ll1llll_opy_):
      os.remove(bstack11ll1llll_opy_)
  except Exception as e:
    logger.debug(bstack1ll1lllll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩಯ") + str(e))
def bstack1lll1111_opy_():
  global bstack11ll1llll_opy_
  bstack111l111l_opy_ = {}
  try:
    if not os.path.isfile(bstack11ll1llll_opy_):
      with open(bstack11ll1llll_opy_, bstack1ll1lllll_opy_ (u"ࠧࡸࠩರ")):
        pass
      with open(bstack11ll1llll_opy_, bstack1ll1lllll_opy_ (u"ࠣࡹ࠮ࠦಱ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack11ll1llll_opy_):
      bstack111l111l_opy_ = json.load(open(bstack11ll1llll_opy_, bstack1ll1lllll_opy_ (u"ࠩࡵࡦࠬಲ")))
  except Exception as e:
    logger.debug(bstack1ll1lllll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬಳ") + str(e))
  finally:
    return bstack111l111l_opy_
def bstack1ll1llll1_opy_(platform_index, item_index):
  global bstack11ll1llll_opy_
  try:
    bstack111l111l_opy_ = bstack1lll1111_opy_()
    bstack111l111l_opy_[item_index] = platform_index
    with open(bstack11ll1llll_opy_, bstack1ll1lllll_opy_ (u"ࠦࡼ࠱ࠢ಴")) as outfile:
      json.dump(bstack111l111l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll1lllll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪವ") + str(e))
def bstack1ll1ll1ll_opy_(bstack11ll1l11l_opy_):
  global CONFIG
  bstack1lll11l_opy_ = bstack1ll1lllll_opy_ (u"࠭ࠧಶ")
  if not bstack1ll1lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪಷ") in CONFIG:
    logger.info(bstack1ll1lllll_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬಸ"))
  try:
    platform = CONFIG[bstack1ll1lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬಹ")][bstack11ll1l11l_opy_]
    if bstack1ll1lllll_opy_ (u"ࠪࡳࡸ࠭಺") in platform:
      bstack1lll11l_opy_ += str(platform[bstack1ll1lllll_opy_ (u"ࠫࡴࡹࠧ಻")]) + bstack1ll1lllll_opy_ (u"ࠬ࠲ࠠࠨ಼")
    if bstack1ll1lllll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩಽ") in platform:
      bstack1lll11l_opy_ += str(platform[bstack1ll1lllll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪಾ")]) + bstack1ll1lllll_opy_ (u"ࠨ࠮ࠣࠫಿ")
    if bstack1ll1lllll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ೀ") in platform:
      bstack1lll11l_opy_ += str(platform[bstack1ll1lllll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧು")]) + bstack1ll1lllll_opy_ (u"ࠫ࠱ࠦࠧೂ")
    if bstack1ll1lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧೃ") in platform:
      bstack1lll11l_opy_ += str(platform[bstack1ll1lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨೄ")]) + bstack1ll1lllll_opy_ (u"ࠧ࠭ࠢࠪ೅")
    if bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ೆ") in platform:
      bstack1lll11l_opy_ += str(platform[bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧೇ")]) + bstack1ll1lllll_opy_ (u"ࠪ࠰ࠥ࠭ೈ")
    if bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ೉") in platform:
      bstack1lll11l_opy_ += str(platform[bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ೊ")]) + bstack1ll1lllll_opy_ (u"࠭ࠬࠡࠩೋ")
  except Exception as e:
    logger.debug(bstack1ll1lllll_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴࠧೌ") + str(e))
  finally:
    if bstack1lll11l_opy_[len(bstack1lll11l_opy_) - 2:] == bstack1ll1lllll_opy_ (u"ࠨ࠮್ࠣࠫ"):
      bstack1lll11l_opy_ = bstack1lll11l_opy_[:-2]
    return bstack1lll11l_opy_
def bstack11llllll_opy_(path, bstack1lll11l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1ll1l1ll_opy_ = ET.parse(path)
    bstack1l11_opy_ = bstack1ll1l1ll_opy_.getroot()
    bstack1lll11l1l_opy_ = None
    for suite in bstack1l11_opy_.iter(bstack1ll1lllll_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ೎")):
      if bstack1ll1lllll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ೏") in suite.attrib:
        suite.attrib[bstack1ll1lllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೐")] += bstack1ll1lllll_opy_ (u"ࠬࠦࠧ೑") + bstack1lll11l_opy_
        bstack1lll11l1l_opy_ = suite
    bstack11l11llll_opy_ = None
    for robot in bstack1l11_opy_.iter(bstack1ll1lllll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ೒")):
      bstack11l11llll_opy_ = robot
    bstack1l111l11_opy_ = len(bstack11l11llll_opy_.findall(bstack1ll1lllll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭೓")))
    if bstack1l111l11_opy_ == 1:
      bstack11l11llll_opy_.remove(bstack11l11llll_opy_.findall(bstack1ll1lllll_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ೔"))[0])
      bstack1ll11ll_opy_ = ET.Element(bstack1ll1lllll_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨೕ"), attrib={bstack1ll1lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨೖ"):bstack1ll1lllll_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫ೗"), bstack1ll1lllll_opy_ (u"ࠬ࡯ࡤࠨ೘"):bstack1ll1lllll_opy_ (u"࠭ࡳ࠱ࠩ೙")})
      bstack11l11llll_opy_.insert(1, bstack1ll11ll_opy_)
      bstack1lllllll_opy_ = None
      for suite in bstack11l11llll_opy_.iter(bstack1ll1lllll_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭೚")):
        bstack1lllllll_opy_ = suite
      bstack1lllllll_opy_.append(bstack1lll11l1l_opy_)
      bstack11ll11ll1_opy_ = None
      for status in bstack1lll11l1l_opy_.iter(bstack1ll1lllll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ೛")):
        bstack11ll11ll1_opy_ = status
      bstack1lllllll_opy_.append(bstack11ll11ll1_opy_)
    bstack1ll1l1ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll1lllll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧ೜") + str(e))
def bstack11l1lllll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack111ll1_opy_
  global CONFIG
  if bstack1ll1lllll_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢೝ") in options:
    del options[bstack1ll1lllll_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣೞ")]
  bstack11ll1ll11_opy_ = bstack1lll1111_opy_()
  for bstack1l1ll1lll_opy_ in bstack11ll1ll11_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1ll1lllll_opy_ (u"ࠬࡶࡡࡣࡱࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠬ೟"), str(bstack1l1ll1lll_opy_), bstack1ll1lllll_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪೠ"))
    bstack11llllll_opy_(path, bstack1ll1ll1ll_opy_(bstack11ll1ll11_opy_[bstack1l1ll1lll_opy_]))
  bstack1l11llll_opy_()
  return bstack111ll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11ll_opy_(self, ff_profile_dir):
  global bstack1l1ll_opy_
  if not ff_profile_dir:
    return None
  return bstack1l1ll_opy_(self, ff_profile_dir)
def bstack1l1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack111l1l111_opy_
  bstack1l1l1l_opy_ = []
  if bstack1ll1lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪೡ") in CONFIG:
    bstack1l1l1l_opy_ = CONFIG[bstack1ll1lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫೢ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll1lllll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥೣ")],
      pabot_args[bstack1ll1lllll_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦ೤")],
      argfile,
      pabot_args.get(bstack1ll1lllll_opy_ (u"ࠦ࡭࡯ࡶࡦࠤ೥")),
      pabot_args[bstack1ll1lllll_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣ೦")],
      platform[0],
      bstack111l1l111_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll1lllll_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨ೧")] or [(bstack1ll1lllll_opy_ (u"ࠢࠣ೨"), None)]
    for platform in enumerate(bstack1l1l1l_opy_)
  ]
def bstack1ll11l111_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack11lll1l1l_opy_=bstack1ll1lllll_opy_ (u"ࠨࠩ೩")):
  global bstack1l11ll11l_opy_
  self.platform_index = platform_index
  self.bstack1l11lll1_opy_ = bstack11lll1l1l_opy_
  bstack1l11ll11l_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack11l1111_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l11l11ll_opy_
  global bstack111l1_opy_
  if not bstack1ll1lllll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ೪") in item.options:
    item.options[bstack1ll1lllll_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ೫")] = []
  for v in item.options[bstack1ll1lllll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭೬")]:
    if bstack1ll1lllll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫ೭") in v:
      item.options[bstack1ll1lllll_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ೮")].remove(v)
    if bstack1ll1lllll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧ೯") in v:
      item.options[bstack1ll1lllll_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ೰")].remove(v)
  item.options[bstack1ll1lllll_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫೱ")].insert(0, bstack1ll1lllll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬೲ").format(item.platform_index))
  item.options[bstack1ll1lllll_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ೳ")].insert(0, bstack1ll1lllll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓ࠼ࡾࢁࠬ೴").format(item.bstack1l11lll1_opy_))
  if bstack111l1_opy_:
    item.options[bstack1ll1lllll_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ೵")].insert(0, bstack1ll1lllll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙࠺ࡼࡿࠪ೶").format(bstack111l1_opy_))
  return bstack1l11l11ll_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1ll11l11_opy_(command, item_index):
  global bstack111l1_opy_
  if bstack111l1_opy_:
    command[0] = command[0].replace(bstack1ll1lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ೷"), bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭೸") + str(item_index) + bstack1ll1lllll_opy_ (u"ࠪࠤࠬ೹") + bstack111l1_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1ll1lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ೺"), bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩ೻") + str(item_index), 1)
def bstack1llllll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack111l1lll_opy_
  bstack1ll11l11_opy_(command, item_index)
  return bstack111l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l111l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack111l1lll_opy_
  bstack1ll11l11_opy_(command, item_index)
  return bstack111l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1111l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack111l1lll_opy_
  bstack1ll11l11_opy_(command, item_index)
  return bstack111l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1111l11_opy_(self, runner, quiet=False, capture=True):
  global bstack1ll11l11l_opy_
  bstack1ll1ll11_opy_ = bstack1ll11l11l_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1ll1lllll_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭೼")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll1lllll_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫ೽")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll1ll11_opy_
def bstack11l11l1_opy_(self, name, context, *args):
  global bstack1ll1lll_opy_
  if name in [bstack1ll1lllll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩ೾"), bstack1ll1lllll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ೿")]:
    bstack1ll1lll_opy_(self, name, context, *args)
  if name == bstack1ll1lllll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫഀ"):
    try:
      if(not bstack1llll11l_opy_):
        bstack11ll1lll_opy_ = str(self.feature.name)
        bstack1l11111ll_opy_(context, bstack11ll1lll_opy_)
        context.browser.execute_script(bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩഁ") + json.dumps(bstack11ll1lll_opy_) + bstack1ll1lllll_opy_ (u"ࠬࢃࡽࠨം"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1ll1lllll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ഃ").format(str(e)))
  if name == bstack1ll1lllll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩഄ"):
    try:
      if not hasattr(self, bstack1ll1lllll_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪഅ")):
        self.driver_before_scenario = True
      if(not bstack1llll11l_opy_):
        scenario_name = args[0].name
        feature_name = bstack11ll1lll_opy_ = str(self.feature.name)
        bstack11ll1lll_opy_ = feature_name + bstack1ll1lllll_opy_ (u"ࠩࠣ࠱ࠥ࠭ആ") + scenario_name
        if self.driver_before_scenario:
          bstack1l11111ll_opy_(context, bstack11ll1lll_opy_)
          context.browser.execute_script(bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨഇ") + json.dumps(bstack11ll1lll_opy_) + bstack1ll1lllll_opy_ (u"ࠫࢂࢃࠧഈ"))
    except Exception as e:
      logger.debug(bstack1ll1lllll_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ഉ").format(str(e)))
  if name == bstack1ll1lllll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧഊ"):
    try:
      bstack1111111_opy_ = args[0].status.name
      if str(bstack1111111_opy_).lower() == bstack1ll1lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧഋ"):
        bstack111l11_opy_ = bstack1ll1lllll_opy_ (u"ࠨࠩഌ")
        bstack11l1lll1_opy_ = bstack1ll1lllll_opy_ (u"ࠩࠪ഍")
        bstack1l1l1l1ll_opy_ = bstack1ll1lllll_opy_ (u"ࠪࠫഎ")
        try:
          import traceback
          bstack111l11_opy_ = self.exception.__class__.__name__
          bstack1lll1l1l1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack11l1lll1_opy_ = bstack1ll1lllll_opy_ (u"ࠫࠥ࠭ഏ").join(bstack1lll1l1l1_opy_)
          bstack1l1l1l1ll_opy_ = bstack1lll1l1l1_opy_[-1]
        except Exception as e:
          logger.debug(bstack111l111l1_opy_.format(str(e)))
        bstack111l11_opy_ += bstack1l1l1l1ll_opy_
        bstack1l11l1111_opy_(context, json.dumps(str(args[0].name) + bstack1ll1lllll_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦഐ") + str(bstack11l1lll1_opy_)), bstack1ll1lllll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ഑"))
        if self.driver_before_scenario:
          bstack11l1llll1_opy_(context, bstack1ll1lllll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢഒ"), bstack111l11_opy_)
        context.browser.execute_script(bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ഓ") + json.dumps(str(args[0].name) + bstack1ll1lllll_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣഔ") + str(bstack11l1lll1_opy_)) + bstack1ll1lllll_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪക"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫഖ") + json.dumps(bstack1ll1lllll_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤഗ") + str(bstack111l11_opy_)) + bstack1ll1lllll_opy_ (u"࠭ࡽࡾࠩഘ"))
      else:
        bstack1l11l1111_opy_(context, bstack1ll1lllll_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣങ"), bstack1ll1lllll_opy_ (u"ࠣ࡫ࡱࡪࡴࠨച"))
        if self.driver_before_scenario:
          bstack11l1llll1_opy_(context, bstack1ll1lllll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤഛ"))
        context.browser.execute_script(bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨജ") + json.dumps(str(args[0].name) + bstack1ll1lllll_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣഝ")) + bstack1ll1lllll_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫഞ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪട"))
    except Exception as e:
      logger.debug(bstack1ll1lllll_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩഠ").format(str(e)))
  if name == bstack1ll1lllll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨഡ"):
    try:
      if context.failed is True:
        bstack1ll1ll1l1_opy_ = []
        bstack1l1l11l_opy_ = []
        bstack1ll_opy_ = []
        bstack111lll1l_opy_ = bstack1ll1lllll_opy_ (u"ࠩࠪഢ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1ll1ll1l1_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1lll1l1l1_opy_ = traceback.format_tb(exc_tb)
            bstack1llll1_opy_ = bstack1ll1lllll_opy_ (u"ࠪࠤࠬണ").join(bstack1lll1l1l1_opy_)
            bstack1l1l11l_opy_.append(bstack1llll1_opy_)
            bstack1ll_opy_.append(bstack1lll1l1l1_opy_[-1])
        except Exception as e:
          logger.debug(bstack111l111l1_opy_.format(str(e)))
        bstack111l11_opy_ = bstack1ll1lllll_opy_ (u"ࠫࠬത")
        for i in range(len(bstack1ll1ll1l1_opy_)):
          bstack111l11_opy_ += bstack1ll1ll1l1_opy_[i] + bstack1ll_opy_[i] + bstack1ll1lllll_opy_ (u"ࠬࡢ࡮ࠨഥ")
        bstack111lll1l_opy_ = bstack1ll1lllll_opy_ (u"࠭ࠠࠨദ").join(bstack1l1l11l_opy_)
        if not self.driver_before_scenario:
          bstack1l11l1111_opy_(context, bstack111lll1l_opy_, bstack1ll1lllll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨധ"))
          bstack11l1llll1_opy_(context, bstack1ll1lllll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣന"), bstack111l11_opy_)
          context.browser.execute_script(bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧഩ") + json.dumps(bstack111lll1l_opy_) + bstack1ll1lllll_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪപ"))
          context.browser.execute_script(bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫഫ") + json.dumps(bstack1ll1lllll_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥബ") + str(bstack111l11_opy_)) + bstack1ll1lllll_opy_ (u"࠭ࡽࡾࠩഭ"))
      else:
        if not self.driver_before_scenario:
          bstack1l11l1111_opy_(context, bstack1ll1lllll_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥമ") + str(self.feature.name) + bstack1ll1lllll_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥയ"), bstack1ll1lllll_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢര"))
          bstack11l1llll1_opy_(context, bstack1ll1lllll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥറ"))
          context.browser.execute_script(bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩല") + json.dumps(bstack1ll1lllll_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣള") + str(self.feature.name) + bstack1ll1lllll_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣഴ")) + bstack1ll1lllll_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭വ"))
          context.browser.execute_script(bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡳࡥࡸࡹࡥࡥࠤࢀࢁࠬശ"))
    except Exception as e:
      logger.debug(bstack1ll1lllll_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫഷ").format(str(e)))
  if name in [bstack1ll1lllll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪസ"), bstack1ll1lllll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬഹ")]:
    bstack1ll1lll_opy_(self, name, context, *args)
    if (name == bstack1ll1lllll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ഺ") and self.driver_before_scenario) or (name == bstack1ll1lllll_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ഻࠭") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack11l11l1l1_opy_(config, startdir):
  return bstack1ll1lllll_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁ഼ࠧ").format(bstack1ll1lllll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢഽ"))
class Notset:
  def __repr__(self):
    return bstack1ll1lllll_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦാ")
notset = Notset()
def bstack1l1l1llll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1lll1ll11_opy_
  if str(name).lower() == bstack1ll1lllll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪി"):
    return bstack1ll1lllll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥീ")
  else:
    return bstack1lll1ll11_opy_(self, name, default, skip)
def bstack111l1l11l_opy_(item, when):
  global bstack11lll1ll_opy_
  try:
    bstack11lll1ll_opy_(item, when)
  except Exception as e:
    pass
def bstack1l1lll1l1_opy_():
  return
def bstack111l11ll_opy_(type, name, status, reason, bstack1l1ll11l1_opy_, bstack1l1lll1_opy_):
  bstack11ll1l1l1_opy_ = {
    bstack1ll1lllll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬു"): type,
    bstack1ll1lllll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩൂ"): {}
  }
  if type == bstack1ll1lllll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩൃ"):
    bstack11ll1l1l1_opy_[bstack1ll1lllll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫൄ")][bstack1ll1lllll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ൅")] = bstack1l1ll11l1_opy_
    bstack11ll1l1l1_opy_[bstack1ll1lllll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭െ")][bstack1ll1lllll_opy_ (u"ࠫࡩࡧࡴࡢࠩേ")] = json.dumps(str(bstack1l1lll1_opy_))
  if type == bstack1ll1lllll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ൈ"):
    bstack11ll1l1l1_opy_[bstack1ll1lllll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ൉")][bstack1ll1lllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬൊ")] = name
  if type == bstack1ll1lllll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫോ"):
    bstack11ll1l1l1_opy_[bstack1ll1lllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬൌ")][bstack1ll1lllll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵ്ࠪ")] = status
    if status == bstack1ll1lllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫൎ"):
      bstack11ll1l1l1_opy_[bstack1ll1lllll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ൏")][bstack1ll1lllll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭൐")] = json.dumps(str(reason))
  bstack11lll1111_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ൑").format(json.dumps(bstack11ll1l1l1_opy_))
  return bstack11lll1111_opy_
def bstack1llll11l1_opy_(item, call, rep):
  global bstack1ll11ll11_opy_
  global bstack11ll111ll_opy_
  name = bstack1ll1lllll_opy_ (u"ࠨࠩ൒")
  try:
    if rep.when == bstack1ll1lllll_opy_ (u"ࠩࡦࡥࡱࡲࠧ൓"):
      bstack11l1l1l11_opy_ = threading.current_thread().bstack1l1lll_opy_
      try:
        name = str(rep.nodeid)
        bstack11ll1ll1l_opy_ = bstack111l11ll_opy_(bstack1ll1lllll_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫൔ"), name, bstack1ll1lllll_opy_ (u"ࠫࠬൕ"), bstack1ll1lllll_opy_ (u"ࠬ࠭ൖ"), bstack1ll1lllll_opy_ (u"࠭ࠧൗ"), bstack1ll1lllll_opy_ (u"ࠧࠨ൘"))
        for driver in bstack11ll111ll_opy_:
          if bstack11l1l1l11_opy_ == driver.session_id:
            driver.execute_script(bstack11ll1ll1l_opy_)
      except Exception as e:
        logger.debug(bstack1ll1lllll_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ൙").format(str(e)))
      try:
        status = bstack1ll1lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ൚") if rep.outcome.lower() == bstack1ll1lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ൛") else bstack1ll1lllll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ൜")
        reason = bstack1ll1lllll_opy_ (u"ࠬ࠭൝")
        if (reason != bstack1ll1lllll_opy_ (u"ࠨࠢ൞")):
          try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
          except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
          threading.current_thread().bstackTestErrorMessages.append(str(reason))
        if status == bstack1ll1lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧൟ"):
          reason = rep.longrepr.reprcrash.message
          if (not threading.current_thread().bstackTestErrorMessages):
            threading.current_thread().bstackTestErrorMessages = []
          threading.current_thread().bstackTestErrorMessages.append(reason)
        level = bstack1ll1lllll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ൠ") if status == bstack1ll1lllll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩൡ") else bstack1ll1lllll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩൢ")
        data = name + bstack1ll1lllll_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ൣ") if status == bstack1ll1lllll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ൤") else name + bstack1ll1lllll_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩ൥") + reason
        bstack1l1_opy_ = bstack111l11ll_opy_(bstack1ll1lllll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ൦"), bstack1ll1lllll_opy_ (u"ࠨࠩ൧"), bstack1ll1lllll_opy_ (u"ࠩࠪ൨"), bstack1ll1lllll_opy_ (u"ࠪࠫ൩"), level, data)
        for driver in bstack11ll111ll_opy_:
          if bstack11l1l1l11_opy_ == driver.session_id:
            driver.execute_script(bstack1l1_opy_)
      except Exception as e:
        logger.debug(bstack1ll1lllll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ൪").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll1lllll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ൫").format(str(e)))
  bstack1ll11ll11_opy_(item, call, rep)
def bstack11lll_opy_(framework_name):
  global bstack1ll1ll1l_opy_
  global bstack1111llll_opy_
  global bstack1l1ll1l1_opy_
  bstack1ll1ll1l_opy_ = framework_name
  logger.info(bstack1l111l1ll_opy_.format(bstack1ll1ll1l_opy_.split(bstack1ll1lllll_opy_ (u"࠭࠭ࠨ൬"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    Service.start = bstack11l1l1lll_opy_
    Service.stop = bstack11ll1111_opy_
    webdriver.Remote.__init__ = bstack11llll11l_opy_
    webdriver.Remote.get = bstack111lll111_opy_
    WebDriver.close = bstack1l11l1_opy_
    WebDriver.quit = bstack111ll1l1_opy_
    bstack1111llll_opy_ = True
  except Exception as e:
    pass
  bstack111l1ll_opy_()
  if not bstack1111llll_opy_:
    bstack111l1l1ll_opy_(bstack1ll1lllll_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ൭"), bstack1l1111l1l_opy_)
  if bstack1ll111111_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1ll111l1_opy_
    except Exception as e:
      logger.error(bstack11l1l11ll_opy_.format(str(e)))
  if (bstack1ll1lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൮") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11ll_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1ll1l1ll1_opy_
      except Exception as e:
        logger.warn(bstack1l111111l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1llll_opy_
      except Exception as e:
        logger.debug(bstack1l11l1l11_opy_ + str(e))
    except Exception as e:
      bstack111l1l1ll_opy_(e, bstack1l111111l_opy_)
    Output.end_test = bstack1l1ll11_opy_
    TestStatus.__init__ = bstack11lllll11_opy_
    QueueItem.__init__ = bstack1ll11l111_opy_
    pabot._create_items = bstack1l1l_opy_
    try:
      from pabot import __version__ as bstack1ll1l11l_opy_
      if version.parse(bstack1ll1l11l_opy_) >= version.parse(bstack1ll1lllll_opy_ (u"ࠩ࠵࠲࠶࠻࠮࠱ࠩ൯")):
        pabot._run = bstack1111l111_opy_
      elif version.parse(bstack1ll1l11l_opy_) >= version.parse(bstack1ll1lllll_opy_ (u"ࠪ࠶࠳࠷࠳࠯࠲ࠪ൰")):
        pabot._run = bstack1l111l11l_opy_
      else:
        pabot._run = bstack1llllll1_opy_
    except Exception as e:
      pabot._run = bstack1llllll1_opy_
    pabot._create_command_for_execution = bstack11l1111_opy_
    pabot._report_results = bstack11l1lllll_opy_
  if bstack1ll1lllll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ൱") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack111l1l1ll_opy_(e, bstack1ll1ll111_opy_)
    Runner.run_hook = bstack11l11l1_opy_
    Step.run = bstack1111l11_opy_
  if bstack1ll1lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ൲") in str(framework_name).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      from _pytest import runner
      pytest_selenium.pytest_report_header = bstack11l11l1l1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l1lll1l1_opy_
      Config.getoption = bstack1l1l1llll_opy_
      runner._update_current_test_var = bstack111l1l11l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1llll11l1_opy_
    except Exception as e:
      pass
def bstack1l1111l_opy_():
  global CONFIG
  if bstack1ll1lllll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭൳") in CONFIG and int(CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ൴")]) > 1:
    logger.warn(bstack1l1111l11_opy_)
def bstack1l1l1ll1l_opy_(arg):
  arg.append(bstack1ll1lllll_opy_ (u"ࠣ࠯࠰ࡧࡦࡶࡴࡶࡴࡨࡁࡸࡿࡳࠣ൵"))
  arg.append(bstack1ll1lllll_opy_ (u"ࠤ࠰࡛ࠧ൶"))
  arg.append(bstack1ll1lllll_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡑࡴࡪࡵ࡭ࡧࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡳࡰࡰࡴࡷࡩࡩࡀࡰࡺࡶࡨࡷࡹ࠴ࡐࡺࡶࡨࡷࡹ࡝ࡡࡳࡰ࡬ࡲ࡬ࠨ൷"))
  global CONFIG
  bstack11lll_opy_(bstack1111lllll_opy_)
  os.environ[bstack1ll1lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ൸")] = CONFIG[bstack1ll1lllll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ൹")]
  os.environ[bstack1ll1lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩൺ")] = CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪൻ")]
  from _pytest.config import main as bstack11l11lll_opy_
  bstack11l11lll_opy_(arg)
def bstack111l1111l_opy_(arg):
  bstack11lll_opy_(bstack11l111l11_opy_)
  from behave.__main__ import main as bstack111l1ll1_opy_
  bstack111l1ll1_opy_(arg)
def bstack1lll1lll_opy_():
  logger.info(bstack111l1l1l1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll1lllll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧർ"), help=bstack1ll1lllll_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪൽ"))
  parser.add_argument(bstack1ll1lllll_opy_ (u"ࠪ࠱ࡺ࠭ൾ"), bstack1ll1lllll_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨൿ"), help=bstack1ll1lllll_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ඀"))
  parser.add_argument(bstack1ll1lllll_opy_ (u"࠭࠭࡬ࠩඁ"), bstack1ll1lllll_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭ං"), help=bstack1ll1lllll_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩඃ"))
  parser.add_argument(bstack1ll1lllll_opy_ (u"ࠩ࠰ࡪࠬ඄"), bstack1ll1lllll_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨඅ"), help=bstack1ll1lllll_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪආ"))
  bstack1lll11_opy_ = parser.parse_args()
  try:
    bstack1l1l11l1_opy_ = bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩඇ")
    if bstack1lll11_opy_.framework and bstack1lll11_opy_.framework not in (bstack1ll1lllll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඈ"), bstack1ll1lllll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨඉ")):
      bstack1l1l11l1_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧඊ")
    bstack111ll11l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1l11l1_opy_)
    bstack111ll11l_opy_ = open(bstack111ll11l1_opy_, bstack1ll1lllll_opy_ (u"ࠩࡵࠫඋ"))
    bstack1llllll1l_opy_ = bstack111ll11l_opy_.read()
    bstack111ll11l_opy_.close()
    if bstack1lll11_opy_.username:
      bstack1llllll1l_opy_ = bstack1llllll1l_opy_.replace(bstack1ll1lllll_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪඌ"), bstack1lll11_opy_.username)
    if bstack1lll11_opy_.key:
      bstack1llllll1l_opy_ = bstack1llllll1l_opy_.replace(bstack1ll1lllll_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ඍ"), bstack1lll11_opy_.key)
    if bstack1lll11_opy_.framework:
      bstack1llllll1l_opy_ = bstack1llllll1l_opy_.replace(bstack1ll1lllll_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ඎ"), bstack1lll11_opy_.framework)
    file_name = bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩඏ")
    file_path = os.path.abspath(file_name)
    bstack111ll1l1l_opy_ = open(file_path, bstack1ll1lllll_opy_ (u"ࠧࡸࠩඐ"))
    bstack111ll1l1l_opy_.write(bstack1llllll1l_opy_)
    bstack111ll1l1l_opy_.close()
    logger.info(bstack111lll11_opy_)
    try:
      os.environ[bstack1ll1lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪඑ")] = bstack1lll11_opy_.framework if bstack1lll11_opy_.framework != None else bstack1ll1lllll_opy_ (u"ࠤࠥඒ")
      config = yaml.safe_load(bstack1llllll1l_opy_)
      config[bstack1ll1lllll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪඓ")] = bstack1ll1lllll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪඔ")
      bstack111l1ll11_opy_(bstack1ll1l1l_opy_, config)
    except Exception as e:
      logger.debug(bstack11lll1lll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11l1111l_opy_.format(str(e)))
def bstack111l1ll11_opy_(bstack111ll1ll1_opy_, config, bstack1l1111111_opy_ = {}):
  global bstack1l1111ll_opy_
  if not config:
    return
  bstack1ll1111l1_opy_ = bstack11l1l1l1l_opy_ if not bstack1l1111ll_opy_ else ( bstack11llll11_opy_ if bstack1ll1lllll_opy_ (u"ࠬࡧࡰࡱࠩඕ") in config else bstack111ll1ll_opy_ )
  data = {
    bstack1ll1lllll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨඖ"): config[bstack1ll1lllll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ඗")],
    bstack1ll1lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ඘"): config[bstack1ll1lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ඙")],
    bstack1ll1lllll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧක"): bstack111ll1ll1_opy_,
    bstack1ll1lllll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧඛ"): {
      bstack1ll1lllll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪග"): str(config[bstack1ll1lllll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ඝ")]) if bstack1ll1lllll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧඞ") in config else bstack1ll1lllll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤඟ"),
      bstack1ll1lllll_opy_ (u"ࠩࡵࡩ࡫࡫ࡲࡳࡧࡵࠫච"): bstackl_opy_(os.getenv(bstack1ll1lllll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧඡ"), bstack1ll1lllll_opy_ (u"ࠦࠧජ"))),
      bstack1ll1lllll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧඣ"): bstack1ll1lllll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඤ"),
      bstack1ll1lllll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨඥ"): bstack1ll1111l1_opy_,
      bstack1ll1lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫඦ"): config[bstack1ll1lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬට")]if config[bstack1ll1lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ඨ")] else bstack1ll1lllll_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧඩ"),
      bstack1ll1lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧඪ"): str(config[bstack1ll1lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨණ")]) if bstack1ll1lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩඬ") in config else bstack1ll1lllll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤත"),
      bstack1ll1lllll_opy_ (u"ࠩࡲࡷࠬථ"): sys.platform,
      bstack1ll1lllll_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬද"): socket.gethostname()
    }
  }
  update(data[bstack1ll1lllll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧධ")], bstack1l1111111_opy_)
  try:
    response = bstack1l11l1ll1_opy_(bstack1ll1lllll_opy_ (u"ࠬࡖࡏࡔࡖࠪන"), bstack1ll111l11_opy_, data, config)
    if response:
      logger.debug(bstack11lll111_opy_.format(bstack111ll1ll1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack111ll111l_opy_.format(str(e)))
def bstack1l11l1ll1_opy_(type, url, data, config):
  bstack111ll1lll_opy_ = bstack111l1lll1_opy_.format(url)
  proxies = bstack11ll1l1l_opy_(config, bstack111ll1lll_opy_)
  if type == bstack1ll1lllll_opy_ (u"࠭ࡐࡐࡕࡗࠫ඲"):
    response = requests.post(bstack111ll1lll_opy_, json=data,
                    headers={bstack1ll1lllll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ඳ"): bstack1ll1lllll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫප")}, auth=(config[bstack1ll1lllll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫඵ")], config[bstack1ll1lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭බ")]), proxies=proxies)
  return response
def bstackl_opy_(framework):
  return bstack1ll1lllll_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣභ").format(str(framework), __version__) if framework else bstack1ll1lllll_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨම").format(__version__)
def bstack11llll1l_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack11l1l1_opy_()
    logger.debug(bstack1lll1ll1l_opy_.format(str(CONFIG)))
    bstack1l1ll1ll1_opy_()
    bstack1l111ll11_opy_()
  except Exception as e:
    logger.error(bstack1ll1lllll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥඹ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11l11l11_opy_
  atexit.register(bstack1111l1l1_opy_)
  signal.signal(signal.SIGINT, bstack11lll11ll_opy_)
  signal.signal(signal.SIGTERM, bstack11lll11ll_opy_)
def bstack11l11l11_opy_(exctype, value, traceback):
  global bstack11ll111ll_opy_
  try:
    for driver in bstack11ll111ll_opy_:
      driver.execute_script(
        bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ࠮ࠣࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿ࠦࠧය") + json.dumps(bstack1ll1lllll_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦර") + str(value)) + bstack1ll1lllll_opy_ (u"ࠩࢀࢁࠬ඼"))
  except Exception:
    pass
  bstack1ll1l_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1ll1l_opy_(message = bstack1ll1lllll_opy_ (u"ࠪࠫල")):
  global CONFIG
  try:
    if message:
      bstack1l1111111_opy_ = {
        bstack1ll1lllll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ඾"): str(message)
      }
      bstack111l1ll11_opy_(bstack1111l1_opy_, CONFIG, bstack1l1111111_opy_)
    else:
      bstack111l1ll11_opy_(bstack1111l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11l11ll11_opy_.format(str(e)))
def bstack1l1l11111_opy_(bstack1llll1ll_opy_, size):
  bstack11l1_opy_ = []
  while len(bstack1llll1ll_opy_) > size:
    bstack111ll_opy_ = bstack1llll1ll_opy_[:size]
    bstack11l1_opy_.append(bstack111ll_opy_)
    bstack1llll1ll_opy_   = bstack1llll1ll_opy_[size:]
  bstack11l1_opy_.append(bstack1llll1ll_opy_)
  return bstack11l1_opy_
def bstack11ll11l1l_opy_(args):
  if bstack1ll1lllll_opy_ (u"ࠬ࠳࡭ࠨ඿") in args and bstack1ll1lllll_opy_ (u"࠭ࡰࡥࡤࠪව") in args:
    return True
  return False
def run_on_browserstack(bstack1l11ll11_opy_=None, bstack11ll1lll1_opy_=None, bstack11l111l1_opy_=False):
  global CONFIG
  global bstack1l11l1ll_opy_
  global bstack1l111l_opy_
  bstack11ll11lll_opy_ = bstack1ll1lllll_opy_ (u"ࠧࠨශ")
  if bstack1l11ll11_opy_ and isinstance(bstack1l11ll11_opy_, str):
    bstack1l11ll11_opy_ = eval(bstack1l11ll11_opy_)
  if bstack1l11ll11_opy_:
    CONFIG = bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨෂ")]
    bstack1l11l1ll_opy_ = bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪස")]
    bstack1l111l_opy_ = bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬහ")]
    bstack11ll11lll_opy_ = bstack1ll1lllll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫළ")
  if not bstack11l111l1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l11l11l_opy_)
      return
    if sys.argv[1] == bstack1ll1lllll_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨෆ")  or sys.argv[1] == bstack1ll1lllll_opy_ (u"࠭࠭ࡷࠩ෇"):
      logger.info(bstack1ll1lllll_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧ෈").format(__version__))
      return
    if sys.argv[1] == bstack1ll1lllll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ෉"):
      bstack1lll1lll_opy_()
      return
  args = sys.argv
  bstack11llll1l_opy_()
  global bstack11ll11_opy_
  global bstack1l111l1l1_opy_
  global bstack1ll11ll1l_opy_
  global bstack111ll111_opy_
  global bstack111l1l111_opy_
  global bstack111l1_opy_
  global bstack11lll11l1_opy_
  global bstack1l1ll1l1_opy_
  if not bstack11ll11lll_opy_:
    if args[1] == bstack1ll1lllll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯්ࠩ") or args[1] == bstack1ll1lllll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫ෋"):
      bstack11ll11lll_opy_ = bstack1ll1lllll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ෌")
      args = args[2:]
    elif args[1] == bstack1ll1lllll_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ෍"):
      bstack11ll11lll_opy_ = bstack1ll1lllll_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ෎")
      args = args[2:]
    elif args[1] == bstack1ll1lllll_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ා"):
      bstack11ll11lll_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧැ")
      args = args[2:]
    elif args[1] == bstack1ll1lllll_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪෑ"):
      bstack11ll11lll_opy_ = bstack1ll1lllll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫි")
      args = args[2:]
    elif args[1] == bstack1ll1lllll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫී"):
      bstack11ll11lll_opy_ = bstack1ll1lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬු")
      args = args[2:]
    elif args[1] == bstack1ll1lllll_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෕"):
      bstack11ll11lll_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧූ")
      args = args[2:]
    else:
      if not bstack1ll1lllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ෗") in CONFIG or str(CONFIG[bstack1ll1lllll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬෘ")]).lower() in [bstack1ll1lllll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪෙ"), bstack1ll1lllll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬේ")]:
        bstack11ll11lll_opy_ = bstack1ll1lllll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬෛ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1lllll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩො")]).lower() == bstack1ll1lllll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ෝ"):
        bstack11ll11lll_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧෞ")
        args = args[1:]
      elif str(CONFIG[bstack1ll1lllll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬෟ")]).lower() == bstack1ll1lllll_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ෠"):
        bstack11ll11lll_opy_ = bstack1ll1lllll_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ෡")
        args = args[1:]
      elif str(CONFIG[bstack1ll1lllll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ෢")]).lower() == bstack1ll1lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෣"):
        bstack11ll11lll_opy_ = bstack1ll1lllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ෤")
        args = args[1:]
      elif str(CONFIG[bstack1ll1lllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ෥")]).lower() == bstack1ll1lllll_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ෦"):
        bstack11ll11lll_opy_ = bstack1ll1lllll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෧")
        args = args[1:]
      else:
        os.environ[bstack1ll1lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭෨")] = bstack11ll11lll_opy_
        bstack1ll11l1l_opy_(bstack11ll11l1_opy_)
  global bstack1111_opy_
  if bstack1l11ll11_opy_:
    try:
      os.environ[bstack1ll1lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ෩")] = bstack11ll11lll_opy_
      bstack111l1ll11_opy_(bstack1111l11l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack11l11ll11_opy_.format(str(e)))
  global bstack1l1lll111_opy_
  global bstack1l11lllll_opy_
  global bstack1ll11111_opy_
  global bstack1lllll_opy_
  global bstack11l11l11l_opy_
  global bstack11l1l1l_opy_
  global bstack1l1ll_opy_
  global bstack111l1lll_opy_
  global bstack1l11ll11l_opy_
  global bstack1l11l11ll_opy_
  global bstack1ll1l1111_opy_
  global bstack1ll1lll_opy_
  global bstack1ll11l11l_opy_
  global bstack111_opy_
  global bstack1ll1_opy_
  global bstack1lll1ll11_opy_
  global bstack11lll1ll_opy_
  global bstack111ll1_opy_
  global bstack1ll11ll11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l1lll111_opy_ = webdriver.Remote.__init__
    bstack1l11lllll_opy_ = WebDriver.quit
    bstack1ll1l1111_opy_ = WebDriver.close
    bstack111_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1111_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack1l111_opy_():
    if bstack1ll1111ll_opy_() < version.parse(bstack1l1lllll1_opy_):
      logger.error(bstack1ll1llll_opy_.format(bstack1ll1111ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1ll1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11l1l11ll_opy_.format(str(e)))
  if bstack11ll11lll_opy_ != bstack1ll1lllll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭෪") or (bstack11ll11lll_opy_ == bstack1ll1lllll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ෫") and not bstack1l11ll11_opy_):
    bstack1ll1l11_opy_()
  if (bstack11ll11lll_opy_ in [bstack1ll1lllll_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ෬"), bstack1ll1lllll_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ෭"), bstack1ll1lllll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ෮")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11ll_opy_
        bstack11l11l11l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l111111l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1lllll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l11l1l11_opy_ + str(e))
    except Exception as e:
      bstack111l1l1ll_opy_(e, bstack1l111111l_opy_)
    if bstack11ll11lll_opy_ != bstack1ll1lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ෯"):
      bstack1l11llll_opy_()
    bstack1ll11111_opy_ = Output.end_test
    bstack11l1l1l_opy_ = TestStatus.__init__
    bstack111l1lll_opy_ = pabot._run
    bstack1l11ll11l_opy_ = QueueItem.__init__
    bstack1l11l11ll_opy_ = pabot._create_command_for_execution
    bstack111ll1_opy_ = pabot._report_results
  if bstack11ll11lll_opy_ == bstack1ll1lllll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ෰"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack111l1l1ll_opy_(e, bstack1ll1ll111_opy_)
    bstack1ll1lll_opy_ = Runner.run_hook
    bstack1ll11l11l_opy_ = Step.run
  if bstack11ll11lll_opy_ == bstack1ll1lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෱"):
    try:
      from _pytest.config import Config
      bstack1lll1ll11_opy_ = Config.getoption
      from _pytest import runner
      bstack11lll1ll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l1l111ll_opy_)
    try:
      from pytest_bdd import reporting
      bstack1ll11ll11_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll1lllll_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨෲ"))
  if bstack11ll11lll_opy_ == bstack1ll1lllll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨෳ"):
    bstack1l111l1l1_opy_ = True
    if bstack1l11ll11_opy_ and bstack11l111l1_opy_:
      bstack111l1l111_opy_ = CONFIG.get(bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭෴"), {}).get(bstack1ll1lllll_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ෵"))
      bstack11lll_opy_(bstack1ll1ll1_opy_)
    elif bstack1l11ll11_opy_:
      bstack111l1l111_opy_ = CONFIG.get(bstack1ll1lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ෶"), {}).get(bstack1ll1lllll_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ෷"))
      global bstack11ll111ll_opy_
      try:
        if bstack11ll11l1l_opy_(bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෸")]) and multiprocessing.current_process().name == bstack1ll1lllll_opy_ (u"ࠧ࠱ࠩ෹"):
          bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ෺")].remove(bstack1ll1lllll_opy_ (u"ࠩ࠰ࡱࠬ෻"))
          bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෼")].remove(bstack1ll1lllll_opy_ (u"ࠫࡵࡪࡢࠨ෽"))
          bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෾")] = bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෿")][0]
          with open(bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ฀")], bstack1ll1lllll_opy_ (u"ࠨࡴࠪก")) as f:
            bstack1111llll1_opy_ = f.read()
          bstack11l111l1l_opy_ = bstack1ll1lllll_opy_ (u"ࠤࠥࠦ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯ࠥ࡯࡭ࡱࡱࡵࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥ࠼ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩ࠭ࢁࡽࠪ࠽ࠣࡪࡷࡵ࡭ࠡࡲࡧࡦࠥ࡯࡭ࡱࡱࡵࡸࠥࡖࡤࡣ࠽ࠣࡳ࡬ࡥࡤࡣࠢࡀࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭࠾ࠎࡩ࡫ࡦࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠬࡸ࡫࡬ࡧ࠮ࠣࡥࡷ࡭ࠬࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡂࠦ࠰ࠪ࠼ࠍࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࡢࡴࡪࠤࡂࠦࡳࡵࡴࠫ࡭ࡳࡺࠨࡢࡴࡪ࠭࠰࠷࠰ࠪࠌࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡢࡵࠣࡩ࠿ࠐࠠࠡࠢࠣࡴࡦࡹࡳࠋࠢࠣࡳ࡬ࡥࡤࡣࠪࡶࡩࡱ࡬ࠬࡢࡴࡪ࠰ࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠩࠋࡒࡧࡦ࠳ࡪ࡯ࡠࡤࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨข").format(str(bstack1l11ll11_opy_))
          bstack1l1llll11_opy_ = bstack11l111l1l_opy_ + bstack1111llll1_opy_
          bstack111l11ll1_opy_ = bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ฃ")] + bstack1ll1lllll_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡺࡥ࡮ࡲ࠱ࡴࡾ࠭ค")
          with open(bstack111l11ll1_opy_, bstack1ll1lllll_opy_ (u"ࠬࡽࠧฅ")):
            pass
          with open(bstack111l11ll1_opy_, bstack1ll1lllll_opy_ (u"ࠨࡷࠬࠤฆ")) as f:
            f.write(bstack1l1llll11_opy_)
          import subprocess
          bstack11l11ll1l_opy_ = subprocess.run([bstack1ll1lllll_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢง"), bstack111l11ll1_opy_])
          if os.path.exists(bstack111l11ll1_opy_):
            os.unlink(bstack111l11ll1_opy_)
          os._exit(bstack11l11ll1l_opy_.returncode)
        else:
          if bstack11ll11l1l_opy_(bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫจ")]):
            bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬฉ")].remove(bstack1ll1lllll_opy_ (u"ࠪ࠱ࡲ࠭ช"))
            bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧซ")].remove(bstack1ll1lllll_opy_ (u"ࠬࡶࡤࡣࠩฌ"))
            bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩญ")] = bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪฎ")][0]
          bstack11lll_opy_(bstack1ll1ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫฏ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1ll1lllll_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫฐ")] = bstack1ll1lllll_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬฑ")
          mod_globals[bstack1ll1lllll_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭ฒ")] = os.path.abspath(bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨณ")])
          exec(open(bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩด")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll1lllll_opy_ (u"ࠧࡄࡣࡸ࡫࡭ࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠧต").format(str(e)))
          for driver in bstack11ll111ll_opy_:
            bstack11ll1lll1_opy_.append({
              bstack1ll1lllll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ถ"): bstack1l11ll11_opy_[bstack1ll1lllll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬท")],
              bstack1ll1lllll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩธ"): str(e),
              bstack1ll1lllll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪน"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡦࡢ࡫࡯ࡩࡩࠨࠬࠡࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠤࠬบ") + json.dumps(bstack1ll1lllll_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤป") + str(e)) + bstack1ll1lllll_opy_ (u"ࠧࡾࡿࠪผ"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11ll111ll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      bstack1l111ll_opy_()
      bstack1l1111l_opy_()
      bstack11l1l_opy_ = {
        bstack1ll1lllll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫฝ"): args[0],
        bstack1ll1lllll_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩพ"): CONFIG,
        bstack1ll1lllll_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫฟ"): bstack1l11l1ll_opy_,
        bstack1ll1lllll_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ภ"): bstack1l111l_opy_
      }
      if bstack1ll1lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨม") in CONFIG:
        bstack1l1l1ll1_opy_ = []
        manager = multiprocessing.Manager()
        bstack11lll1_opy_ = manager.list()
        if bstack11ll11l1l_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1ll1lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩย")]):
            if index == 0:
              bstack11l1l_opy_[bstack1ll1lllll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪร")] = args
            bstack1l1l1ll1_opy_.append(multiprocessing.Process(name=str(index),
                                          target=run_on_browserstack, args=(bstack11l1l_opy_, bstack11lll1_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1ll1lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫฤ")]):
            bstack1l1l1ll1_opy_.append(multiprocessing.Process(name=str(index),
                                          target=run_on_browserstack, args=(bstack11l1l_opy_, bstack11lll1_opy_)))
        for t in bstack1l1l1ll1_opy_:
          t.start()
        for t in bstack1l1l1ll1_opy_:
          t.join()
        bstack11lll11l1_opy_ = list(bstack11lll1_opy_)
      else:
        if bstack11ll11l1l_opy_(args):
          bstack11l1l_opy_[bstack1ll1lllll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬล")] = args
          test = multiprocessing.Process(name=str(0),
                                        target=run_on_browserstack, args=(bstack11l1l_opy_,))
          test.start()
          test.join()
        else:
          bstack11lll_opy_(bstack1ll1ll1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1ll1lllll_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬฦ")] = bstack1ll1lllll_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ว")
          mod_globals[bstack1ll1lllll_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧศ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11ll11lll_opy_ == bstack1ll1lllll_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬษ") or bstack11ll11lll_opy_ == bstack1ll1lllll_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ส"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack111l1l1ll_opy_(e, bstack1l111111l_opy_)
    bstack1l111ll_opy_()
    bstack11lll_opy_(bstack11l1ll1l1_opy_)
    if bstack1ll1lllll_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ห") in args:
      i = args.index(bstack1ll1lllll_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧฬ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack11ll11_opy_))
    args.insert(0, str(bstack1ll1lllll_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨอ")))
    pabot.main(args)
  elif bstack11ll11lll_opy_ == bstack1ll1lllll_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬฮ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack111l1l1ll_opy_(e, bstack1l111111l_opy_)
    for a in args:
      if bstack1ll1lllll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫฯ") in a:
        bstack111ll111_opy_ = int(a.split(bstack1ll1lllll_opy_ (u"࠭࠺ࠨะ"))[1])
      if bstack1ll1lllll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫั") in a:
        bstack111l1l111_opy_ = str(a.split(bstack1ll1lllll_opy_ (u"ࠨ࠼ࠪา"))[1])
      if bstack1ll1lllll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔࠩำ") in a:
        bstack111l1_opy_ = str(a.split(bstack1ll1lllll_opy_ (u"ࠪ࠾ࠬิ"))[1])
    bstack111lll1l1_opy_ = None
    if bstack1ll1lllll_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪี") in args:
      i = args.index(bstack1ll1lllll_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫึ"))
      args.pop(i)
      bstack111lll1l1_opy_ = args.pop(i)
    if bstack111lll1l1_opy_ is not None:
      global bstack1l1l11ll_opy_
      bstack1l1l11ll_opy_ = bstack111lll1l1_opy_
    bstack11lll_opy_(bstack11l1ll1l1_opy_)
    run_cli(args)
  elif bstack11ll11lll_opy_ == bstack1ll1lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ื"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      from _pytest import runner
      import importlib
      bstack1ll11l_opy_ = importlib.find_loader(bstack1ll1lllll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ุࠩ"))
    except Exception as e:
      logger.warn(e, bstack1l1l111ll_opy_)
    bstack1l111ll_opy_()
    try:
      if bstack1ll1lllll_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴูࠪ") in args:
        i = args.index(bstack1ll1lllll_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵฺࠫ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1ll1lllll_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭฻") in args:
        i = args.index(bstack1ll1lllll_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧ฼"))
        args.pop(i+1)
        args.pop(i)
      if bstack1ll1lllll_opy_ (u"ࠬ࠳ࡰࠨ฽") in args:
        i = args.index(bstack1ll1lllll_opy_ (u"࠭࠭ࡱࠩ฾"))
        args.pop(i+1)
        args.pop(i)
      if bstack1ll1lllll_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ฿") in args:
        i = args.index(bstack1ll1lllll_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩเ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1ll1lllll_opy_ (u"ࠩ࠰ࡲࠬแ") in args:
        i = args.index(bstack1ll1lllll_opy_ (u"ࠪ࠱ࡳ࠭โ"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack1111ll_opy_ = config.args
    bstack1ll1ll_opy_ = config.invocation_params.args
    bstack1ll1ll_opy_ = list(bstack1ll1ll_opy_)
    bstack1111l1l_opy_ = [os.path.normpath(item) for item in bstack1111ll_opy_]
    bstack1l111111_opy_ = [os.path.normpath(item) for item in bstack1ll1ll_opy_]
    bstack1l1ll1ll_opy_ = [item for item in bstack1l111111_opy_ if item not in bstack1111l1l_opy_]
    if bstack1ll1lllll_opy_ (u"ࠫ࠲࠳ࡣࡢࡥ࡫ࡩ࠲ࡩ࡬ࡦࡣࡵࠫใ") not in bstack1l1ll1ll_opy_:
      bstack1l1ll1ll_opy_.append(bstack1ll1lllll_opy_ (u"ࠬ࠳࠭ࡤࡣࡦ࡬ࡪ࠳ࡣ࡭ࡧࡤࡶࠬไ"))
    import platform as pf
    if pf.system().lower() == bstack1ll1lllll_opy_ (u"࠭ࡷࡪࡰࡧࡳࡼࡹࠧๅ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1111ll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l11ll1ll_opy_)))
                    for bstack1l11ll1ll_opy_ in bstack1111ll_opy_]
    if (bstack1llll11l_opy_):
      bstack1l1ll1ll_opy_.append(bstack1ll1lllll_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫๆ"))
      bstack1l1ll1ll_opy_.append(bstack1ll1lllll_opy_ (u"ࠨࡖࡵࡹࡪ࠭็"))
    try:
      from pytest_bdd import reporting
      bstack1l1ll1l1_opy_ = True
    except Exception as e:
      pass
    if (not bstack1l1ll1l1_opy_):
      bstack1l1ll1ll_opy_.append(bstack1ll1lllll_opy_ (u"ࠩ࠰ࡴ่ࠬ"))
      bstack1l1ll1ll_opy_.append(bstack1ll1lllll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨ้"))
    bstack1l1ll1ll_opy_.append(bstack1ll1lllll_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ๊࠭"))
    bstack1l1ll1ll_opy_.append(bstack1ll1lllll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩ๋ࠬ"))
    bstack1111ll11_opy_ = []
    for spec in bstack1111ll_opy_:
      bstack1111l1ll_opy_ = []
      bstack1111l1ll_opy_.append(spec)
      bstack1111l1ll_opy_ += bstack1l1ll1ll_opy_
      bstack1111ll11_opy_.append(bstack1111l1ll_opy_)
    bstack1ll11ll1l_opy_ = True
    bstack1llllllll_opy_ = 1
    if bstack1ll1lllll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭์") in CONFIG:
      bstack1llllllll_opy_ = CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧํ")]
    bstack111111l_opy_ = int(bstack1llllllll_opy_)*int(len(CONFIG[bstack1ll1lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ๎")]))
    execution_items = []
    for bstack1111l1ll_opy_ in bstack1111ll11_opy_:
      for index, _ in enumerate(CONFIG[bstack1ll1lllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ๏")]):
        item = {}
        item[bstack1ll1lllll_opy_ (u"ࠪࡥࡷ࡭ࠧ๐")] = bstack1111l1ll_opy_
        item[bstack1ll1lllll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ๑")] = index
        execution_items.append(item)
    bstack1llll1lll_opy_ = bstack1l1l11111_opy_(execution_items, bstack111111l_opy_)
    for execution_item in bstack1llll1lll_opy_:
      bstack1l1l1ll1_opy_ = []
      for item in execution_item:
        bstack1l1l1ll1_opy_.append(bstack1l1l1l1l1_opy_(name=str(item[bstack1ll1lllll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ๒")]),
                                            target=bstack1l1l1ll1l_opy_,
                                            args=(item[bstack1ll1lllll_opy_ (u"࠭ࡡࡳࡩࠪ๓")],)))
      for t in bstack1l1l1ll1_opy_:
        t.start()
      for t in bstack1l1l1ll1_opy_:
        t.join()
  elif bstack11ll11lll_opy_ == bstack1ll1lllll_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ๔"):
    try:
      from behave.__main__ import main as bstack111l1ll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack111l1l1ll_opy_(e, bstack1ll1ll111_opy_)
    bstack1l111ll_opy_()
    bstack1ll11ll1l_opy_ = True
    bstack1llllllll_opy_ = 1
    if bstack1ll1lllll_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ๕") in CONFIG:
      bstack1llllllll_opy_ = CONFIG[bstack1ll1lllll_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ๖")]
    bstack111111l_opy_ = int(bstack1llllllll_opy_)*int(len(CONFIG[bstack1ll1lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭๗")]))
    config = Configuration(args)
    bstack1111lll_opy_ = config.paths
    if len(bstack1111lll_opy_) == 0:
      import glob
      pattern = bstack1ll1lllll_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪ๘")
      bstack1lll111ll_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1lll111ll_opy_)
      config = Configuration(args)
      bstack1111lll_opy_ = config.paths
    bstack1111ll_opy_ = [os.path.normpath(item) for item in bstack1111lll_opy_]
    bstack1lll1lll1_opy_ = [os.path.normpath(item) for item in args]
    bstack1111ll1_opy_ = [item for item in bstack1lll1lll1_opy_ if item not in bstack1111ll_opy_]
    import platform as pf
    if pf.system().lower() == bstack1ll1lllll_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭๙"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1111ll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l11ll1ll_opy_)))
                    for bstack1l11ll1ll_opy_ in bstack1111ll_opy_]
    bstack1111ll11_opy_ = []
    for spec in bstack1111ll_opy_:
      bstack1111l1ll_opy_ = []
      bstack1111l1ll_opy_ += bstack1111ll1_opy_
      bstack1111l1ll_opy_.append(spec)
      bstack1111ll11_opy_.append(bstack1111l1ll_opy_)
    execution_items = []
    for bstack1111l1ll_opy_ in bstack1111ll11_opy_:
      for index, _ in enumerate(CONFIG[bstack1ll1lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ๚")]):
        item = {}
        item[bstack1ll1lllll_opy_ (u"ࠧࡢࡴࡪࠫ๛")] = bstack1ll1lllll_opy_ (u"ࠨࠢࠪ๜").join(bstack1111l1ll_opy_)
        item[bstack1ll1lllll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ๝")] = index
        execution_items.append(item)
    bstack1llll1lll_opy_ = bstack1l1l11111_opy_(execution_items, bstack111111l_opy_)
    for execution_item in bstack1llll1lll_opy_:
      bstack1l1l1ll1_opy_ = []
      for item in execution_item:
        bstack1l1l1ll1_opy_.append(bstack1l1l1l1l1_opy_(name=str(item[bstack1ll1lllll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ๞")]),
                                            target=bstack111l1111l_opy_,
                                            args=(item[bstack1ll1lllll_opy_ (u"ࠫࡦࡸࡧࠨ๟")],)))
      for t in bstack1l1l1ll1_opy_:
        t.start()
      for t in bstack1l1l1ll1_opy_:
        t.join()
  else:
    bstack1ll11l1l_opy_(bstack11ll11l1_opy_)
  if not bstack1l11ll11_opy_:
    bstack1l1llll_opy_()
def browserstack_initialize(bstack1l1l11lll_opy_=None):
  run_on_browserstack(bstack1l1l11lll_opy_, None, True)
def bstack1l1llll_opy_():
  [bstack11l11111_opy_, bstack11lllll_opy_] = bstack1l1l1l111_opy_()
  if bstack11l11111_opy_ is not None and bstack11l1l111l_opy_() != -1:
    sessions = bstack1l1l1l1_opy_(bstack11l11111_opy_)
    bstack1lllll1ll_opy_(sessions, bstack11lllll_opy_)
def bstack11l11lll1_opy_(bstack11l111ll1_opy_):
    if bstack11l111ll1_opy_:
        return bstack11l111ll1_opy_.capitalize()
    else:
        return bstack11l111ll1_opy_
def bstack1lll111l1_opy_(bstack11ll1ll_opy_):
    if bstack1ll1lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ๠") in bstack11ll1ll_opy_ and bstack11ll1ll_opy_[bstack1ll1lllll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ๡")] != bstack1ll1lllll_opy_ (u"ࠧࠨ๢"):
        return bstack11ll1ll_opy_[bstack1ll1lllll_opy_ (u"ࠨࡰࡤࡱࡪ࠭๣")]
    else:
        bstack1ll1lll11_opy_ = bstack1ll1lllll_opy_ (u"ࠤࠥ๤")
        if bstack1ll1lllll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ๥") in bstack11ll1ll_opy_ and bstack11ll1ll_opy_[bstack1ll1lllll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ๦")] != None:
            bstack1ll1lll11_opy_ += bstack11ll1ll_opy_[bstack1ll1lllll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ๧")] + bstack1ll1lllll_opy_ (u"ࠨࠬࠡࠤ๨")
            if bstack11ll1ll_opy_[bstack1ll1lllll_opy_ (u"ࠧࡰࡵࠪ๩")] == bstack1ll1lllll_opy_ (u"ࠣ࡫ࡲࡷࠧ๪"):
                bstack1ll1lll11_opy_ += bstack1ll1lllll_opy_ (u"ࠤ࡬ࡓࡘࠦࠢ๫")
            bstack1ll1lll11_opy_ += (bstack11ll1ll_opy_[bstack1ll1lllll_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ๬")] or bstack1ll1lllll_opy_ (u"ࠫࠬ๭"))
            return bstack1ll1lll11_opy_
        else:
            bstack1ll1lll11_opy_ += bstack11l11lll1_opy_(bstack11ll1ll_opy_[bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭๮")]) + bstack1ll1lllll_opy_ (u"ࠨࠠࠣ๯") + (bstack11ll1ll_opy_[bstack1ll1lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ๰")] or bstack1ll1lllll_opy_ (u"ࠨࠩ๱")) + bstack1ll1lllll_opy_ (u"ࠤ࠯ࠤࠧ๲")
            if bstack11ll1ll_opy_[bstack1ll1lllll_opy_ (u"ࠪࡳࡸ࠭๳")] == bstack1ll1lllll_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧ๴"):
                bstack1ll1lll11_opy_ += bstack1ll1lllll_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥ๵")
            bstack1ll1lll11_opy_ += bstack11ll1ll_opy_[bstack1ll1lllll_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ๶")] or bstack1ll1lllll_opy_ (u"ࠧࠨ๷")
            return bstack1ll1lll11_opy_
def bstack1lll1ll1_opy_(bstack111l11l11_opy_):
    if bstack111l11l11_opy_ == bstack1ll1lllll_opy_ (u"ࠣࡦࡲࡲࡪࠨ๸"):
        return bstack1ll1lllll_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ๹")
    elif bstack111l11l11_opy_ == bstack1ll1lllll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ๺"):
        return bstack1ll1lllll_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๻")
    elif bstack111l11l11_opy_ == bstack1ll1lllll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ๼"):
        return bstack1ll1lllll_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭๽")
    elif bstack111l11l11_opy_ == bstack1ll1lllll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ๾"):
        return bstack1ll1lllll_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ๿")
    elif bstack111l11l11_opy_ == bstack1ll1lllll_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ຀"):
        return bstack1ll1lllll_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨກ")
    elif bstack111l11l11_opy_ == bstack1ll1lllll_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧຂ"):
        return bstack1ll1lllll_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭຃")
    else:
        return bstack1ll1lllll_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࠪຄ")+bstack11l11lll1_opy_(bstack111l11l11_opy_)+bstack1ll1lllll_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭຅")
def bstack11ll1l1ll_opy_(session):
    return bstack1ll1lllll_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨຆ").format(session[bstack1ll1lllll_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ງ")],bstack1lll111l1_opy_(session), bstack1lll1ll1_opy_(session[bstack1ll1lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩຈ")]), bstack1lll1ll1_opy_(session[bstack1ll1lllll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫຉ")]), bstack11l11lll1_opy_(session[bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ຊ")] or session[bstack1ll1lllll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭຋")] or bstack1ll1lllll_opy_ (u"ࠧࠨຌ")) + bstack1ll1lllll_opy_ (u"ࠣࠢࠥຍ") + (session[bstack1ll1lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫຎ")] or bstack1ll1lllll_opy_ (u"ࠪࠫຏ")), session[bstack1ll1lllll_opy_ (u"ࠫࡴࡹࠧຐ")] + bstack1ll1lllll_opy_ (u"ࠧࠦࠢຑ") + session[bstack1ll1lllll_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪຒ")], session[bstack1ll1lllll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩຓ")] or bstack1ll1lllll_opy_ (u"ࠨࠩດ"), session[bstack1ll1lllll_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ຕ")] if session[bstack1ll1lllll_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧຖ")] else bstack1ll1lllll_opy_ (u"ࠫࠬທ"))
def bstack1lllll1ll_opy_(sessions, bstack11lllll_opy_):
  try:
    bstack1111l_opy_ = bstack1ll1lllll_opy_ (u"ࠧࠨຘ")
    if not os.path.exists(bstack1l1ll1l_opy_):
      os.mkdir(bstack1l1ll1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1lllll_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫນ")), bstack1ll1lllll_opy_ (u"ࠧࡳࠩບ")) as f:
      bstack1111l_opy_ = f.read()
    bstack1111l_opy_ = bstack1111l_opy_.replace(bstack1ll1lllll_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁࠬປ"), str(len(sessions)))
    bstack1111l_opy_ = bstack1111l_opy_.replace(bstack1ll1lllll_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩຜ"), bstack11lllll_opy_)
    bstack1111l_opy_ = bstack1111l_opy_.replace(bstack1ll1lllll_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫຝ"), sessions[0].get(bstack1ll1lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨພ")) if sessions[0] else bstack1ll1lllll_opy_ (u"ࠬ࠭ຟ"))
    with open(os.path.join(bstack1l1ll1l_opy_, bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪຠ")), bstack1ll1lllll_opy_ (u"ࠧࡸࠩມ")) as stream:
      stream.write(bstack1111l_opy_.split(bstack1ll1lllll_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬຢ"))[0])
      for session in sessions:
        stream.write(bstack11ll1l1ll_opy_(session))
      stream.write(bstack1111l_opy_.split(bstack1ll1lllll_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ຣ"))[1])
    logger.info(bstack1ll1lllll_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭຤").format(bstack1l1ll1l_opy_));
  except Exception as e:
    logger.debug(bstack1l11lll11_opy_.format(str(e)))
def bstack1l1l1l1_opy_(bstack11l11111_opy_):
  global CONFIG
  try:
    host = bstack1ll1lllll_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧລ") if bstack1ll1lllll_opy_ (u"ࠬࡧࡰࡱࠩ຦") in CONFIG else bstack1ll1lllll_opy_ (u"࠭ࡡࡱ࡫ࠪວ")
    user = CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩຨ")]
    key = CONFIG[bstack1ll1lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫຩ")]
    bstack1l1l1111l_opy_ = bstack1ll1lllll_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨສ") if bstack1ll1lllll_opy_ (u"ࠪࡥࡵࡶࠧຫ") in CONFIG else bstack1ll1lllll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ຬ")
    url = bstack1ll1lllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠳ࡰࡳࡰࡰࠪອ").format(user, key, host, bstack1l1l1111l_opy_, bstack11l11111_opy_)
    headers = {
      bstack1ll1lllll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬຮ"): bstack1ll1lllll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪຯ"),
    }
    proxies = bstack11ll1l1l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1ll1lllll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ະ")], response.json()))
  except Exception as e:
    logger.debug(bstack1ll11111l_opy_.format(str(e)))
def bstack1l1l1l111_opy_():
  global CONFIG
  try:
    if bstack1ll1lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬັ") in CONFIG:
      host = bstack1ll1lllll_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭າ") if bstack1ll1lllll_opy_ (u"ࠫࡦࡶࡰࠨຳ") in CONFIG else bstack1ll1lllll_opy_ (u"ࠬࡧࡰࡪࠩິ")
      user = CONFIG[bstack1ll1lllll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨີ")]
      key = CONFIG[bstack1ll1lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪຶ")]
      bstack1l1l1111l_opy_ = bstack1ll1lllll_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧື") if bstack1ll1lllll_opy_ (u"ࠩࡤࡴࡵຸ࠭") in CONFIG else bstack1ll1lllll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩູࠬ")
      url = bstack1ll1lllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱ຺ࠫ").format(user, key, host, bstack1l1l1111l_opy_)
      headers = {
        bstack1ll1lllll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫົ"): bstack1ll1lllll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩຼ"),
      }
      if bstack1ll1lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩຽ") in CONFIG:
        params = {bstack1ll1lllll_opy_ (u"ࠨࡰࡤࡱࡪ࠭຾"):CONFIG[bstack1ll1lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ຿")], bstack1ll1lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ເ"):CONFIG[bstack1ll1lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ແ")]}
      else:
        params = {bstack1ll1lllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪໂ"):CONFIG[bstack1ll1lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩໃ")]}
      proxies = bstack11ll1l1l_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack111ll1l11_opy_ = response.json()[0][bstack1ll1lllll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪໄ")]
        if bstack111ll1l11_opy_:
          bstack11lllll_opy_ = bstack111ll1l11_opy_[bstack1ll1lllll_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬ໅")].split(bstack1ll1lllll_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨໆ"))[0] + bstack1ll1lllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ࠫ໇") + bstack111ll1l11_opy_[bstack1ll1lllll_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪ່ࠧ")]
          logger.info(bstack1lllll11l_opy_.format(bstack11lllll_opy_))
          bstack1ll11l1ll_opy_ = CONFIG[bstack1ll1lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ້")]
          if bstack1ll1lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ໊") in CONFIG:
            bstack1ll11l1ll_opy_ += bstack1ll1lllll_opy_ (u"໋ࠧࠡࠩ") + CONFIG[bstack1ll1lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ໌")]
          if bstack1ll11l1ll_opy_!= bstack111ll1l11_opy_[bstack1ll1lllll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧໍ")]:
            logger.debug(bstack1lll1ll_opy_.format(bstack111ll1l11_opy_[bstack1ll1lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨ໎")], bstack1ll11l1ll_opy_))
          return [bstack111ll1l11_opy_[bstack1ll1lllll_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ໏")], bstack11lllll_opy_]
    else:
      logger.warn(bstack11ll1l111_opy_)
  except Exception as e:
    logger.debug(bstack11ll111_opy_.format(str(e)))
  return [None, None]
def bstack1lll1l11l_opy_(url, bstack1lll1llll_opy_=False):
  global CONFIG
  global bstack1l11ll111_opy_
  if not bstack1l11ll111_opy_:
    hostname = bstack11l1l11l_opy_(url)
    is_private = bstack1l_opy_(hostname)
    if (bstack1ll1lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ໐") in CONFIG and not CONFIG[bstack1ll1lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ໑")]) and (is_private or bstack1lll1llll_opy_):
      bstack1l11ll111_opy_ = hostname
def bstack11l1l11l_opy_(url):
  return urlparse(url).hostname
def bstack1l_opy_(hostname):
  for bstack111llll_opy_ in bstack11l1llll_opy_:
    regex = re.compile(bstack111llll_opy_)
    if regex.match(hostname):
      return True
  return False