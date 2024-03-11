from urllib import request

from django.shortcuts import render, HttpResponse
import json
from email.utils import formataddr
from smtplib import SMTP_SSL, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import environ
from datetime import datetime

times = 0

def login(request):
    global times
    times += 1
    if request.path == '/login/signin/':
        report_loc = '../signin/'
    else:
        report_loc = 'signin/'
    return render(request, 'login.html', {'loc': report_loc, 'error': ''})

def signin(request):
    json2 = open('user_data.json', )
    data = json.load(json2)
    # ADMIN
    admin_l1 = data['admin'][0]
    emails_admin_l1 = list(admin_l1.keys())
    passwords_admin_l1 = list(admin_l1.values())
    # TECHNICAL
    technical_l1 = data['technical'][0]
    emails_technical_l1 = list(technical_l1.keys())
    passwords_technical_l1 = list(technical_l1.values())
    # SUPERVISOR
    supervisor_l1 = data['supervisor'][0]
    emails_supervisor_l1 = list(supervisor_l1.keys())
    passwords_supervisor_l1 = list(supervisor_l1.values())

    json2.close()
    global times
    times = times + 1
    if request.path == '/login/signin/':
        report_loc = '../signin/'
    else:
        report_loc = 'signin/'
    email = request.POST['email']
    password = request.POST['password']
    # ADMIN
    if email in emails_admin_l1:
        print(passwords_admin_l1[emails_admin_l1.index(email)])
        if passwords_admin_l1[emails_admin_l1.index(email)] == password:
            times = 0
            request.session['page'] = 'templates/admin_template.html'
            return render(request, '../templates/templates/admin_template.html')
        else:
            return render(request, 'login.html', {'loc': report_loc, 'errorclass': 'alert alert-danger',
                                                  'error': 'Lo siento. El correo electrónico y la contraseña no coinciden.'})
    # TECHNICAL
    elif email in emails_technical_l1:
        if passwords_technical_l1[emails_technical_l1.index(email)] == password:
            times = 0
            request.session['user'] = email
            request.session['page'] = 'templates/technical_template.html'
            return render(request, '../templates/templates/technical_template.html')
        else:
            return render(request, 'login.html', {'loc': report_loc, 'errorclass': 'alert alert-danger',
                                                  'error': 'Lo siento. El correo electrónico y la contraseña no coinciden.'})
    # SUPERVISOR
    elif email in emails_supervisor_l1:
        if passwords_supervisor_l1[emails_supervisor_l1.index(email)] == password:
            times = 0
            request.session['page'] = 'templates/supervisor_template.html'
            return render(request, '../templates/templates/supervisor_template.html')
        else:
            return render(request, 'login.html', {'loc': report_loc, 'errorclass': 'alert alert-danger',
                                                  'error': 'Lo siento. El correo electrónico y la contraseña no coinciden.'})
    else:
        return render(request, 'login.html', {'loc': report_loc, 'errorclass': 'alert alert-danger', 'error': 'Lo siento. El correo electrónico y la contraseña no coinciden!'})

# settings
def settings(request):
    global times
    json2 = open('settings_data.json', )
    data = json.load(json2)
    settings = data['settings']
    template = request.session['page']
    return render(request, '../templates/settings.html', {'settings': settings[0], 'template': template})

def updateSettings(request):
    # post data
    social_reason = request.POST['social_reason']
    name = request.POST['name']
    ruc = request.POST['ruc']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    address_2 = request.POST['address_2']
    #  update in data json
    with open('settings_data.json', 'r+') as jsonFile:
        data = json.load(jsonFile)
        file_data = [{
            "social_reason": social_reason,
            "name": name,
            "ruc": ruc,
            "email": email,
            "phone": phone,
            "address": address,
            "address_2": address_2
        }]
        data["settings"] = file_data
        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile)
        jsonFile.truncate()
    # return data
    message = 'Configuraciones actualizadas exitosamente!'
    type = 'success'
    json2 = open('settings_data.json', )
    data = json.load(json2)
    settings = data['settings']
    template = request.session['page']
    return render(request, '../templates/settings.html', {'settings': settings[0], 'template': template, 'message': message, 'type': type})

# incidence
def incidence(request):
    global times
    json2 = open('technicals_data.json', )
    data = json.load(json2)
    technicals = data['technicals']
    template = request.session['page']
    return render(request, '../templates/incidence.html', {'technicals': technicals, 'template': template})

