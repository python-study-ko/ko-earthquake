# 구글에서 취득한 영문 주소를 국문 주소로 변환 하기 위한 코드입니다.
# 개발 : https://github.com/MaseKor

import requests
from bs4 import BeautifulSoup

url ='https://www.google.co.kr/search?q='

def trans_ad(ad_en):
    """
    영문주소를 입력하면 구글에 검색한뒤 bs4로 주소만 크롤해줍니다.
    :param ad_en: 영문 주소
    :return: 튜플 ( 성공여부, 결과 메시지) ; 성공시: 0, 실패시: 1
    """
    sourcecode = requests.get(url + ad_en)
    try:
        plaintext = sourcecode.text
        soup = BeautifulSoup(plaintext, "html.parser")
        ad_ko = soup.find_all('b')[1].contents[0]
    except Exception as e:
        return (0,"영문주소 변환에 실패 했습니다.")
    return (1,ad_ko)
