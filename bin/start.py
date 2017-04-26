#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.service.Service import *
from bin.service.Html_service import *
from bin.until import Path
from tornado.options import define, options

P = Path.getInstance()
define("port", default=8001, help="run on the given port", type=int)

if __name__ == "__main__":
    # log = Logger()
    # log.info("日志模块消息!")

    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r"/service", Service),
                  (r"/index.html", index),
                  (r"/main.html", main),
                  (r"/interface_statistics.html", interface_statistics)
                  ],
        template_path=P.htmlPath,
        static_path=P.webPath,
        debug=False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
