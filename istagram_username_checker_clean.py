import random
import string
import smtplib
import time
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class InstagramUsernameChecker:
    def _init_(self, email, email_password):
        self.email = email
        self.email_password = email_password
        self.available_usernames = []
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

    def generate_double_letter(self):
        return "".join(random.choice(string.ascii_lowercase) for _ in range(2))

    def generate_double_with_numbers(self):
        base = self.generate_double_letter()
        numbers = "".join(random.choice(string.digits) for _ in range(random.randint(1, 2)))
        return base + numbers

    def generate_triple_letter(self):
        return "".join(random.choice(string.ascii_lowercase) for _ in range(3))

    def generate_triple_with_numbers(self):
        base = self.generate_triple_letter()
        numbers = "".join(random.choice(string.digits) for _ in range(random.randint(1, 2)))
        return base + numbers

    def generate_quadruple_letter(self):
        return "".join(random.choice(string.ascii_lowercase) for _ in range(4))

    def generate_quadruple_with_numbers(self):
        base = self.generate_quadruple_letter()
        numbers = "".join(random.choice(string.digits) for _ in range(random.randint(1, 2)))
        return base + numbers

    def generate_with_symbols(self, username):
        symbols = [".", "_"]
        if random.choice([True, False]) and len(username) > 2:
            pos = random.randint(1, len(username) - 1)
            return username[:pos] + random.choice(symbols) + username[pos:]
        else:
            return username + random.choice(symbols)

    def generate_all_usernames(self, count=10):
        usernames = []

        for _ in range(count):
            username = self.generate_double_letter() if random.choice([1, 2]) == 1 else self.generate_double_with_numbers()
            if random.random() < 0.2:
                username = self.generate_with_symbols(username)
            usernames.append(username)

        for _ in range(count):
            username = self.generate_triple_letter() if random.choice([1, 2]) == 1 else self.generate_triple_with_numbers()
            if random.random() < 0.2:
                username = self.generate_with_symbols(username)
            usernames.append(username)

        for _ in range(count):
            username = self.generate_quadruple_letter() if random.choice([1, 2]) == 1 else self.generate_quadruple_with_numbers()
            if random.random() < 0.2:
                username = self.generate_with_symbols(username)
            usernames.append(username)

        return list(set(usernames))

    def check_instagram_username(self, username):
        try:
            url = f"https://www.instagram.com/{username}/"
            response = self.session.get(url, timeout=10)
            if response.status_code == 404:
                return True
            elif response.status_code == 200:
                return False
            else:
                return False
        except Exception as e:
            print(f"خطأ في التحقق من {username}: {e}")
            return False

    def generate_email_from_username(self, username, domain="gmail.com"):
        random_suffix = "".join(random.choice(string.digits) for _ in range(3))
        return f"{username}{random_suffix}@{domain}"

    def send_notification_email(self, username, email):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = self.email
            msg["Subject"] = f"يوزر إنستغرام متاح: {username}"

            body = (
                "تم العثور على يوزر إنستغرام متاح!\n\n"
                f"اليوزر: {username}\n"
                f"الإيميل المقترح: {email}\n"
                f"وقت العثور: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"رابط إنستغرام: https://www.instagram.com/{username}/\n"
            )
            msg.attach(MIMEText(body, "plain", "utf-8"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.email, self.email_password)
            server.sendmail(self.email, self.email, msg.as_string())
            server.quit()
            print(f"تم إرسال إشعار عن اليوزر المتاح: {username}")
            return True
        except Exception as e:
            print(f"حدث خطأ أثناء إرسال الإشعار: {e}")
            return False

    def send_summary_email(self, available_usernames):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = self.email
            msg["Subject"] = f"ملخص يوزرات إنستغرام المتاحة - {time.strftime('%Y-%m-%d')}"

            body_lines = ["اليوزرات المتاحة على إنستغرام:", ""]
            for i, username in enumerate(available_usernames, 1):
                email = self.generate_email_from_username(username)
                body_lines.append(f"{i}. {username} - {email}")
            body_lines.append("")
            body_lines.append(f"مجموع: {len(available_usernames)}")
            msg.attach(MIMEText("\n".join(body_lines), "plain", "utf-8"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.email, self.email_password)
            server.sendmail(self.email, self.email, msg.as_string())
            server.quit()
            print("تم إرسال الإيميل الملخص!")
            return True
        except Exception as e:
            print(f"حدث خطأ أثناء إرسال الإيميل الملخص: {e}")
            return False

def main():
    print("=" * 60)
    print("أداة البحث عن يوزرات إنستغرام المتاحة")
    print("=" * 60)

    email = input("أدخل عنوان الإيميل الرئيسي: ")
    password = input("أدخل كلمة مرور الإيميل (يفضل App Password): ")

    checker = InstagramUsernameChecker(email, password)

    try:
        count = int(input("كم يوزر تريد توليده من كل نوع؟ (الافتراضي: 5): ") or "5")
    except Exception:
        count = 5

    print("\nجاري توليد أسماء المستخدمين...")
    usernames = checker.generate_all_usernames(count)
    print(f"تم توليد {len(usernames)} يوزر للفحص")

    print("جاري فحص اليوزرات على إنستغرام...")
    available_count = 0

    for i, username in enumerate(usernames, 1):
        print(f"جاري فحص اليوزر {i}/{len(usernames)}: {username}")
        if checker.check_instagram_username(username):
            print(f"✅ متاح: {username}")
            available_count += 1
            checker.available_usernames.append(username)
            suggested_email = checker.generate_email_from_username(username)
            checker.send_notification_email(username, suggested_email)
            time.sleep(2)
        else:
            print(f"❌ محجوز: {username}")
            time.sleep(1)

    print("\n" + "=" * 60)
    print("نتائج الفحص:")
    print("=" * 60)
    print(f"عدد اليوزرات المفحوصة: {len(usernames)}")
    print(f"عدد اليوزرات المتاحة: {available_count}")

    if available_count > 0:
        print("\nاليوزرات المتاحة:")
        for i, username in enumerate(checker.available_usernames, 1):
            suggested_email = checker.generate_email_from_username(username)
            print(f"{i}. {username} - {suggested_email}")

        filename = f"available_instagram_usernames_{int(time.time())}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write("اليوزرات المتاحة على إنستغرام:\n\n")
            for username in checker.available_usernames:
                email_line = checker.generate_email_from_username(username)
                file.write(f"{username} - {email_line}\n")
        print(f"\nتم حفظ اليوزرات المتاحة في ملف: {filename}")

        send_summary = input("\nهل تريد إرسال ملخص؟ (y/n): ")
        if send_summary.lower() == "y":
            checker.send_summary_email(checker.available_usernames)
    else:
        print("لم يتم العثور على أي يوزرات متاحة.")

    print("\nتم الانتهاء من عملية الفحص!")

if _name_ == "_main_":
    main()