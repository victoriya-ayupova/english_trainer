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


# from itsdangerous import Signer
#
# signer = Signer('asdf')
# encrypted_value = signer.sign('1')
#
# signer = Signer('asdf')
# decrypted_value = signer.unsign(encrypted_value)
# print(decrypted_value)

from itsdangerous import URLSafeTimedSerializer, BadSignature


def generate_recovery_url(email: str) -> str:
    base_url = f'http://127.0.0.1/reset_password/'
    signer = URLSafeTimedSerializer(app.secret_key)
    encrypted_value = signer.dumps(1)
    return base_url + encrypted_value


# @app.get('/reset_password/<string:payload>')
# def reset_password(payload: str):
#     signer = URLSafeTimedSerializer('asdf')
#     try:
#         key, timestamp = signer.loads(payload)
#     except BadSignature:
#         return redirect(url_for('error_reset'))
#
#     if timestamp - datetime.datetime.now() > ...:
#         return redirect(url_for('error_reset'))
#
#     ...


print(generate_recovery_url('vasya@mail.ru'))
