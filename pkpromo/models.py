import datetime

from django.db import models
import string
import secrets
import hashlib


class UserData(models.Model):
    name = models.CharField('Имя', max_length=69, blank=False)
    email = models.EmailField(null=False, blank=False, verbose_name='Адрес электронной почты')
    phone = models.CharField('Телефон', max_length=20, null=False, blank=False)
    #when_call = models.CharField('Имя', max_length=69, blank=False)

    class Meta:
        #ordering = ['-date']
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return "%s" % (self.name)


STATUSES = (
    ('default', 'не установлен'),
    ('decline', 'Отклонено'),
    ('accept', 'Согласовано'),
    ('seen', 'Просмотрено')
)


class Abiturientus(models.Model):
    fio = models.CharField('ФИО', max_length=256, blank=False)
    code = models.CharField(max_length=32)
    status = models.CharField(choices=STATUSES, default='default', max_length=30, blank=False, null=False, verbose_name='Статус')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    apply_date = models.DateField(verbose_name='Дата загрузки документов', null=True, blank=True)

    def generate_code(self):
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for i in range(12))
        return code

    class Meta:
        verbose_name = 'Абитуриент'
        verbose_name_plural = 'Абитуриенты'

    def save(self, *args, **kwargs):
        if not self.pk:
            gen_code = self.generate_code()

            un_code = "%s%s" % (self.fio, gen_code)
            hash = hashlib.md5(un_code.encode()).hexdigest()

            self.code = hash
        super(Abiturientus, self).save(*args, **kwargs)

    def __str__(self):
        return "%s — Статус: %s" % (self.fio, self.get_status_display() if self.status else 'не установлен')


def generate_filename(self, filename):
    url = "files/users/%s %s/%s/%s" % (self.abiturientus.fio, self.abiturientus.code, self.file_type, filename)
    return url


FILE_TYPES = (
    ('pd', 'Заявление о согласии на обработку ПД'),
    ('distributepd', 'Заявление о согласии на распространение ПД'),
    ('epgu', 'Заявление о согласии на передачу информации на ЕПГУ'),
    ('zayava', 'Заявление'),
    ('zachisl', 'Заявление о согласии на зачисление'),
    ('passport', 'Паспорт'),
    ('docobrazov', 'Документ об образовании'),
    ('snils', 'СНИЛС'),
    ('other', 'Иные документы')
)

FILE_TYPES_DICT = {
    'pd': 'Заявление о согласии на обработку ПД',
    'distributepd': 'Заявление о согласии на распространение ПД',
    'epgu': 'Заявление о согласии на передачу информации на ЕПГУ',
    'zayava': 'Заявление',
    'zachisl': 'Заявление о согласии на зачисление',
    'passport': 'Паспорт',
    'docobrazov': 'Документ об образовании',
    'snils': 'СНИЛС',
    'other': 'Иные документы'
}


class AbiturientusFile(models.Model):
    file = models.FileField(upload_to=generate_filename, max_length=256)
    file_type = models.CharField(choices=FILE_TYPES, max_length=256)
    abiturientus = models.ForeignKey(Abiturientus, on_delete=models.CASCADE, related_name='files')


    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return "%s — %s" % (self.abiturientus.fio, self.get_file_type_display())

