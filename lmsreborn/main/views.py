import re

from django.shortcuts import render, redirect
from .forms import RegForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import *
import json
import requests
User = get_user_model()


def register_view(request):
    if request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('log')
    form = RegForm()
    return render(request, template_name="registration.html", context={"form": form})

# important

# def login_view(request):
#     form = AuthenticationForm(request, data=request.POST)
#     # email = get_user_model().objects.get(username=request.POST.get('username')).email
#     # username = request.POST.get('username')
#     # password = request.POST.get('password')
#     # user = authenticate(username=username, password=password)
#     # if user is not None:
#     #     login(request, user)
#     #     return redirect("home")
#     return render(request=request, template_name="login.html", context={"form": form})


def auth_view(request):
    # print(get_user_model().objects.get.username)
    email = request.POST.get('username')
    password = request.POST.get('password')
    try:
        username = get_user_model().objects.get(email=email).username
    except:
        print('(((((((((((((((((((((((((((((')
        return redirect('err')
    else:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return redirect("err")


def HomePageView(request):
    context = {
        # 'dish': dishes.objects.all(),
    }
    return render(request, 'HomePage.html', context=context)


def AccountPageView(request):
    print(str(request.user))
    if request.user.is_authenticated:
        context = {
            # 'dish': dishes.objects.all(),
            'gpu': GPU.objects.all().order_by('-gpu_name'),
            'cpu': CPU.objects.all().order_by('-cpu_name'),
            'ram': RAM.objects.all(),
        }
        return render(request, 'AccountPage.html', context=context)
    else:
        return redirect('log')


def logout_view(request):
    logout(request)
    return redirect('log')


def delete_view(request):
    u = get_user_model().objects.get(username=str(request.user))
    u.delete()
    return redirect('log')


def update_username_view(request):
    if request.method == 'POST':
        # print(request.POST['dropdown'])
        user = get_user_model().objects.get(id=request.user.id)
        x = request.POST.get('new_username')
        user.username = x
        user.save()
        return redirect('account')


def update_email_view(request):
    if request.method == 'POST':
        user = get_user_model().objects.get(id=request.user.id)
        x = request.POST.get('new_email')
        user.email = x
        user.save()
        return redirect('account')


# def update_password_view(request):
#     if request.method == 'POST':
#         user = get_user_model().objects.get(id=request.user.id)
#         x = request.POST.get('new_password')
#         user.password = x
#         user.save()
#         return redirect('account')


def update_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('change_password')
        else:
            print('(((((((((((')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


def update_gpu_view(request):
    # for i in GPU.objects.all().values():
    #     print(i['gpu_name'])
    if request.method == 'POST':
        user = get_user_model().objects.get(id=request.user.id)
        x = request.POST['gpu_dropdown']
        print(x)
        user.gpu_model = GPU.objects.get(id=x)
        user.save()
        return redirect('account')


def update_cpu_view(request):
    if request.method == 'POST':
        user = get_user_model().objects.get(id=request.user.id)
        x = request.POST['cpu_dropdown']
        print(x)
        user.cpu_model = CPU.objects.get(id=x)
        user.save()
        return redirect('account')


def update_ram_view(request):
    if request.method == 'POST':
        user = get_user_model().objects.get(id=request.user.id)
        x = request.POST['ram_dropdown']
        print(x)
        user.ram_model = RAM.objects.get(id=x)
        user.save()
        return redirect('account')


def comparing(request):
    gpu = ''
    cpu = ''
    ram = ''
    SteamL = str(request.GET.get('SteamLink'))
    tx = 'https://store.steampowered.com/api/appdetails/?appids='
    cc = ''
    for i in range(35, len(SteamL)):
        if SteamL[i] != '/':
            cc = cc + SteamL[i]
        else:
            break
    tx = tx + cc

    response = requests.get(tx)
    k = json.loads(response.text)[cc]['data']['pc_requirements'].setdefault('recommended', 'Seems that this game does not have recommended system requirements.')
    k = k.replace('™', '')
    k = k.replace('®', '')
    g = ''
    g1 = ''
    c = ''
    c1 = ''
    for i in GPU.objects.all().values():
        if re.search(i['gpu_name'], k):
            g = i['gpu_name']
            g1 = i['teraflops']
    for i in CPU.objects.all().values():
        if re.search(i['cpu_name'], k):
            c = i['cpu_name']
            c1 = i['gaming_rate']
    print(g, g1, c, c1, sep=' ')
    ugpu = get_user_model().objects.get(username=str(request.user)).gpu_model
    ucpu = get_user_model().objects.get(username=str(request.user)).cpu_model
    ugpu1 = ''
    ucpu1 = ''
    # print(ugpu, ucpu)
    for i in GPU.objects.all().values():
        if str(i['gpu_name']) == str(ugpu):
            ugpu1 = i['teraflops']
    for i in CPU.objects.all().values():
        if str(i['cpu_name']) == str(ucpu):
            ucpu1 = i['gaming_rate']
    print(ugpu1, ucpu1, sep='|')
    resc = 0
    resg = 0
    res = ''
    if c1 != '' and ucpu1 != '':
        resc = int((int(ucpu1)*100)/(int(c1)))
    if g1 != '' and ugpu1 != '':
        resg = int((int(ugpu1)*100)/(int(g1)))
    if resc < 95 or resg < 95:
        res = 'You will most likely experience freezes and lags while playing'
    else:
        res = 'You will most likely experience good framerate and no lags while playing'
    context = {
        # 'dish': dishes.objects.all(),
        'sys': k,
        'gpu': g,
        'cpu': c,
        'gpu1': g1,
        'cpu1': c1,
        'ugpu1': ugpu1,
        'ucpu1': ucpu1,
        'resg': resg,
        'resc': resc,
        'res': res,
    }
    return render(request, 'comparison.html', context=context)
def info_view(request):
    context = {
        # 'dish': dishes.objects.all(),
        'gpu': GPU.objects.all().order_by('-teraflops'),
        'cpu': CPU.objects.all(),
        'ram': RAM.objects.all(),
    }
    return render(request, 'Info.html', context=context)




