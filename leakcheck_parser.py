from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import csv
import random
import argparse


def read_emails(file_name):
    emails = []
    count = 0
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for i, line in enumerate(reader):
            emails.append(line[0].split(';')[0])
            count += 1
    return emails, count


def parser_data(file_name, rows):
    csv_file = open(file_name, 'a', newline='')
    '''
    Шапка
    '''
    writer = csv.writer(csv_file, delimiter=";")
    writer.writerow(['Email', 'Password', 'Source', 'Date'])
    for row in rows:
        splited_row = row.split()
        writer = csv.writer(csv_file, delimiter=";")
        try:
            writer.writerow([splited_row[1], splited_row[2], splited_row[3], splited_row[4]])
        except IndexError:
            writer.writerow([splited_row[1], splited_row[2], splited_row[3]])
        finally:
            continue


def login(login, password):
    driver.find_element(By.CSS_SELECTOR, '.login-button').click()

    time.sleep(3)

    driver.find_element(By.NAME, 'username').send_keys(login)
    driver.find_element(By.NAME, 'password').send_keys(password)

    driver.find_element(By.CLASS_NAME, 'btn-success').click()

    input('pass captcha and click enter ONLY WHEN YOU SEE DASHBOARD PAGE')


def leackcheck_parse(emails, count):
    result = []
    index = 1
    for email in emails:
        driver.find_element(By.NAME, 'search').clear()
        driver.find_element(By.NAME, 'search').send_keys(email)
        select_element = driver.find_element(By.NAME, 'type')
        select_object = Select(select_element)
        select_object.select_by_value('email')

        driver.find_element(By.XPATH, '//button[text()="Check"]').click()

        time.sleep(random.randint(1, 3))
        try:
            text = driver.find_element(By.XPATH, '//tbody').text
            text = text.replace('\nThis row doesn\'t contain any passwords', ' nopassword').replace('Remove my data', '').replace(':', ' ')
            # ОБЯЗАТЕЛЬНО ВТОРОЙ ПАРАМЕТР ПЕРВОГО replace С ПРОБЕЛОМ, НУЖНО ДЛЯ split()
            if text == '':
                continue
            else:
                result.append(text + '\n')
                print('=' * 50)
                print(text)
                print('=' * 50)
                driver.back()
        except:
            driver.back()
            continue
        finally:
            print(f'{index}/{count}')
            index += 1
    return result


url = 'https://leakcheck.io/dashboard'
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Парсер leackcheck с испльзованием selenium. Если в консоли парсер заедает(перестаёт работать) - нажать Enter')
    parser.add_argument('-f', '--file', type=str, required=True, help='Название csv файла. Пример, -f result.csv')
    parser.add_argument('-e', '--emails', type=str, required=True, help='Путь к csv файлу с электронным почтами')
    parser.add_argument('-l', '--login', type=str, required=False, help='Логин для leakcheck. Если не указать, то используются дефолтные креды. Вводить без кавычек')
    parser.add_argument('-p', '--password', type=str, required=False, help='Пароль для leakcheck. Если не указать, то используются дефолтные креды. Вводить без кавычек')
    parser.add_argument('-d', '--decodriver', type=str, required=True, help='Путь к декодрайверу. Пока используется только firefox')
    parser.add_argument('-b', '--browser', type=str, required=True, help='Тип браузера. {firefox, chrome}')
    args = parser.parse_args()
    try:
        if args.emails[-4:] != '.csv':
            print('Укажите файл с электронными почтами с расширением csv')
            exit(-1)
        open(args.emails, 'r')
    except FileNotFoundError:
        print('Файл с электронными почтами не найден.')
        exit(-1)
    csv_file_name = args.file.replace('\'', '').replace('\"', '')
    emails_csv_file_name = args.emails.replace('\'', '').replace('\"', '')
    if not ('csv' in csv_file_name):
        csv_file_name = csv_file_name + '.csv'

    emails, count = read_emails(emails_csv_file_name)

    if args.browser == 'chrome':
        driver = webdriver.Chrome(executable_path=args.decodriver.replace('\'', '').replace('\"', ''))
        driver.get(url)
    elif args.browser == 'firefox':
        driver = webdriver.Firefox(executable_path=args.decodriver.replace('\'', '').replace('\"', ''))
        driver.get(url)
    else:
        print('Print only valid browser')
        exit(-1)

    if args.login is None or args.password is None:
        print('write credentials')
        exit(-1)
    else:
        login(args.login.replace('\'', '').replace('\"', ''), args.password.replace('\'', '').replace('\"', ''))

    print('\n' * 2)
    print(f'Registered {count} emails')
    result = leackcheck_parse(emails, count)

    parser_data(csv_file_name, result)
    exit(0)
