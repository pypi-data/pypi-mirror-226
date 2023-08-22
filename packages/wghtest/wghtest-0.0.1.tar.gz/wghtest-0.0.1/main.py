#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：
"""

class YTObject:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password


    def upload_doc(self, doc):
        """
            文档上传
        """
        url = ""
        pass

    def qa(self, question):
        """
            文档问答
        """
        url = ""

        pass


if __name__ == '__main__':
    exit(0)
