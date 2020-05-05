'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-05 19:09:42
@LastEditors: feliciaren
@LastEditTime: 2020-05-05 19:52:49
'''
import pytest
from server.search.basic_search import BasicSearch


class TestBasicSearch:

    def test_init(self):
        search = BasicSearch()
        assert(search.__class__==BasicSearch)
