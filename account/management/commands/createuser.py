import re

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    help = "This command is to create user with different levels"

    def add_arguments(self, parser):
        parser.add_argument("-c", "--count", type=int, 
        help="Count of users creates")

        parser.add_argument("-l", "--level", type=str,
        help="For set level of the user (normal, super, admin)")

    def handle(self, *args, **options):
        levels = ("normal", "super", "admin")

        count = max((options["count"] or 1), 1)
        level = options["level"] or "normal"

        if level not in levels:
            level = "normal"
        
        for number in range(1, count + 1):
            self.stdout.write(self.style.
            HTTP_INFO(f"\nCreate user {str(number)}th:"))

            username = self.get_username()
            email = self.get_email()
            password = self.get_password()
            
            user = User.objects.create_user(username=username, 
            email=email, password=password)
            
            if level.lower() == "super":
                user.is_staff = True
                user.is_superuser = True
                user.save()

            if level.lower() == "admin":
                user.is_staff = True
                user.is_superuser = True
                user.is_admin = True
                user.save()

            self.stdout.write(self.style.
            SUCCESS(f"\nUser {username} create successful!\n"))

    def get_username(self):
        all_usernames = User.objects.values_list("username")
        usernames = (username[0].lower() for username in all_usernames)

        while True:
            username = input("\nUsername:\n-> ")

            if username.lower() in usernames:
                self.stdout.write(self.style.
                ERROR("Your username should not be in the database."))
            elif not validate_username(username):
                self.stdout.write(self.style.ERROR(
                "Your username must start and end with English letters,\n" 
                "and you can use periods and underscores,\n" 
                "with a minimum of 3 letters and a maximum of 50."
                ))
            else:
                return username

    def get_email(self):
        all_emails = User.objects.values_list("email")
        emails = (email[0] for email in all_emails)

        while True:
            email = input("\nEmail:\n-> ")

            if email.lower() in emails:
                self.stdout.write(self.style.
                ERROR("Your email should not be in the database."))
            elif not validate_email(email):
                self.stdout.write(self.style.ERROR("Please enter a email."))
            else:
                return email

    def get_password(self):
        while True:
            min_length = 4
            password = input("\nPassword:\n-> ")

            if len(password) < min_length:
                self.stdout.write(self.style.
                ERROR("Your password must be at least 4 characters long."))
            else:
                return password

def validate_username(username):
    min_length, max_length = 3, 50
    pattern = r"^[a-zA-Z]+([._]?[a-zA-Z0-9]+)*$"

    if re.match(pattern, username) and min_length <= len(username) <= max_length:
        return True
    return False

def validate_email(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    if re.match(pattern, email):
        return True
    return False
            