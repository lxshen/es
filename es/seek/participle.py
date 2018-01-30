# -*-coding:utf-8 -*-
# import sys
#
# reload(sys)
# sys.setdefaultencoding('utf-8')
from models_as.es_types import ArticleType
from elasticsearch_dsl.connections import connections
from seek import setting
import json
# 创建一个连接
es = connections.create_connection(hosts=['10.16.88.33'])


def gen_suggest(index, info_dict):
    '''
    用于分词
    :param index: 对应操作的索引
    :param info_dict: 要进行分词操作的内容（元组）
    :return: 返回分词之后的所有词汇的列表
    '''
    used_words = set()
    suggests = list()
    for text, weight in info_dict.items():
        # print text,weight
        # words = es.indices.analyze(index=index, analyzer="ik_max_word",
        #                            params={'filter': ["lowercase"]}, body=text)
        words = es.indices.analyze(index=index,params={'filter': ["lowercase"]}, body={'analyzer':"ik_max_word", 'text' :text})
        # 遍历取出所有分词，放在一个列表中
        analyzer_word = list()
        for word in words['tokens']:
            if len(word['token']) > 1:
                analyzer_word.append(word['token'])
        # 使用set去重
        analyzer_word = set(analyzer_word)
        new_words = analyzer_word - used_words
        used_words = new_words
        suggests.append({"input": list(new_words), 'weight': weight})
    return suggests


def save_es(data_tuple=None):
    bodao = ArticleType()

    bodao.brandId = '139389362'    # Text()  brandValueId
    bodao.categoryId = 50013618      # Long()  淘宝分类 categoryId
    bodao.commission = 12.00           # Double()   佣金百分比  commission
    bodao.consumerProtection = 'sfgdfjn'       # Text()    特别长的字段   feature

    bodao.cp.condition = 'dfcxvb'        # Text()  优惠券使用条件 Coupon_condition
    bodao.cp.count = 'sdfsdbcv'          # Text() 已领取张数  采集不到  默认10000
    bodao.cp.expired = 'jhghn'           # Text()     到期时间  coupon_expired
    bodao.cp.limit = 'sdfdcvbnbn'        # Text()   限领张数   默认1   limit
    bodao.cp.price = 'cvnbvb'            # Text()    优惠劵面值 coupon_price
    bodao.cp.retStatus = 'cbvnvn'        # Text()  优惠劵接口获取     retStatus

    Seller = data_tuple[1]     # todo 到时候需要看看读取数据库字段时候是字典还是json

    bodao.cp.sellerName = Seller['shopName']  # Text(ik)   店家名称 解析Seller
    bodao.cp.updated = 'dfgbcbv'        # Text()     优惠券更新时间
    bodao.cp.spare = '37'              # Text()    剩余张数   spare
    bodao.cp.starts = 'sdfsd'          # Text()     开始时间   starts

    bodao.cpUrl = 'cbnvbnvbm'            # Text()  优惠券url  coupon_url
    bodao.cpId = bodao.cpUrl.split('=')[-1]     # Text()   优惠券id  从coupon_url中解析
    bodao.cpid = 7856234523              # Long()
    bodao.created = 346786790780         # Long()   创建时间
    bodao.descUrl = 'sdfxvbbcn'          # Text()    电脑主图 taobaoDescUrl

    Feature = json.loads(bodao.consumerProtection)
    item = Feature['consumerProtection']['items']
    print(item)
    if '赠运费险' in str(item):
        bodao.freeExpress = 1  # Integer()  按是否包邮查询  分析 feature字段
    else:
        bodao.freeExpress = 0  # Integer()  按是否包邮查询  分析 feature字段

    delivery = Feature['delivery']['postage']
    if '0.00' or '免运费' or '包邮' in delivery:
        bodao.freeExpressBack = 1  # Integer()   按是否包含邮费险查询
    else:
        bodao.freeExpressBack = 0  # Integer()   按是否包含邮费险查询

    bodao.gold = 896413167               # todo Long()  是否是金牌卖家查询
    bodao.historySales = 65765345        # Long()  销量  sales
    bodao.imagePath = 'sdggdfhfgnb'      # Text()  主图 img_url
    bodao.imagePaths = 'xbtdyrtybb'      # Text()  图片集合  Images
    bodao.intro = '时尚百搭束脚牛仔裤，加绒加厚，保证不起球不褪色'    # Text(ik)  文案  intor

    bodao.isBrand = 52356457568       # Long()  todo 怎么获取品牌 返回1或0
    bodao.itemId = 'lxshen'              # Text()   商品id  item_id

    bodao.ju = 24564567                 # Long()  todo  是否参加聚划算
    bodao.price = 7686745            # Long()        券后价  price
    bodao.dv = bodao.price * bodao.commission  # Double()  真实佣金 劵后价 * 佣金百分比
    bodao.props = 'sdfgdbcvbcvb'     # Text()    产品的基本信息 props
    bodao.qiang = 454534            # Long()  todo 是否参与淘抢购

    bodao.qianggou.endTime = 54             #Integer()
    bodao.qianggou.progress = 2423         #Integer()
    bodao.qianggou.soldCount = 776     #Integer()
    bodao.qianggou.startTime = 454       #Integer()

    bodao.rootCategoryId = 50008164       # Long()   淘宝基础分类  rootCategoryId
    bodao.dcid = getDcid(str(bodao.rootCategoryId))  # Integer() 按自定义类目查询14,这个需要根据rootCategoryId进行分类
    bodao.sellPrice = 123255587       # Long()   商品原价   sell_price
    bodao.sellerId = Seller['userId']      # Text()   店家id    解析seller 中的 userId
    bodao.sellerInfo = 'sdfsgdfg'     # Text()  商品规格   seller
    bodao.shopId = Seller['shopId']         # Text()  解析 seller 中的 shopId

    bodao.shopType = Seller['shopType']      # Text()  出自淘宝，天猫 解析 shop_type 或解析 seller中的shopType

    if bodao.shopType == 'B' and '旗舰店' in bodao.bodao.cp.sellerName:
        bodao.flagShip = 'B'  # Long()    是否是旗舰店(是天猫，店铺名称里面含有’旗舰店‘)
        bodao.itemUrl = 'https://detail.tmall.com/item.htm?id=' + bodao.itemId  # Text()    商品url 根据这个商品id以及
    else:
        bodao.flagShip = 'C'
        bodao.itemUrl = 'https://item.taobao.com/item.htm?id =' + bodao.itemId  # Text()    商品url 根据这个商品id以及


    bodao.source = 'sdfsdfg'          # Text()  来至什么平台（大淘客） source
    bodao.subtitle = 'xfvb cvb'       # Text()  副标题    d_title
    bodao.tags = '请选择颜色分类 参考身高'         # Text(ik)   先不管
    bodao.title = '童装男童冬装裤子2017新款韩版'   # Text(ik)  标题 title
    bodao.updated = 144536467          # Long()   更新时间
    bodao.viewCount = 12254778678      # Long()   人气值  viewCount
    bodao.weight = 544              # Integer()    先不管
    bodao.ymbCategoryId = getYmbCategoryId(str(bodao.rootCategoryId))   # Long()  按指定类目查询11  这个需要根据rootCategoryId进行分类

    dic = {
        bodao.cp.sellerName: 9,
        bodao.intro: 8,
        bodao.tags: 7,
        bodao.title: 10,
    }
    bodao.meta.id = bodao.itemId
    bodao.suggest = gen_suggest(ArticleType._doc_type.index, dic)
    bodao.save()


