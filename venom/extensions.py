# -*- coding: utf-8 -*-


class SpiderInjectExt(object):

    def process_request(self, request, spider):
        if 'spider' not in request.meta:
            newmeta = request.meta.copy()
            newmeta['spider'] = spider
            return request.replace(meta=newmeta)
