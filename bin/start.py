#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.service.Service import *
from bin.service.Html_service import *
from bin.until import Path
from tornado.options import define, options
import threading

P = Path.getInstance()
define("port", default=8002, help="run on the given port", type=int)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r"/service", Service),
                  (r"/index.html", index),
                  (r"/main.html", main),
                  (r"/interface_statistics.html", interface_statistics),
                  (r"/line_test.html", line_test)
                  ],
        template_path=P.htmlPath,
        static_path=P.webPath,
        debug=False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
