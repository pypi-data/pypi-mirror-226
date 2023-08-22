"""
@Author: kang.yang
@Date: 2023/8/21 17:10
"""
import kuto
from kuto.core.android.element import AdrElem
from kuto.core.image.element import ImageElem


class ImagePage(kuto.Page):
    searchEntry = AdrElem(rid="com.tencent.mm:id/j5t")
    searchInput = AdrElem(rid="com.tencent.mm:id/cd7")
    searchResult = AdrElem(rid="com.tencent.mm:id/kpm")
    schoolEntry = ImageElem(image="../static/校园场馆.png")
