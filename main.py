# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests as requests
from urllib3.connectionpool import xrange
from prometheus_client import Gauge
import requests
from requests_toolbelt import MultipartEncoder
import xml.etree.ElementTree as ET
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def post_file_to_wechat_get_media_id(filename, access_token):


    post_file_url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=file"

    m = MultipartEncoder(
        fields={filename: ('file', open(filename, 'rb'), 'text/plain')},
    )
    print(m)
    r = requests.post(url=post_file_url, data=m, headers={'Content-Type': m.content_type})
    print(r.text)

    return r.text['media_id']


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    xml_string = '''
    <xml>
        <ToUserName><![CDATA[wwd4c0cabaa5479e2b]]></ToUserName>
        <FromUserName><![CDATA[LiuBaiSong]]></FromUserName>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[template_card_event]]></Event>
        <CreateTime>1646539330</CreateTime>
        <AgentID>1000002</AgentID>
        <EventKey><![CDATA[button_key_1]]></EventKey>
        <TaskId><![CDATA[task0001]]></TaskId>
        <CardType><![CDATA[button_interaction]]></CardType>
        <SelectedItems>
            <SelectedItem>
            <QuestionKey><![CDATA[btn_question_key1]]></QuestionKey>
            <OptionIds>
                <OptionId><![CDATA[btn_selection_id1]]></OptionId>
            </OptionIds>
            </SelectedItem>
        </SelectedItems>
        <ResponseCode><![CDATA[vxR7PzS5OS2axDF9MdgGaZ1atXhzsSUzfjwwwESILfY]]></ResponseCode>
    </xml>
    '''
    root = ET.fromstring(xml_string)
    for username in root.findall('ResponseCode'):
        ResponseCode = username.text
    print(ResponseCode)
