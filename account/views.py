from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm

from .models import Account, Record
from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserForm


@login_required(login_url='login')
def homepage(request):
    user = request.user
    account = Account.objects.get(user=user)
    record = Record.objects.get(user=user)
    context = {
        'account': account,
        'record': record,
    }

    return render(request, 'homepage.html', context)


def register(request):
    if not request.user.is_authenticated:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        context = {
            'form': form
        }
    else:
        return redirect('home')

    return render(request, 'auth/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'auth/login.html', {'error_message': 'Invalid login'})

    return render(request, 'auth/login.html')


@login_required(login_url='login')
def deposit_view(request):
    user = request.user
    account = Account.objects.get(user=user)

    if request.method == 'POST':
        action = request.POST.get('action')
        amount = request.POST.get('amount')
        if action == 'deposit':
            # Call the Crypto.com API to initiate a deposit transaction
            result = request.post(
                'https://api.crypto.com/v1/deposit',
                json={'user_id': user.id, 'amount': amount}
            )
            # Check the response to see if the deposit was successful
            if result.status_code == 200:
                # Deposit was successful, update the user's account balance
                account.deposit(amount)
                account.save()
                return redirect('home')
            else:
                # Handle the error, for example by displaying a message to the user
                pass
            return redirect('home')
    context = {'account': account}
    return render(request, 'account.html', context)


@login_required(login_url='login')
def withdraw_view(request):
    user = request.user
    account = Account.objects.get(user=user)
    if request.method == 'POST':
        action = request.POST.get('action')
        amount = request.POST.get('amount')
        if action == 'withdraw':
            account.withdraw(amount)
            account.save()
            return redirect('home')
    context = {'account': account}
    return render(request, 'account.html', context)


@login_required(login_url='login')
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user=user)
        if form.is_valid():
            form.save()
    else:
        form = UserForm(instance=user)
    context = {
        'form': form,
        'password_form': password_form,
    }
    return render(request, 'auth/user_profile.html', context)
