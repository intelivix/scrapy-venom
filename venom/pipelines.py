
class PipelineAllowedMixin(object):

    def get_pipeline_name(self):
        return self.__class__.__name__

    def pipeline_is_allowed(self, spider):
        pipeline_name = self.get_pipeline_name()
        try:
            spider_pipelines = spider.pipelines_allowed
            return pipeline_name in spider_pipelines
        except AttributeError:
            return True


class ItemAllowedMixin(object):

    def item_is_allowed(self, item):
        try:
            for item_allowed in self.items_allowed:
                if isinstance(item, item_allowed):
                    return True
            return False
        except AttributeError:
            return True


class Pipeline(PipelineAllowedMixin, ItemAllowedMixin):

    def item_pipeline(self, item, spider):
        raise NotImplementedError(
            'Pipeline requires an item_pipeline method.')

    def pre_item_pipeline(self, item, spider):
        pass

    def pos_item_pipeline(self, item, spider):
        pass

    def process_item(self, item, spider):

        if not self.pipeline_is_allowed(spider):
            return item

        if not self.item_is_allowed(item):
            return item

        self.pre_item_pipeline(item, spider)
        item = self.item_pipeline(item, spider)
        self.pos_item_pipeline(item, spider)

        return item
