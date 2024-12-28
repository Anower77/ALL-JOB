from django.core.mail import send_mail

def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        'anowerhossain765562@gmail.com',  # Replace with your email
        recipient_list,
        fail_silently=False,
    )
