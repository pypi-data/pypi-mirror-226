"""
@Author: kang.yang
@Date: 2023/8/21 17:05
"""
import kuto
from kuto.core.android.element import AdrElem
from kuto.core.ocr.element import OCRElem


class OcrPage(kuto.Page):
    searchBtn = AdrElem(rid="com.tencent.mm:id/j5t")
    searchInput = AdrElem(rid="com.tencent.mm:id/cd7")
    searchResult = AdrElem(rid="com.tencent.mm:id/kpm")
    schoolEntry = OCRElem(text="校园场馆", pos=12)
