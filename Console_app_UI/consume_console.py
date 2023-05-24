import requests


class App:
    def get_info(self):
        print("Connecting to the account web service for registration procedures")
        self.username = input("username: ")
        self.email = input("email: ")
        self.name = input("name: ")
        self.surname = input("surname: ")
        self.password = input("password: ")
        self.repassword = input("repassword: ")

    def registration(self):
        # API'ye POST isteği gönder
        url = "http://127.0.0.1:8001/api/accounts/register/"

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "password": self.password,
            "repassword": self.repassword,
        }
        response = requests.post(url, json=data, headers=headers)

        # İsteğin durumunu kontrol et
        if response.status_code == 201:
            print("Success: Registrated")
            print(response.text)
        else:
            print("Failed: Unregistrated")
            print(response.text)


app = App()
app.get_info()
app.registration()