def getDcid(rootCategoryId):
    if rootCategoryId in setting.Women_clothing:
        return 1
    if rootCategoryId in setting.Department:
        return 2
    if rootCategoryId in setting.Food:
        return 3
    if rootCategoryId in setting.Beautiful_outfit:
        return 4
    if rootCategoryId in setting.Shoe_bag:
        return 5
    if rootCategoryId in setting.Underwear:
        return 6
    if rootCategoryId in setting.Men_clothing:
        return 7
    if rootCategoryId in setting.Maternal_infant:
        return 8
    if rootCategoryId in setting.Digital_home_appliances:
        return 9
    if rootCategoryId in setting.Household_textile:
        return 10
    if rootCategoryId in setting.Exercise_outdoors:
        return 11
    if rootCategoryId in setting.Product_style_car:
        return 12
    if rootCategoryId in setting.Books_audio_video:
        return 13
    if rootCategoryId in setting.Other:
        return 14

def getYmbCategoryId(rootCategoryId):
    if rootCategoryId in setting.Cosmetic_personal_care_1:
        return 1
    elif rootCategoryId in setting.Women_men_wear_2:
        return 2
    elif rootCategoryId in setting.Home_building_materials_3:
        return 3
    elif rootCategoryId in setting.Food_tea_fruit_4:
        return 4
    elif rootCategoryId in setting.Digital_office_5:
        return 5
    elif rootCategoryId in setting.Medical_care_6:
        return 6
    elif rootCategoryId in setting.Maternal_child_parent_7:
        return 7
    elif rootCategoryId in setting.Accessories_shoes_bags_8:
        return 8
    elif rootCategoryId in setting.Exercise_9:
        return 9
    elif rootCategoryId in setting.Book_audio_video_10:
        return 10
    else:
        return 11

save_es()

# print(getDcid('50008164'))
# print(getYmbCategoryId('50008164'))
