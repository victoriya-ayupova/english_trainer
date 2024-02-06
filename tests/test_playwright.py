import re
from playwright.sync_api import Page, expect


def authorize(page, email='lena@mail.ru', password='123456'):
    page.goto("http://127.0.0.1:5001/auth/login")
    page.get_by_label('Email').fill(email)
    page.get_by_label('Password').fill(password)
    page.get_by_role('button', name='Войти').click()


def test_has_title(page: Page):
    page.goto("http://127.0.0.1:5001")
    page.screenshot(path='screenshot.png')
    expect(page).to_have_title(re.compile("LinguaLearn"))


def test_login(page: Page, db):
    authorize(page)
    expect(page).to_have_url('http://127.0.0.1:5001/')
    expect(page).to_have_title(re.compile("LinguaLearn - main"))


def test_incorrect_password(page: Page, db):
    authorize(page, password='12345')
    expect(page).to_have_url('http://127.0.0.1:5001/auth/login')
    expect(page.get_by_text('Неверный пароль')).to_be_visible()


def test_no_words(page: Page, db):
    authorize(page)
    expect(page.get_by_text('У вас нет слов для изучения. Загрузите текст')).to_be_visible()


def test_add_text(page: Page, db):
    authorize(page)
    page.get_by_text('Загрузить текст').click()
    expect(page).to_have_url('http://127.0.0.1:5001/main/upload')
    text = ('Everything was in confusion in the Oblonskys house. '
            'The wife had discovered that the husband was carrying on an intrigue with a French girl, '
            'who had been a governess in their family, and she had announced to her husband '
            'that she could not go on living in the same house with him.')
    page.get_by_label('Text').fill(text)
    page.get_by_role('button', name='Загрузить').click()
    expect(page.get_by_text('Текст загружен')).to_be_visible()
    expect(page).to_have_url('http://127.0.0.1:5001/')

