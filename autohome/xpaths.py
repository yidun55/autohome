#coding: utf-8



def xpath_sentence():
    """
    autohome的xpath语句
    """
    return {
    "urls_caricon":"//div[@class='uibox-con']//dl[@class='caricon-list']/\
        dd[position()>1]/a/@href",  #不同类型车的url view-source:http://www.autohome.com.cn/a00/
    "name_caricon":"//div[@class='uibox-con']//dl[@class='caricon-list']/\
        dd[position()>1]/a/span/text()", #不同类型车的name
    "urls_caricon_suv":"//div[@class='uibox-con']//dl[@class='caricon-list']/\
        dd[@class='caricon07']//a/@href", #不同类型SUV的url
    "name_caricon_suv":"//div[@class='uibox-con']//dl[@class='caricon-list']/\
        dd[@class='caricon07']//a/text()", #不同类型SUV的name
    "auto_ids":"//ul[@class='rank-list-ul']/li/@id",
    "type_auto":"//div[@class='subnav-title-name']/a/text()", #车型
    "brand":"//tr[@id='tr_0']/td[1]/div/text()",  #厂商--品牌
    "level":"//tr[@id='tr_1']/td[1]/div/text()",  #汽车级别分类(微型，SUV等)
    "BSX":"//tr[@id='tr_3']/td[1]/div/text()",  #变速箱分类
    "CSJG":"//tr[@id='tr_5']/td[1]/div/text()",  #车身结构
    "ZWGS":"//tr[@id='tr_24']/td[1]/div/text()",  #坐位个数
    "PL":"//tr[@id='tr_28']/td[1]/div/text()",  #排量
    "RLXS":"//tr[@id='tr_44']/td[1]/div/text()",  #燃料形式
    "QDFS":"//tr[@id='tr_53']/td[1]/div/text()",   #驱动方式
    "DDTC":"//tr[@id='tr_527']/td[1]/div/text()",  #电动天窗
    "DDTJZY":"//tr[@id='tr_557']/td[1]/div/text()", #电动调节坐椅
    "ESP":"//tr[@id='tr_517']/td[1]/div/text()", #ESP
    "XQDD":"//tr[@id='tr_578']/td[1]/div/text()",  #氙气大灯 grep
    "GPS":"//tr[@id='tr_566']/td[1]/div/text()",  #GPS
    "DSXH":"//tr[@id='tr_543']/td[1]/div/text()", #定速巡航
    "ZPZY":"//tr[@id='tr_549']/td[1]/div/text()", #真皮坐椅 grep
    "DCLD":"//tr[@id='tr_544']/td[1]/div/text()",  #倒车雷达
    "QZDKT":"//tr[@id='tr_603']/td[1]/div/text()",  #全自动空调
    "DGLFXP":"//tr[@id='tr_539']/td[1]/div/text()"   #多功能方向盘
    }

def xpath_repair():
    """
    repair_autohome的xpath语句
    """
    return {
    "type_auto":"//div[@class='subnav-title-name']/a/text()", #车型
    "brand":"//tr[@id='tr_0']/td[1]/div/text()",  #厂商--品牌
    "level":"//tr[@id='tr_1']/td[1]/div/text()",  #汽车级别分类(微型，SUV等)
    "BSX":"//tr[@id='tr_3']/td[1]/div/text()",  #变速箱分类
    "CSJG":"//tr[@id='tr_5']/td[1]/div/text()",  #车身结构
    "ZWGS":"//tr[@id='tr_19']/td[1]/div/text()",  #坐位个数
    "PL":"//tr[@id='tr_37']/td[1]/div/text()",  #排量
    "RLXS":"//tr[@id='tr_52']/td[1]/div/text()",  #燃料形式
    "QDFS":"//tr[@id='tr_27']/td[1]/div/text()",   #驱动方式
    }
