import PySimpleGUI as sg
import sympy
import WindowMaker
import MATH

window = WindowMaker.PrimeW()

while True:
    event, values = window.read()
    # ВЫХОД ИЗ ПРОГРАММЫ
    if event == sg.WINDOW_CLOSED:
        break
    # Кнопка возвращения в самое первое окно
    if event == 'Menu' or event == 'Menu1':
        window.close()
        window = WindowMaker.PrimeW()
    # Нажатие кнопки OK при создании простых чисел
    if event == '-OkPrime-':
        SimpleSize = values['-SimpleSize-']
        if SimpleSize not in (16, 32, 64, 128, 256, 512, 1024, 2048):
            sg.popup_error('Некорректные данные')
        else:
            p = 0
            q = 0
            # Случайные целые простые числа
            while not sympy.isprime(p):
                p = sympy.randprime(2 ** (SimpleSize - 1), (2 ** SimpleSize) - 1)
            while not sympy.isprime(q):
                q = sympy.randprime(2 ** (SimpleSize - 1), (2 ** SimpleSize) - 1)
            # Произведение простых чисел
            n = p * q
            window.close()
            window = WindowMaker.OpenEW()
    # Нажатие кнопки OK при создании открытой экспоненты
    if event == '-OkOpenE-':
        OpenE = values['-OpenE-']
        if OpenE not in (3, 5, 17, 257, 65537):
            sg.popup_error('Некорректные данные')
        else:
            # Вычисляется функция Эйлера
            FuncEil = (p - 1) * (q - 1)
            m, a, d = MATH.extended_gcd(FuncEil, OpenE)
            if m != 1:
                sg.popup_error('Выберите другую открытую Экспоненту')
            else:
                window.close()
                window = WindowMaker.KeySavingW()
    # Сохранение ключей
    if event == "-SubmitKeySaving-":
        if any((values['-new_public_key-'] == '', values['-new_private_key-'] == '')):
            sg.popup_error('Некорректный ввод данных')
        else:
            with open(values[0], "w") as f:
                f.write("RSAPublicKey ::= SEQUENCE {" + "\n")
                f.write("            modulus " + str(n) + ",\n")
                f.write("            publicExponent " + str(OpenE) + "\n")
                f.write("}")
            with open(values[1], "w") as f:
                f.write("RSAPrivateKey ::= SEQUENCE {" + "\n")
                f.write("            modulus " + str(n) + ",\n")
                f.write("            publicExponent " + str(OpenE) + ",\n")
                f.write("            privateExponent " + str(d) + ",\n")
                f.write("            prime1 " + str(p) + ",\n")
                f.write("            prime2 " + str(q) + ",\n")
                f.write("}")
                window.close()
                window = WindowMaker.KeySuccessSavingW()
        # Запуск шифрования
    # Кнопка Crypt/DeCrypt
    if event == 'Crypt/DeCrypt':
        window.close()
        window = WindowMaker.CryptDecrypt()
    # Запуск шифрования
    if event == "Submit":
        # Проверка на указание всех значений
        if values["-FileCryptingRADIO-"]:
            if any((values['-public_key_IN-'] == '', values['-file_IN-'] == '')):
                sg.popup_error('Некорректный ввод данных')
            else:
                # Читаем файл открытого ключа и переносим значение в переменную pubKey
                with open(values['-file_IN-']) as f:
                    text = f.read()
                with open(values['-public_key_IN-']) as f:
                    # Находим строку с modulus и выписываем все, что есть после. split удаляет всё, что после запятой
                    keytext = f.read()
                    pubkey = " ".join(keytext.lower().split("modulus")[1:]).split(',', 1)[0].strip()
                    E = " ".join(keytext.lower().split("publicexponent")[1:]).split('\n', 1)[0].strip()
                    del keytext
                try:
                    pubkey = int(pubkey)
                    E = int(E)
                except ValueError:
                    sg.popup_error("Файл открытого ключа поврежден!")
                else:
                    listletter = [ord(ch) for ch in text]
                    PubkeyLEN = len(str(pubkey))
                    crypttext = list()
                    for i in listletter:
                        cryptletter = str(pow(i, E, pubkey))
                        nullencounter = (PubkeyLEN - len(cryptletter)) * "0"
                        crypttext.append(nullencounter + cryptletter)
                    # Костылем сделал добавление файла в ту же папку, что и исходный текст
                    filename = values['-file_IN-'].split("/")[-1]
                    filename_CRYPTED = filename.replace(".", "_CRYPTED.")
                    filepath = values['-file_IN-'].split("/")
                    filepath.pop(-1)
                    filepath = "/".join(filepath) + "/" + filename_CRYPTED
                    with open(filepath, "w+") as file:
                        file.write('EncryptedData :: = SEQUENCE {' + '\n')
                        file.write('contentType text' + '\n')
                        file.write('contentEncryptionAlgorithmIdentifier rsaEncryption' + '\n')
                        file.write('encryptedContent ')
                        file.writelines(crypttext)
                        file.write('\n' + '         }')

                    sg.popup_ok("Файл успешно зашифрован")
        else:
            if any((values['-public_key_IN-'] == '', values['-printed_file_in-'] == '')):
                sg.popup_error('Некорректный ввод данных')
            else:
                # Читаем файл открытого ключа и переносим значение в переменную pubKey
                text = values['-printed_file_in-']
                with open(values['-public_key_IN-']) as f:
                    # Находим строку с modulus и выписываем все, что есть после. split удаляет всё, что после запятой
                    keytext = f.read()
                    pubkey = " ".join(keytext.lower().split("modulus")[1:]).split(',', 1)[0].strip()
                    E = " ".join(keytext.lower().split("publicexponent")[1:]).split('\n', 1)[0].strip()
                    del keytext
                try:
                    pubkey = int(pubkey)
                    E = int(E)
                except ValueError:
                    sg.popup_error("Файл открытого ключа поврежден!")
                else:
                    listletter = [ord(ch) for ch in text]
                    PubkeyLEN = len(str(pubkey))
                    crypttext = list()
                    for i in listletter:
                        cryptletter = str(pow(i, E, pubkey))
                        nullencounter = (PubkeyLEN - len(cryptletter)) * "0"
                        crypttext.append(nullencounter + cryptletter)
                    filepath = sg.popup_get_folder('Выберите папку:', no_titlebar=True, grab_anywhere=True)
                    filename = sg.popup_get_text('Напишите название файла(без .txt):', no_titlebar=True, grab_anywhere=True) + '.txt'
                    filename_CRYPTED = filename.replace(".", "_CRYPTED.")
                    filepath = filepath + "/" + filename_CRYPTED
                    with open(filepath, "w+") as file:
                        file.write('EncryptedData :: = SEQUENCE {' + '\n')
                        file.write('contentType text' + '\n')
                        file.write('contentEncryptionAlgorithmIdentifier rsaEncryption' + '\n')
                        file.write('encryptedContent ')
                        file.writelines(crypttext)
                        file.write('\n' + '         }')

                    sg.popup_ok("Файл успешно зашифрован")
    # Запуск дешифрования
    if event == "-DSubmit-":
        if any((values['-Crypted_file_IN-'] == '', values['-private_key_IN-'] == '')):
            sg.popup_error('Некорректный ввод данных')
        else:
            with open(values['-Crypted_file_IN-']) as f:
                keytext = f.read()
                text = " ".join(keytext.lower().split("encryptedcontent")[1:]).split('\n', 1)[0].strip()
            with open(values['-private_key_IN-']) as f:
                # Находим строку с modulus и выписываем все, что есть после. split удаляет всё, что после запятой
                keytext = f.read()
                pubkey = " ".join(keytext.lower().split("modulus")[1:]).split(',', 1)[0].strip()
                privatekey = " ".join(keytext.lower().split("privateexponent")[1:]).split(',', 3)[0].strip()
                del keytext
            if text == '':
                sg.popup_error('Некорректный формат файлов!')
            else:
                try:
                    pubkey = int(pubkey)
                    privatekey = int(privatekey)
                    x = len(str(pubkey))
                    listletter = [int(text[y - x:y]) for y in range(x, len(text) + x, x)]
                except ValueError:
                    sg.popup_error("Некорректный формат файлов!")
                else:
                    x = len(str(pubkey))
                    listletter = [int(text[y - x:y]) for y in range(x, len(text) + x, x)]
                    filename = values['-Crypted_file_IN-'].split("/")[-1]
                    filename_DECRYPTED = filename.replace("_CRYPTED.", "_DECRYPTED.")
                    filepath = values['-Crypted_file_IN-'].split("/")
                    filepath.pop(-1)
                    filepath = "/".join(filepath) + "/" + filename_DECRYPTED
                    with open(filepath, "w+", encoding="utf-8") as file:
                        for i in listletter:
                            listletter = chr(pow(i, privatekey, pubkey))
                            file.write(listletter)
                    sg.popup_ok("Файл успешно расшифрован")
