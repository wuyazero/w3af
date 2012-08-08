'''
test_strange_reason.py

Copyright 2012 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''
import unittest

import core.data.kb.knowledgeBase as kb

from core.data.url.httpResponse import httpResponse
from core.data.request.fuzzableRequest import fuzzableRequest
from core.data.parsers.urlParser import url_object
from plugins.grep.strange_reason import strange_reason


class test_strange_reason(unittest.TestCase):
    
    def setUp(self):
        kb.kb.cleanup()
        self.plugin = strange_reason()
        self.url = url_object('http://www.w3af.com/')
        self.headers = {'content-type': 'text/html'}
        self.request = fuzzableRequest(self.url)

    def tearDown(self):
        self.plugin.end()
        
    def test_strange_reason_empty(self):
        response = httpResponse(200, '' , self.headers, self.url, self.url, msg='Ok')
        self.plugin.grep(self.request, response)
        self.assertEquals( len(kb.kb.getData('strange_reason', 'strange_reason')) , 0 )
    
    def test_strange_reason_large(self):
        response = httpResponse(300, 'A'*4096 , self.headers, self.url, self.url, msg='Multiple Choices')
        self.plugin.grep(self.request, response)
        self.assertEquals( len(kb.kb.getData('strange_reason', 'strange_reason')) , 0 )
    
    def test_strange_reason_found_200(self):
        response = httpResponse(200, 'A'*4096 , self.headers, self.url, self.url, msg='Foo!')
        self.plugin.grep(self.request, response)
        self.assertEquals( len(kb.kb.getData('strange_reason', 'strange_reason')) , 1 )

    def test_strange_reason_found_300(self):
        response = httpResponse(300, 'A'*2**10 , self.headers, self.url, self.url, msg='Multiple')
        self.plugin.grep(self.request, response)
        self.assertEquals( len(kb.kb.getData('strange_reason', 'strange_reason')) , 1 )
        