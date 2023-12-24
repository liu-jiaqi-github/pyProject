#!/user/bin/env python
# !-*-coding:utf-8 -*-

# !@Time       : 2023/12/23 10:44
# !@Author     : ljq
# !@File       : 生成xml.py
# !@Software   : PyCharm
# !Description : '
from lxml.etree import Element, tostring
def main():
    root = Element("root")
    div = Element("div")
    div.text = "这是个盒子"
    root.append(div)
    a = tostring(root, encoding="utf-8", pretty_print=True).decode("utf-8")
    print(type(a))
    print(a)
if __name__ == '__main__':
    main()