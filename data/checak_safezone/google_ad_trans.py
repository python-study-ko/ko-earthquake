# 구글에서 취득한 영문 주소를 국문 주소로 변환 하기 위한 코드입니다.
# 개발 : https://github.com/MaseKor

import requests
from bs4 import BeautifulSoup

url ='https://www.google.co.kr/search?q='
data = '45 Sannyang-gil, Ganggyeong-eup, Nonsan, Chungcheongnam-do, South Korea'

sourcecode = requests.get(url + data)
plaintext = sourcecode.text
soup = BeautifulSoup(plaintext, "html.parser")

test = soup.find_all('b')[1].contents

print(test)