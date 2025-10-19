from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

def cadastro(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            Usuario.objects.create(fullname=fullname, email=email, password=password)
            return redirect('index')  # Redireciona para login ou outra página
        else:
            return render(request, 'APPEstoque/cadastro.html', {'error': 'Senhas não conferem!'})

    return render(request, 'APPEstoque/cadastro.html')

def index(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(password, usuario.password):
                # Login bem-sucedido
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nome'] = usuario.fullname
                return redirect('dashboard')  # ou outra página
            else:
                return render(request, 'APPEstoque/index.html', {'error': 'Senha incorreta'})
        except Usuario.DoesNotExist:
            return render(request, 'APPEstoque/index.html', {'error': 'E-mail não cadastrado'})

    return render(request, 'APPEstoque/index.html')

@login_required
def dashboard(request):
    return render(request, 'APPEstoque/dashboard.html')

def password(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'APPEstoque/password.html', {'error': 'Senhas não conferem!'})

        try:
            user = Usuario.objects.get(fullname=fullname, email=email)
            user.set_password(password)  # Define a nova senha de forma segura
            user.save()
            return redirect('index')  # Redireciona para login ou outra página
        except Usuario.DoesNotExist:
            return render(request, 'APPEstoque/password.html', {'error': 'Usuário não encontrado!'})

    return render(request, 'APPEstoque/password.html')

def container(request):
    return render(request, 'APPEstoque/container.html')