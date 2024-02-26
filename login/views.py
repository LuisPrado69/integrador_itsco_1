from django.shortcuts import render, HttpResponse
import json

times = 0


def login(request):
    global times
    print('Login Page Opened!')
    times += 1
    if request.path == '/login/signin/':
        report_loc = '../signin/'
    else:
        report_loc = 'signin/'
    return render(request, 'login.html', {'loc': report_loc, 'error': ''})


def signin(request):
    print('Login Request Made!')
    print('Reading Data from JSON')
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
    print('Read data from JSON')
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
            print('Logged in ADMIN PAGE, returning HTTP response')
            return HttpResponse('Logged in ADMIN PAGE, returning HTTP response')
        else:
            print('Email != Password, returning HTTP response')
            return render(request, 'login.html', {'loc': report_loc, 'errorclass': 'alert alert-danger',
                                                  'error': 'Sorry. The Email and Password do not match.'})
    # TECHNICAL
    elif email in emails_technical_l1:
        if passwords_technical_l1[emails_technical_l1.index(email)] == password:
            times = 0
            print('Logged in TECHNICAL PAGE, returning HTTP response')
            return render(request, '../templates/technical_template.html')
        else:
            print('Email != Password, returning HTTP response')
            return render(request, 'login.html', {'loc': report_loc, 'errorclass': 'alert alert-danger',
                                                  'error': 'Sorry. The Email and Password do not match.'})
    # SUPERVISOR
    elif email in emails_supervisor_l1:
        if passwords_supervisor_l1[emails_supervisor_l1.index(email)] == password:
            times = 0
            print('Logged in SUPERVISOR PAGE, returning HTTP response')
            return HttpResponse('Logged in SUPERVISOR PAGE, returning HTTP response')
        else:
            print('Email != Password, returning HTTP response')
            return render(request, 'login.html', {'loc': report_loc, 'errorclass': 'alert alert-danger',
                                                  'error': 'Sorry. The Email and Password do not match.'})
    else:
        print('Account does not exist, returning HTTP response')
        return render(request, 'login.html', {'loc': report_loc, 'errorclass': 'alert alert-danger',
                                              'error': 'Sorry. No such account exists. Consider signing up!'})


def incidence(request):
    global times
    return render(request, '../templates/incidence.html')


def storeIncidence(request):
    global times
    # post data
    name = request.POST['name']
    document = request.POST['document']
    address = request.POST['address']
    phone = request.POST['phone']
    detail = request.POST['detail']
    email = request.POST['email']

    json2 = open('incidence_data.json', )
    data = json.load(json2)
    # ADMIN
    admin_l1 = data['technical']

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
        "email": email
    }
    print(code)
    write_json(new_data)
    return render(request, '../templates/incidence.html')


def write_json(new_data, filename='incidence_data.json'):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["technical"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)
