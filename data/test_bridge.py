from data.bridge import Bridge

# 테스트 파일
# 할일:  윈도우에서 json 호출시 UnicodeDecodeError: 'cp949' codec can't decode byte 0xec in position 134: illegal multibyte sequence 에러 발생
testDB = Bridge("ini_sample.json")



print(testDB.path)
print(testDB.tables)
