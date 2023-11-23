# import smtplib
#
# username = 'englishtrainer312@gmail.com'
# password = 'xsil pilc jejv myic'
# host = 'smtp.gmail.com'
# port = 587
#
# connection = smtplib.SMTP(host, port)
# connection.starttls()
# connection.login(username, password)
# text = (
#     'Subject: Test subject\n'
#     f'From: TestTest <{username}>\n\n'
#     'lajfjhGVFX'
# )
#
# connection.sendmail(username, username, text)


import random

n = 10**10
nums = (random.randint(1, 2 * n) for _ in range(n))
filtered_nums = (num for num in nums if num % 2 == 0)
with open('file.txt', 'w') as file:
    for num in filtered_nums:
        file.write(f'{num} ')