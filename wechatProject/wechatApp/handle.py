from django.template.loader import render_to_string
import sys
sys.path.append('weatherFlie')
#from getWearther import referWeather不行不知道为啥
from weatherFile.getWeather import referWeather

def main_handle(xml):
    try:
        event = xml.find('Event').text
    except:
        event = ''

    try:
        msg_type = xml.find('MsgType').text
        msg_content = xml.find('Content').text
    except:
        msg_type = ''
        msg_content = ''

    try:
        content_list = msg_content.split(' ')
    except:
        return parser_text(xml,'哇，客官的言语，让我有点迷茫。。。')

    #如果是新关注用户
    if event == 'subscribe':
        text = '嘿嘿，欢迎客官入住本店。。。'
        return parser_text(xml,text)

    if msg_type == 'text':
        if content_list[0] == ' 查询':
            if len(content_list) < 3:
                return parser_text(xml, '请客官确认格式后，再次输入。')
            else:
                if content_list[1] == '天气':
                    weather = referWeather(content_list[2:])
                    return parser_text(xml, weather)




def parser_text(xml, text):
    '''
    处理微信发来的文本数据
    返回处理过的xml
    '''
    # 我们反转发件人和收件人的消息
    fromUser = xml.find('ToUserName').text
    toUser = xml.find('FromUserName').text
    # event事件是咩有msg id 的
    try:
        message_id = xml.find('MsgId').text
    except:
        message_id = ''
    # 我们来构造需要返回的时间戳
    nowtime = str(int(time.time()))

    context = {
        'FromUserName': fromUser,
        'ToUserName': toUser,
        'Content': text,
        'time': nowtime,
        'id': message_id,
    }
    # 我们来构造需要返回的xml
    respose_xml = render_to_string('wx_text.xml', context=context)

    return respose_xml
