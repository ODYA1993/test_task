from django.db.models import Q
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from test_task.forms import NameForm, RegisterUserForm, LoginUserForm
from test_task.models import User, Score, TranslationHistory
import urllib


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'test_task/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'test_task/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def calculate(request):
    authenticated_user_id = request.user.id  # id авторизированный пользователь
    recipients = Score.objects.exclude(user_id=authenticated_user_id)  # id счетов НЕ авторизированных пользователей

    if request.method == 'POST':
        amount = request.POST['amount']  # сумма перевода
        your_accounts = request.POST.getlist('your_accounts')  # id счетов авторизированного пользователя
        transfer_score_id = request.POST['transfer']  # id_счета кому переводим
        transactions(your_accounts, amount, transfer_score_id, authenticated_user_id)

    data = {
        'form': NameForm(),
        'recipients': recipients,
    }
    return render(request, 'test_task/home.html', data)


def transactions(your_accounts, amount, transfer_score_id, authenticated_user_id):
    account_len = len(your_accounts)  # коль-во выбранных счетов
    i = int(amount) / account_len  # сумму делим на коль-во аккаунтов
    selected_accounts = Score.objects.filter(id__in=your_accounts)  # querySet id выбранных аккаунтов
    for selected_account in selected_accounts:
        if selected_account.balance < i:
            raise Exception('insufficient funds!')

        selected_account.balance = float(selected_account.balance) - i
        selected_account.save()
        account_transfer = Score.objects.get(id=transfer_score_id)
        account_transfer.balance = float(account_transfer.balance) + i
        account_transfer.save()
        save_transactions(user=authenticated_user_id, score_sender=selected_account,
                          score_recipient=account_transfer, amount=i)


def save_transactions(user, score_sender, score_recipient, amount):
    return TranslationHistory.objects.create(user_id=user, score_sender=score_sender,
                                             score_recipient=score_recipient, amount=amount)


def history(request):
    q = request.GET.get('q', '')
    print('00000000000000', q)
    if q:
        history_filter = request.user.translationhistory_set.filter(
            Q(score_sender__account_number__icontains=q) |              #  сделать тернарным выражение
            Q(amount=q)).order_by('-id')
    else:
        history_filter = request.user.translationhistory_set.all().order_by('-id')

    paginator = Paginator(history_filter, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    from urllib.parse import urlencode
    params = {'q': q}
    q = urlencode(params)
    print(q)
    data = {
        'page_obj': page_obj,
        'q': q
    }
    return render(request, 'test_task/history.html', data)


def details(request, acc_id):
    score = Score.objects.filter(account_number=acc_id)

    data = {
        'score': score
    }
    return render(request, 'test_task/details_accounts.html', data)


