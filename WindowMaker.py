import PySimpleGUI as sg


def PrimeW():
    layout = [[sg.Text("Размер случайных простых чисел 'p' и 'q':"), ],
              [sg.Combo(values=(16, 32, 64, 128, 256, 512, 1024, 2048), k='-SimpleSize-')],
              [sg.Button('Ok', k='-OkPrime-'), sg.Button('Crypt/DeCrypt')]
              ]
    window = sg.Window('RSA шифр', layout)
    return window


def OpenEW():
    layout = [[sg.Text("Выберите открытую экспоненту:")],
              [sg.Combo(values=(3, 5, 17, 257, 65537), k='-OpenE-')],
              [sg.Button('Ok', k='-OkOpenE-')]
              ]
    # Create the window
    window = sg.Window('RSA шифр', layout)
    return window


def KeySavingW():
    layout = [[sg.Text("Выберите, куда записать внешний ключ:")],
              [sg.In(), sg.FileBrowse(key='-new_public_key-', file_types=(("Text Files", "*.txt"),))],
              [sg.Text("Выберите, куда записать внутренний ключ:")],
              [sg.In(), sg.FileBrowse(key='-new_private_key-', file_types=(("Text Files", "*.txt"),))],
              [sg.Button('Submit', k="-SubmitKeySaving-")]
              ]
    # Create the window
    window = sg.Window('RSA шифр', layout)
    return window


def KeySuccessSavingW():
    layout = [[sg.Text("Ключи успешно сохранены!")],
              [sg.Button('Menu')]]
    # Create the window
    window = sg.Window('RSA шифр', layout)
    return window


def CryptDecrypt():
    # ТАБ в CryptDecrypt с шифрованием файла
    crypt_layout = [[sg.Text("Выберите открытый ключ:")],
                    [sg.In(), sg.FileBrowse(key='-public_key_IN-')],
                    [sg.Radio("Выберите файл для зашифровки:", "RADIO", default=True, key="-FileCryptingRADIO-")],
                    [sg.In(), sg.FileBrowse(key='-file_IN-')],
                    [sg.Radio("Введите текст для зашифровки:", "RADIO", default=False, key="-TextCryptingRADIO-")],
                    [sg.Multiline(key='-printed_file_in-', size=(52, 5))],
                    [sg.Button("Submit"), sg.Button("Menu")]

                    ]

    # ТАБ в CryptDecrypt с расшифрованием файла
    decrypt_layout = [[sg.Text("Выберите закрытый ключ:")],
                      [sg.In(), sg.FileBrowse(key='-private_key_IN-')],
                      [sg.Text("Выберите зашифрованный файл:")],
                      [sg.In(), sg.FileBrowse(key='-Crypted_file_IN-')],
                      [sg.VPush()],
                      [sg.Button("Submit", key="-DSubmit-"), sg.Button("Menu", key="Menu1")]
                      ]
    layout = [[sg.TabGroup(
        [[
            sg.Tab('Crypt', crypt_layout, key='-Crypt_layout-'),
            sg.Tab('DeCrypt', decrypt_layout, key='-DeCrypt_layout-'),
        ]],
        tab_location='topleft', enable_events=True, selected_title_color='white', selected_background_color='black')],
    ]

    # Create the window
    #if values["-File"]
    window = sg.Window('RSA шифр', layout)
    return window
