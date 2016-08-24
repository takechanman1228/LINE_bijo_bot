import requests
from PIL import Image
# from io import StringIO
import io
# from StringIO import StringIO
# import Image

LINEBOT_API_EVENT ='https://trialbot-api.line.me/v1/events'
LINEBOT_API_EVENT = 'https://trialbot-api.line.me/v1/bot/message/'
LINE_HEADERS = {
    'Content-type': 'application/json; charset=UTF-8',
    'X-Line-ChannelID':'1469904360', # Channel ID
    'X-Line-ChannelSecret':'cadb3352a866e7811c1a5d8d655e3f91', # Channel secre
    'X-Line-Trusted-User-With-ACL':'u48d6abf59024909b4a3eae290539188e' # MID (of Channel)
}
binary_img_response=requests.get('https://trialbot-api.line.me/v1/bot/message/4803763273444/content', headers=LINE_HEADERS)

# f = open("write.txt","w")
# f.write(binary_img_response.text)
# f.close()
# i = Image.open(StringIO(binary_img_response.content))
# Image.save()
# print()
# im = Image.fromstring('L', (100, 50), text)

# image = Image.open(binary_img_response.text)
# image = Image.open(StringIO(binary_img_response.content))
# image = Image.frombuffer('L', (100, 50), binary_img_response.text)
# image.show()
# image.save('img.jpg', 'JPEG', quality=100, optimize=True)

tempBuff = io.StringIO()
tempBuff.write(binary_img_response.text)
tempBuff.seek(0)
img=Image.open(tempBuff)
img.save('img.jpg', 'JPEG', quality=100, optimize=True)

#
# print(type(binary_img_response.text))
# stream = io.StringIO(binary_img_response.text)
# image = Image.open(stream)
image.save('img.jpg', 'JPEG', quality=100, optimize=True)
