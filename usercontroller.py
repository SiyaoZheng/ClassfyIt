#!/usr/bin/env python
#coding:utf-8

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

texts = open('texts.txt','r').read().split()

from itertools import zip_longest    # zip_longest -> Python 3, izip_longest -> Python 2
chunk_list = lambda a_list, n:zip_longest(*[iter(a_list)]*n)
texts = list(chunk_list([x for x in texts], 8))
f = open('labels.txt','w')
f.write('')
f.close()


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            page = int(self.get_argument("page"))
            action_type = self.get_argument("action_type")
            if action_type == 'label':
                label = self.get_argument("label")
                text = self.get_argument("text")
                f = open('labels.txt','a')
                f.write(label + ', ' + text)
                f.write('\n')
                f.close()
                self.render("index.html",page=str(page),texts = texts[page],)
            elif action_type == 'page':
                page = int(self.get_argument("page"))
                page += 1
                self.render("index.html",texts = texts[page], page=str(page))
        except Exception as e:
            print(e)
            page = 0
            self.render("index.html",texts = texts[page],page=page)

handlers = [
    (r"/", IndexHandler)
]

template_path = os.path.join(os.path.dirname(__file__),"template")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers, template_path,debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
