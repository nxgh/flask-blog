import re

# pattern = r'^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})'      

# 至少 8位, 一个小写字母，一个大写字母，一个数字,一个特殊字符[$@$!_%*?&]
# pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?_&])[A-Za-z\d$@$!_%*?&]{8,}'
# password = [
#     'P1&',
#     'Password_123',
#     'Hgxn_1102&lorem',
#     'safhewDasief@1awjk',
#     'safhewasief@awjk',
#     '12341254151234s',
#     '234wioklsaedrjirfsd34tweds',
# ]


# for i in password:
#     print(i, re.match(pattern, i))
pattern = re.compile(r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
print(pattern.search('flsel@foasfo.com'))