# -*- coding=utf-8 -*-
'''
writer:lxshen
date:2018-1-23
E-mail:guanghui2017@outlook.com
'''

# 文件的作用就是用来写es中的数据模型的

from datetime import datetime
from elasticsearch_dsl import DocType, analyzer, \
    Completion, Text, Integer, Object, MetaField, Index, Long, Double

from elasticsearch_dsl.connections import connections


# 自定义分词器类
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

class CustomAnalyzer(_CustomAnalyzer):

    def get_analysis_definition(self):
        return {}

# 创建分析器的对象
#   filter=['lowercase]  转换大小写
ik_analyzer = CustomAnalyzer('ik_smart', filters=['lowercase'])

# 创建连接, 传入
connections.create_connection(hosts=['10.16.88.33'])



class Qianggou(DocType):
    endTime = Integer()
    progress = Integer()
    soldCount = Integer()
    startTime = Integer()
class Cp(DocType):
    condition = Text()
    count = Text()
    expired = Text()
    limit = Text()
    price = Text()
    retStatus = Text()
    sellerName = Text(store=True, analyzer="ik_smart")
    updated = Text()
    spare = Text()
    starts = Text()


class ArticleType(DocType):
    brandId = Text()
    categoryId = Long()
    commission = Double()
    consumerProtection = Text()
    cp = Object(Cp)
    cpId = Text()
    cpUrl = Text()
    cpid = Long()
    created = Long()
    dcid = Integer()
    descUrl = Text()
    dv = Double()
    flagShip = Long()
    freeExpress = Integer()
    freeExpressBack = Integer()
    gold = Long()
    historySales = Long()
    imagePath = Text()
    imagePaths = Text()
    intro = Text(store=True, analyzer="ik_smart")
    isBrand = Long()
    itemId = Text()
    itemUrl = Text()
    ju = Long()
    price = Long()
    props = Text()
    qiang = Long()
    qianggou = Object(Qianggou)
    rootCategoryId = Long()
    sellPrice = Long()
    sellerId = Text()
    sellerInfo = Text()
    shopId = Text()
    shopType = Text()
    source = Text()
    subtitle = Text()
    tags = Text(store=True, analyzer='ik_smart')
    title = Text(store=True, analyzer='ik_smart')
    updated = Long()
    viewCount = Long()
    weight = Integer()
    ymbCategoryId = Long()

    # 搜索建议
    # 不能直接指定分词器，
    suggest = Completion(analyzer=ik_analyzer)


    class Meta:
        # 索引名称
        index = 'bodao'
        # type名称
        doc_type = 'es'
        all = MetaField(enabled=True)


if __name__ == '__main__':
    job = Index('bodao')
    job.settings(
        number_of_shards=5,
        number_of_replicas=0
    )
    ik = analyzer('ik', tokenizer="ik_smart")

    job.analyzer(ik)
    job.create()

    ArticleType().init()
