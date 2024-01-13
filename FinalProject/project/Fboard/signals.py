from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Reply


@receiver(post_save, sender=Reply)
def reply_announcer(sender, instance, created, **kwargs):
    message_1 = f'Создан отклик для "{instance.post.title}" пользователем {instance.author}'
    email_box_1 = instance.post.author.email

    print(message_1)
    print(f'Автор {instance.post.author} получит письмо на {email_box_1}')
    if created:
        send_mail(subject='Для вашего объявления создан отклик!',
                  message=message_1,
                  from_email='Teardrop1303@yandex.ru',
                  recipient_list=[email_box_1, ])

    if instance.approved:
        message_2 = f'Отклик для "{instance.post.title}" одобрен автором {instance.post.author}'
        email_box_2 = instance.author.email

        send_mail(subject='Ваш отклик одобрен!',
                  message=message_2,
                  from_email='Teardrop1303@yandex.ru',
                  recipient_list=[email_box_2, ])