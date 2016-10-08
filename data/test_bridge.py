from data.bridge import Bridge

# 테스트 파일
testDB = Bridge("ini_sample.json")



print(testDB.path)
print(testDB.tables)