def storeIncidence(request):
    global times
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d, %H:%M")
    # post data
    name = request.POST['name']
    document = request.POST['document']
    address = request.POST['address']
    phone = request.POST['phone']
    detail = request.POST['detail']
    email = request.POST['email']
    technical = request.POST['technical']

    json2 = open('incidence_data.json', )
    data = json.load(json2)
    # ADMIN
    admin_l1 = data['incidences']

    if len(admin_l1) > 0 and admin_l1[-1].get('code') is not None:
        code = admin_l1[-1].get('code')
    else:
        code = "0000001"
    json2.close()

    code = int(code) + 1
    code = "{:07d}".format(code)
    # end post data
    new_data = {
        "code": code,
        "name": name,
        "document": document,
        "address": address,
        "phone": phone,
        "detail": detail,
        "detail_technic": '',
        "price": '',
        "email": email,
        "technical": technical,
        "status": 'PENDING'
    }
    write_json(new_data, 'incidence_data.json', 'incidences')

    # Send email
    BODY_HTML = """<html>
            <head></head>
            <body>
              <h1>Sistema de gestión de incidencias</h1>
              <h2>Su incidecia se ha registrado exitosamente a continuación adjuntamos la información de la misma</h2>
              <h3>Detalle de incidencia</h3>
              <h4>Código: """ + code + """</h4>
              <h4>Nombre: """ + name + """</h4>
              <h4>Cédula: """ + document + """</h4>
              <h4>Dirección: """ + address + """</h4>
              <h4>Teléfono: """ + phone + """</h4>
              <h4>Fecha: """ + current_time + """</h4>
            </body>
            </html>"""
    SUBJECT = 'Registro de incidencia'
    send_email(email, BODY_HTML, SUBJECT)

    # return data
    json2 = open('technicals_data.json', )
    data = json.load(json2)
    technicals = data['technicals'][0]
    message = 'Registro de incidencia exitoso!'
    type = 'success'
    template = request.session['page']
    return render(request, '../templates/incidence.html',
                  {'technicals': technicals, 'message': message, 'type': type, 'template': template})

# technical
def technical(request):
    global times
    template = request.session['page']
    return render(request, '../templates/technical.html', {'template': template})

def storeTechnical(request):
    global times
    # post data
    email = request.POST['email']
    password = request.POST['password']
    names = request.POST['names']
    identify = request.POST['identify']

    json2 = open('user_data.json', )
    data = json.load(json2)
    l1 = data['technical'][0]

    json3 = open('technicals_data.json', )
    data3 = json.load(json3)
    l2 = data3['technicals']

    # validation if user exist in list
    validate_user = False
    for l in l2:
        for attribute, value in l.items():
            if attribute == 'email':
                if value == email:
                    validate_user = True
                    break
            elif attribute == 'identity':
                if value == identify:
                    validate_user = True
                    break
    if validate_user:
        message = 'Usuario registrado anteriormente'
        type = 'warning'
        json2 = open('user_data.json', )
        data = json.load(json2)
        technicals = data['technical'][0]
        template = request.session['page']
        return render(request, '../templates/technical.html',
                      {'technicals': technicals, 'message': message, 'type': type, 'template': template})

    emails = list(l1.keys())
    passwords = list(l1.values())
    emails.append(email)
    passwords.append(password)
    d4 = {emails[len(emails) - 1]: passwords[len(emails) - 1]}
    for x in range(len(emails) - 1):
        d4 = dict(list(d4.items()) + list({emails[x]: passwords[x]}.items()))
    with open('user_data.json', 'r+') as a:
        file_data = json.load(a)
        file_data['technical'] = [d4]
        # Sets file's current position at offset.
        a.seek(0)
        # convert back to json.
        json.dump(file_data, a, indent=4)
        a.close()
    # end post data technicals
    new_data = {
        'email': email,
        'password': password,
        'names': names,
        'identify': identify
    }
    write_json(new_data, 'technicals_data.json', 'technicals')
    # return data
    json2 = open('user_data.json', )
    data = json.load(json2)
    technicals = data['technical'][0]
    message = 'Registro de técnico exitoso!'
    type = 'success'
    template = request.session['page']
    return render(request, '../templates/technical.html',
                  {'technicals': technicals, 'message': message, 'type': type, 'template': template})

def order(request, num):
    global times
    match num:
        case 1:
            type = 'PENDING'
        case 2:
            type = 'IN_PROGRESS'
        case 3:
            type = 'FINISH'
    template = request.session['page']
    admin = False
    if template == 'templates/admin_template.html' or template == 'templates/supervisor_template.html':
        admin = True
    # ADMIN each json
    json2 = open('incidence_data.json', )
    data = json.load(json2)
    json2.close()
    incidences = data['incidences']
    result = []
    for incidence in incidences:
        if incidence["status"] == type:
            if admin:
                result.append(incidence)
            else:
                if incidence["technical"] == request.session['user']:
                    result.append(incidence)
    return render(request, '../templates/order/index.html', {'template': template, 'incidences': result, 'num': num})

