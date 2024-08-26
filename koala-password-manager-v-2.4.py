import pyzipper
from os.path import exists as pe
from glob import glob as gl
from re import findall as find
from os import system as s
from os.path import getsize as gs

def accountfind():
    global account, found, n
    found = False
    print("Ось усі Ваші облікові записи:")
    try:
        f = open("list.txt", "r", encoding="utf-8")
    except FileNotFoundError:
        print("Не знайдено жодного облікового запису!")
        accnf= True #accounts not found
        return 1
    print(f.read())
    f.close()
    
    if option == "open" or option == "відкрити":
        q = "У який з них Ви хочете ввійти? "
    elif option == "delete" or option == "видалити":
        q = "Який з них Ви хочете видалити? "
    
    account = input(f"{q}")
    n = 0
    
    f = open("list.txt", "r", encoding="utf-8")
    for n, text in enumerate(f):
        if account in text:
            found = True
            break
    f.close()
    
    if not found:
        print("Обліковий запис не знайдено")
        
s("attrib -h -s *.* && color 61 ")

while True: #Основний цикл
    s("title Koala Password Manager") 
    option = input("""Виберіть функцію: create, open, delete, help exit /
створити, відкрити, видалити, допомога, вийти """)
    
    if option == "create" or option == "створити":
        account = input("Обліковий запис: ")
        data = input("Введіть ім'я користувача та/або пароль: ")
        n = 1
        while True:
            zipname = f"{n}.zip"
            txtname = f"{n}.txt"
            if not pe(zipname):
                txt_f = open(txtname, "w", encoding="utf-8")
                txt_f.write(data)
                txt_f.close()
                break
            else:
                n += 1
        
        f = open("list.txt", "a", encoding="utf-8")
        f.write(f"{account}\n")
        f.close()
        
        zf = pyzipper.AESZipFile(zipname, 'w',
                                 compression=pyzipper.ZIP_LZMA,
                                 encryption=pyzipper.WZ_AES)
        zf.setpassword(f"{account} account".encode("utf-8"))
        zf.write(txtname)
        zf.close()
        
        s(f"del {txtname}")
        print(f"Створено {zipname}")
    
    elif option == "open" or option == "відкрити":
        accountfind()
        if accountfind==1 or not found:
            continue #Перезапуск головнлго циклу
        #if found 
        zf = pyzipper.AESZipFile(f"{n+1}.zip")
        password = f"{account} account".encode("utf-8")
        zf.pwd = password
        files = zf.namelist()
        print(zf.read(files[0]).decode("utf-8"))
        zf.close()
    
    elif option == "exit" or option == "вийти":
        break #Приривання основного циклу
    
    elif option == "delete" or option == "видалити":
        accountfind()
        if found:
            rusure = input("Ви впевнені? (так/ні  y/n) ")
            if rusure == "y" or rusure == "так":
                f = open("list.txt", "r", encoding="utf-8")
                lines = f.readlines()
                f.close()
                
                fw = open("list.txt", "w", encoding="utf-8")
                for line in lines:
                    if account not in line:
                        fw.write(line)
                fw.close()
            #якщо rusure не "так" або "y", то програма повернеться до головного циколу
                s(f"del {n+1}.zip")
                #Сортування по зростанню номера архіва і якщо порядок порушено,
                #відбувається перейменування
                for n, filename in enumerate(sorted(gl("*.zip"), key=lambda x: int(find(r'\d+', x)[0])), start=1):
                    newfilename = str(n) + ".zip"
                    s(f"ren {filename} {newfilename}")
                empty= gs("list.txt")
                if empty==0:
                    s("del list.txt")
                    print("У Вас більше немає облікових записів!")
                
                print(f"Обліковий запис {account} видалено успішно!")
    elif option == "help" or option == "допомога":
        print ("""Ця програма - простий та зручний у використанні менеджер паролів.
Логіни та паролі зберігаються у текстових файлах, 
що в свою чергу знаходяться в Zip- архівах, захищених паролями.
Додатковий захист забезпечують атрибути файлів у Windows - 
Прихований та Системний.""")
        h_option = input("оберіть функцію програми, яка Вас цікавить, окрім Допомога. ")
        if h_option== "create" or h_option == "створити":
            print("""
Програма запитає у вас назву облікового запису та  дані для входу до нього.
Далі буде створено текстовий файл, в який записуються дані для входу
 у ваш обліковий запис. 
Він буде мати назву порядкового номера. 
Після цього створиться Zip-архів з таким самим іменем, 
куди додається текстовий файл. Пароль архіва - 
“назва-облікового-запису account”. 
Назва облікового запису буде додана у файл list.txt. 
Номер рядка в якому вона знаходиться відповідає номеру Zip-архіва,
в якому знаходиться пароль до облікового запису. 
Якщо щось піде не так, Вам буде потрібен сторонній архіватор 
для відкриття Zip-архівів.
""")
        elif h_option == "open" or h_option == "відкрити":
            print("""
Вам покажеться список ваших облікових записів. 
Вам треба буде вибрати один із них
 і ви відразу ж побачите дані для входу.
 Якщо облікового запису, який ви ввели немає, 
програма сповістить вас про це і знову перейде до вибору функції.
""")
        elif h_option == "delete" or h_option == "видалити":
            print("""
Ви вибираєте обліковий запис так само, як і для відкриття. 
Цього разу ви повинні підтвердити свій вибір. 
Програма  видалить обліковий запис з  файлу list.txt, 
як і сам  Zip-архів. І підкоригує нумерацію, якщо це потрібно
""")
        elif h_option == "exit" or h_option == "вийти":
            print("""
Перед виходом з програми до всіх файлів у папці, 
крім самої програми, застосуються вищезгадані атрибути.
Всі атрибути знімаються при наступному запуску програми.
""")
        else:
            print("Немає даних.")
    else:
        print("неіснуюча функція!")
s("attrib +h +s *.* && attrib -h -s *.exe")
