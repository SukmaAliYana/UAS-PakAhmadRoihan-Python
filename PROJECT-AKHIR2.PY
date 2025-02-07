import os
import json
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from datetime import datetime
import cv2

PHOTO_DIR = "absensi_photos"
DATA_FILE = "absensi_data.json"
USER_ACCOUNTS_FILE = "user_accounts.json"
USERS_FILE = "users.json"
COMPLAINTS_FILE = "complaints.json"

if not os.path.exists(COMPLAINTS_FILE):
    with open(COMPLAINTS_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(USER_ACCOUNTS_FILE):
    initial_accounts = {
        "admin": "admin123",
        "ali": "ali123",
        "dimas": "dimas123",
        "arip": "arip"
    }
    with open(USER_ACCOUNTS_FILE, "w") as f:
        json.dump(initial_accounts, f, indent=4)

def load_user_accounts():
    with open(USER_ACCOUNTS_FILE, "r") as f:
        return json.load(f)

def save_user_accounts(accounts):
    with open(USER_ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

user_accounts = load_user_accounts()

if not os.path.exists(PHOTO_DIR):
    os.makedirs(PHOTO_DIR)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump([], f)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.background_image = Image(source="/Users/mac/loginscreengitar.jpeg", allow_stretch=True, keep_ratio=False) 
        self.add_widget(self.background_image)
        
        self.add_widget(self.layout)

        self.layout.add_widget(Label(text="Login", font_size=32))
        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False)
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(Button(text="Login Guys", on_press=self.login))
        self.layout.add_widget(Button(text="Daftar Akun Baru Yok", on_press=self.daftar))

        self.error_label = Label(text="", color=(1, 0, 0, 1), font_size=14)
        self.layout.add_widget(self.error_label)

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        if username in user_accounts and user_accounts[username] == password:
            if username == "admin":
                self.manager.get_screen('admin').current_user = username
                self.manager.current = 'admin'
            else:
                user_screen = self.manager.get_screen('user')
                user_screen.current_user = username
                self.manager.current = 'user'
        else:
            Popup(title="Login Gagal", content=Label(text="Username atau password salah!"), size_hint=(0.6, 0.4)).open()
        
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)

        if username == "admin" and password == "admin123":
            self.manager.current = 'admin'
        elif username in user_accounts and user_accounts[username] == password:
            self.manager.get_screen('user').current_user = username  
            self.manager.current = 'user'
        else:
            Popup(title="Login Gagal", content=Label(text="Maaf, Password atau Username anda bukan milik Admin :D"), size_hint=(0.6, 0.4)).open()
            
        if username in user_accounts and user_accounts[username] == password:
            if username == "admin":
                self.manager.get_screen('admin').current_user = username
                self.manager.current = 'admin'
            else:
                self.manager.get_screen('user').current_user = username
                self.manager.current = 'user'

        with open(USERS_FILE, 'r') as f:
            users = json.load(f)

        self.error_label.text = "Maaf, username atau password Anda salah"

    def daftar(self, instance):
        self.manager.current = 'daftar'

class DaftarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)

        self.layout.add_widget(Label(text="Daftar Akun Baru", font_size=32))
        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False)
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(Button(text="Daftar", on_press=self.daftar_akun))
        self.layout.add_widget(Button(text="Kembali ke Login", on_press=self.kembali))

    def daftar_akun(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username and len(password) >= 4:
            with open(USERS_FILE, 'r+') as f:
                users = json.load(f)
                if any(user['username'] == username for user in users):
                    Popup(title="Pendaftaran Gagal", content=Label(text="Username sudah terdaftar!"), size_hint=(0.6, 0.4)).open()
                    return
                users.append({"username": username, "password": password})
                f.seek(0)
                json.dump(users, f, indent=4)

            Popup(title="Pendaftaran Sukses", content=Label(text="Akun berhasil didaftarkan!"), size_hint=(0.6, 0.4)).open()
            self.manager.current = 'login'
        else:
            Popup(title="Pendaftaran Gagal", content=Label(text="Username dan password tidak valid!"), size_hint=(0.6, 0.4)).open()

    def kembali(self, instance):
        self.manager.current = 'login'

class UserScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = None
        self.current_user = None
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.background_image = Image(source="/Users/mac/userscreenawan.jpeg", allow_stretch=True, keep_ratio=False) 
        self.add_widget(self.background_image)
        
        self.add_widget(self.layout)

        self.welcome_label = Label(text="", font_size=24)
        self.layout.add_widget(self.welcome_label)
        self.layout.add_widget(Button(text="Absen Sekarang", on_press=self.absen))
        self.layout.add_widget(Button(text="Riwayat Absensi", on_press=self.riwayat))
        self.layout.add_widget(Button(text="Komplain ke Admin", on_press=self.komplain))
        self.layout.add_widget(Button(text="Logout", on_press=self.logout))

    def absen(self, instance):
        AbsenPopup(username=self.current_user).open()
        
    def on_pre_enter(self, *args):
        if self.current_user:
            self.welcome_label.text = f"Hi, Selamat datang {self.current_user}!"
        else:
            self.welcome_label.text = "Hi, Selamat datang!"

    def absen(self, instance):
        AbsenPopup(username=self.current_user).open()

    def riwayat(self, instance):
        RiwayatPopup(user_mode=True, username=self.current_user).open()
            
    def komplain(self, instance):
        KomplainPopup().open()

    def logout(self, instance):
        self.manager.current = 'login'
        
class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.background_image = Image(source="/Users/mac/adminscreenkucing.jpeg", allow_stretch=True, keep_ratio=False) 
        self.add_widget(self.background_image)
        
        self.add_widget(self.layout)

        self.welcome_label = Label(text="", font_size=24)
        self.layout.add_widget(self.welcome_label)
        self.layout.add_widget(Button(text="Lihat Data Absensi", on_press=self.riwayat))
        self.layout.add_widget(Button(text="Mendaftar Akun Pengguna", on_press=self.daftar_pengguna))
        self.layout.add_widget(Button(text="Lihat Komplain Pengguna", on_press=self.lihat_komplain))
        self.layout.add_widget(Button(text="Logout", on_press=self.logout))

    def on_pre_enter(self, *args):
        if self.current_user:
            self.welcome_label.text = f"Hi, Selamat datang {self.current_user}!"
        else:
            self.welcome_label.text = "Hi, Selamat datang Admin!"
            
    def riwayat(self, instance):
        RiwayatPopup(user_mode=True, username=self.current_user).open()

    def lihat_komplain(self, instance):
        LihatKomplainPopup().open()

    def daftar_pengguna(self, instance):
        DaftarScreenAdmin().open()

    def logout(self, instance):
        self.manager.current = 'login'

class DaftarScreenAdmin(Popup):
    def __init__(self, **kwargs):
        super().__init__(title="Daftar Pengguna Baru", size_hint=(0.8, 0.8), **kwargs)
        self.content_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.add_widget(self.content_layout)
         
        self.content_layout.add_widget(Label(text="Masukkan Username Baru:"))
        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.content_layout.add_widget(self.username_input)
        
        self.content_layout.add_widget(Label(text="Masukkan Password Baru:"))
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False)
        self.content_layout.add_widget(self.password_input)

        self.content_layout.add_widget(Button(text="Simpan", on_press=self.save_user))
        self.content_layout.add_widget(Button(text="Batal", on_press=self.dismiss))
        self.content_layout.add_widget(Button(text="Daftar", on_press=self.daftar_akun))
        self.content_layout.add_widget(Button(text="Tutup", on_press=self.dismiss))

    def save_user(self, instance):
        new_username = self.username_input.text.strip()
        new_password = self.password_input.text.strip()

        if new_username and new_password:
            user_accounts[new_username] = new_password
            save_user_accounts(user_accounts)
            Popup(title="Sukses", content=Label(text="Akun baru berhasil ditambahkan!"), size_hint=(0.6, 0.4)).open()
            self.dismiss()
        else:
            Popup(title="Error", content=Label(text="Username dan password tidak boleh kosong!"), size_hint=(0.6, 0.4)).open()
    
    def daftar_akun(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username and len(password) >= 4:
            with open(USERS_FILE, 'r+') as f:
                users = json.load(f)
                if any(user['username'] == username for user in users):
                    Popup(title="Pendaftaran Gagal", content=Label(text="Username sudah terdaftar!"), size_hint=(0.6, 0.4)).open()
                    return
                users.append({"username": username, "password": password})
                f.seek(0)
                json.dump(users, f, indent=4)

            Popup(title="Pendaftaran Sukses", content=Label(text="Akun berhasil didaftarkan!"), size_hint=(0.6, 0.4)).open()
            self.dismiss()
        else:
            Popup(title="Pendaftaran Gagal", content=Label(text="Username dan password tidak valid!"), size_hint=(0.6, 0.4)).open()

class AbsenPopup(Popup):
    def __init__(self, username=None, **kwargs):
        super().__init__(title="Absen Sekarang", size_hint=(0.8, 0.8), **kwargs)
        self.username = username
        self.content = BoxLayout(orientation='vertical')
        
        self.image_preview = Image(size_hint=(1, 0.7))
        self.content.add_widget(self.image_preview)
        self.content.add_widget(Button(text="Ambil Foto", on_press=self.take_photo))
        self.content.add_widget(Button(text="Simpan dan Keluar", on_press=self.dismiss))
        self.content.add_widget(Button(text="Tutup", on_press=self.dismiss))
        
    def take_photo(self, instance):
        camera = cv2.VideoCapture(0)
        try:
            ret, frame = camera.read()
            if ret:
                filename = os.path.join(PHOTO_DIR, f"{self.username}_absen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                if os.path.exists(filename):
                    filename = filename.replace(".jpg", f"_{datetime.now().strftime('%H%M%S')}.jpg")
                cv2.imwrite(filename, frame)

                if not os.path.exists(DATA_FILE):
                    data = {}

                else:
                    with open(DATA_FILE, 'r') as f:
                        try:
                            data = json.load(f)
                        except json.JSONDecodeError:
                            data = {}
                    
                if self.username not in data:
                    data[self.username] = []

                data[self.username].append({
                    'timestamp': datetime.now().isoformat(),
                    'photo': filename,
                    'uploaded': False
                })
                
                with open(DATA_FILE, 'w') as f:
                    json.dump(data, f, indent=4)
                                    
                self.image_preview.source = filename
                self.image_preview.reload()
        except Exception as e:
            Popup(title="Error", content=Label(text=f"Error mengambil foto: {e}"), size_hint=(0.6, 0.4)).open()
        finally:
            camera.release()
            cv2.destroyAllWindows()    
    
    def absen(self, instance):
        AbsenPopup(username=self.current_user).open()
        
    def riwayat(self, instance):
        RiwayatPopup(user_mode=True, username=self.current_user).open()
        
        print(f"Username saat ini: {self.current_user}")

class KomplainPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(title="Komplain ke Admin", size_hint=(0.8, 0.6), **kwargs)
        self.content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.content.add_widget(Label(text="Tulis Komplain Anda:", font_size=10))
        self.komplain_input = TextInput(hint_text="Masukkan keluhan Anda di sini...", multiline=True)
        self.content.add_widget(self.komplain_input)

        self.content.add_widget(Button(text="Kirim Komplain", on_press=self.kirim_komplain))
        self.content.add_widget(Button(text="Tutup", on_press=self.dismiss))

    def kirim_komplain(self, instance):
        komplain = self.komplain_input.text.strip()
        if komplain:
            with open(COMPLAINTS_FILE, 'r+') as f:
                data = json.load(f)
                data.append({
                    'timestamp': datetime.now().isoformat(),
                    'complaint': komplain
                })
                f.seek(0)
                json.dump(data, f, indent=4)
            self.dismiss()
            Popup(title="Komplain Dikirim", content=Label(text="Komplain Anda berhasil dikirim ke admin."), size_hint=(0.6, 0.4)).open()
        else:
            Popup(title="Error", content=Label(text="Komplain tidak boleh kosong!"), size_hint=(0.6, 0.4)).open()

class LihatKomplainPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(title="Daftar Komplain", size_hint=(0.8, 0.8), **kwargs)
        self.content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        with open(COMPLAINTS_FILE, 'r') as f:
            data = json.load(f)
        if data:
            for entry in data:
                self.content.add_widget(Label(text=f"{entry['timestamp']}: {entry['complaint']}"))
        else:
            self.content.add_widget(Label(text="Tidak ada komplain."))

        self.content.add_widget(Button(text="Tutup", on_press=self.dismiss))

class RiwayatPopup(Popup):
    def __init__(self, user_mode=True, username=None, **kwargs):
        super().__init__(title="Riwayat Absensi", size_hint=(0.8, 0.8), **kwargs)
        self.username = username
        self.content = BoxLayout(orientation='vertical')
        
        try:
            with open (DATA_FILE, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            data = {}
            Popup(title="Error", content=Label(text=f"Kesalahan membaca data absensi: {e}"), size_hint=(0.6, 0.4)).open()
            
        if user_mode and self.username:
            absensi_user = data.get(self.username, [])
            if absensi_user:
                for entry in absensi_user:
                    self.content.add_widget(Label(text=f"{entry['timestamp']} - {os.path.basename(entry['photo'])}"))
            else:
                self.content.add_widget(Label(text="Belum ada data absensi.")) 
                      
        elif not user_mode: # Admin mode, show all users' absensi
            if data:
                for username, absensi in data.items():
                    self.content.add_widget(Label(text=f"Absensi untuk {username}:"))
                    for entry in absensi:
                        self.content.add_widget(Label(text=f"  {entry['timestamp']} - {os.path.basename(entry['photo'])}"))
            else:
                self.content.add_widget(Label(text="Tidak ada data absensi."))

        self.content.add_widget(Button(text="Tutup", on_press=self.dismiss))

class AbsenApp(App):
    def build(self):
        Window.size = (400, 600)
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DaftarScreen(name='daftar'))
        sm.add_widget(UserScreen(name='user'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm

if __name__ == '__main__': 
    try:    
        AbsenApp().run()
    except Exception as e:
        print(f"An error occurred: {e}")