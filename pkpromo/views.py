import datetime
import json
import urllib.request
import urllib.parse
import re
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

from pkpromo.models import Abiturientus, AbiturientusFile


#def relative_to_absolute_links(html):
#    prefix = 'https://vk.com'
#
 #   #regex = re.compile("(href|src|action|background)=\"[^\"]*\"")
#    result = re.sub(r'((href|src)=[\'\"](?!http))(.*?[\'\"])', '\\1%s\\3' % prefix, html)
#    return result


def index(request):
    #sock = urllib.request.urlopen("https://vk.com/widget_article.php?app=0&width=100%25&_ver=1&url=%40ustu_official-arhitektora&startWidth=0&referrer=&title=%D0%9F%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B2%20%D0%A3%D0%93%D0%A2%D0%A3&17283ed2b6a")
    #html_source = sock.read().decode(sock.headers.get_content_charset())
    #sock.close()

    #html_source = relative_to_absolute_links(html_source)
    return render(request, 'index.html')


#def get_vk_widget(request):
#    sock = urllib.request.urlopen("")
 #   html_source = sock.read().decode(sock.headers.get_content_charset())
#    sock.close()
#
 #   return html_source


def index_vr(request):
    #sock = urllib.request.urlopen("https://vk.com/widget_article.php?app=0&width=100%25&_ver=1&url=%40ustu_official-arhitektora&startWidth=0&referrer=&title=%D0%9F%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B2%20%D0%A3%D0%93%D0%A2%D0%A3&17283ed2b6a")
    #html_source = sock.read().decode(sock.headers.get_content_charset())
    #sock.close()

    #html_source = relative_to_absolute_links(html_source)
    return render(request, 'vrindex.html')


def send_main_form(request):
    name = request.POST.get('name', None)
    surname = request.POST.get('surname', None)
    middlename = request.POST.get('middlename', None)
    tel = request.POST.get('tel', None)
    time = request.POST.get('time', None)

    text = """Абитуриент %(surname)s %(name)s %(middlename)s запрашивает звонок на телефон %(tel)s. Удобное время для звонка — %(time)s.""" % ({
        'name': name,
        'surname': surname,
        'middlename': middlename,
        'tel': tel,
        'time': time,
    })

    #browser_user_agent = request.META.get('HTTP_USER_AGENT', '')
    #browser_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    #remote_addr = request.META.get('REMOTE_ADDR', '')
    #x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    #messages_deelivered =

    send_mail(
        "pkpromo.ugtu.net: Новый абитуриент запрашивает звонок",
        text,
        'no-reply@ugtu.net',
        settings.EMAIL_THEM,
        fail_silently=True,
    )

    #Проверить, норм ли всё
    #записать в БД со статусом отправлено или нет

    return_data = {'message': 'Мы перезвоним, текст'}
    data = json.dumps(return_data, ensure_ascii=False)
    return HttpResponse(data, content_type='application/json')


def apply_form(request):
    if request.method == 'POST':
        recaptcha_token = request.POST.get('g-recaptcha-response')

        if not recaptcha_token:
            return render(request, 'apply.html', {'recaptcha_error': 'Капча не пройдена. Попробуйте ещё раз.'})

        url = 'https://www.google.com/recaptcha/api/siteverify'
        params = urllib.parse.urlencode({
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_token
        }).encode('utf-8')

        print(params)

        with urllib.request.urlopen(url, data=params) as response:
            result = json.loads(response.read().decode())

        print(result)
        if not result.get('success'):
            return render(request, 'apply.html', {'recaptcha_error': 'Капча не пройдена. Попробуйте ещё раз.'})

        fio = request.POST.get('fio', "")
        phone = request.POST.get('phone', "")
        email = request.POST.get('email', "")

        #abiturientus = Abiturientus(fio="%s %s %s" % (fio, phone, email))
        abiturientus = Abiturientus(fio=fio, comment="%s\n%s" % (phone, email), apply_date=datetime.date.today())
        abiturientus.save()

        pds = request.FILES.getlist('pd')
        for pd_file in pds:
            AbiturientusFile(abiturientus=abiturientus, file_type='pd', file=pd_file).save()

        pds = request.FILES.getlist('distributepd')
        for pd_file in pds:
            AbiturientusFile(abiturientus=abiturientus, file_type='distributepd', file=pd_file).save()

        pds = request.FILES.getlist('epgu')
        for pd_file in pds:
            AbiturientusFile(abiturientus=abiturientus, file_type='epgu', file=pd_file).save()

        pds = request.FILES.getlist('zayava')
        for pd_file in pds:
            AbiturientusFile(abiturientus=abiturientus, file_type='zayava', file=pd_file).save()

        pds = request.FILES.getlist('zachisl')
        for pd_file in pds:
            AbiturientusFile(abiturientus=abiturientus, file_type='zachisl', file=pd_file).save()

        pds = request.FILES.getlist('passport')
        for pd_file in pds:
            AbiturientusFile(abiturientus=abiturientus, file_type='passport', file=pd_file).save()

        pds = request.FILES.getlist('docobrazov')
        for pd_file in pds:
            AbiturientusFile(abiturientus=abiturientus, file_type='docobrazov', file=pd_file).save()

        pds = request.FILES.getlist('snils')
        for pd_file in pds:
            AbiturientusFile(abiturientus=abiturientus, file_type='snils', file=pd_file).save()

        pds = request.FILES.getlist('other')
        if pds:
            for pd_file in pds:
                AbiturientusFile(abiturientus=abiturientus, file_type='other', file=pd_file).save()

        try:
            text = """Абитуриент %(fio)s загрузил документы.\nВы можете увидеть их по ссылке:\nhttp://%(url)s/admin/pkpromo/abiturientus/%(abi_id)s/change/
            """ % ({
                'fio': abiturientus.fio,
                'url': request.META['HTTP_HOST'],
                'abi_id': abiturientus.pk
            })

            send_mail(
                "pkpromo.ugtu.net: Новый абитуриент загрузил документы",
                text,
                'no-reply@ugtu.net',
                settings.EMAIL_THEM,
                fail_silently=True,
            )
        except Exception:
            pass

        return HttpResponseRedirect(reverse('url_apply_ty'))

    return render(request, 'apply.html')


def apply_ty(request):
    return render(request, 'apply_ty.html')