def orderEdit(request, code, num):
    global times
    template = request.session['page']
    match num:
        case 1:
            array_type = {'code': [{
                'code': 'IN_PROGRESS',
                'trans': 'EN PROCESO'
            }]}
        case 2:
            array_type = {'code': [{
                'code': 'FINISH',
                'trans': 'TERMINADO'
            }]}
        case _:
            array_type = {}
    # ADMIN each json
    json2 = open('incidence_data.json', )
    data = json.load(json2)
    json2.close()
    incidences = data['incidences']
    result = {}
    message = None
    type = None
    for incidence in incidences:
        if (incidence["code"] == code):
            result = incidence
            break
    if result == {}:
        message = 'No se encontró orden de trabajo!'
        type = 'danger'
    return render(request, '../templates/order/edit.html',
                  {'template': template, 'incidence': result, 'message': message, 'type': type,
                   'array_type': array_type['code'], 'num': num})

def orderUpdate(request):
    global times
    # post data
    detail_technic = request.POST['detail_technic']
    status = request.POST['status']
    code = request.POST['code']
    price = request.POST.get('price', 0)
    validate_count = 0
    with open('incidence_data.json', 'r+') as f:
        data = json.load(f)
        count = 0
        for incidence in data['incidences']:
            if (incidence["code"] == code):
                data['incidences'][count]['status'] = status
                data['incidences'][count]['detail_technic'] = detail_technic
                validate_count = count
                if price:
                    data['incidences'][count]['price'] = price
            count = count + 1
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part

    match status:
        case 'IN_PROGRESS':
            # Send email
            BODY_HTML = """<html>
                    <head></head>
                    <body>
                      <h1>Sistema de gestión de incidencias</h1>
                      <h2>Este es un mensaje para informarle que estamos trabando en su incidencia</h2>
                      <h3>Detalle de incidencia</h3>
                      <h4>Código: """ + data['incidences'][validate_count]['code'] + """</h4>
                      <h4>Detalle técnico: """ + detail_technic + """</h4>
                    </body>
                    </html>"""
            SUBJECT = 'Cambios en su incidencia'
            send_email(data['incidences'][validate_count]['email'], BODY_HTML, SUBJECT)
        case 'FINISH':
            # Send email
            BODY_HTML = """<html>
                        <head></head>
                        <body>
                          <h1>Sistema de gestión de incidencias</h1>
                          <h2>Este es un mensaje para informarle que hemos terminado el trabajo en su incidencia</h2>
                          <h3>Detalle de incidencia</h3>
                          <h4>Código: """ + data['incidences'][validate_count]['code'] + """</h4>
                          <h4>Detalle técnico: """ + detail_technic + """</h4>
                          <h4>Costo: """ + price + """</h4>
                        </body>
                        </html>"""
            SUBJECT = 'Cambios en su incidencia'
            send_email(data['incidences'][validate_count]['email'], BODY_HTML, SUBJECT)
    # return data
    template = request.session['page']
    json2 = open('incidence_data.json', )
    data = json.load(json2)
    json2.close()
    incidences = data['incidences']
    result = {}
    for incidence in incidences:
        if (incidence["code"] == code):
            result = incidence
            break
    message = 'Orden de trabajo editado correctamente!'
    type = 'success'
    return render(request, '../templates/order/edit.html',
                  {'template': template, 'incidence': result, 'message': message, 'type': type})

def write_json(new_data, filename, field):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[field].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)

def send_email(email, BODY_HTML,SUBJECT):
    print('sending email to' + email)
    env = environ.Env(
        DEBUG=(bool, False)
    )
    SENDER = env('SENDER')
    SENDERNAME = env('SENDERNAME')
    USERNAME_SMTP = env('USERNAME_SMTP')
    PASSWORD_SMTP = env('PASSWORD_SMTP')
    HOST = env('HOST')
    PORT = env('PORT')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = formataddr((SENDERNAME, SENDER))
    msg['To'] = email
    part = MIMEText(BODY_HTML, 'html')
    msg.attach(part)
    try:
        with SMTP_SSL(HOST, PORT) as server:
            server.login(USERNAME_SMTP, PASSWORD_SMTP)
            server.sendmail(SENDER, email, msg.as_string())
            server.close()
            print("Correo enviado!")
    except SMTPException as e:
        print("Error en el envío de email: ", e)