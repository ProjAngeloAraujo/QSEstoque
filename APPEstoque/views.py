from django.shortcuts import render, redirect
from .models import Usuario, Container, Produto, Pedido
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def cadastro(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'APPEstoque/cadastro.html', {
                'error': 'Senhas não conferem!'
            })

        # Evita cadastro duplicado
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'APPEstoque/cadastro.html', {
                'error': 'E-mail já cadastrado!'
            })

        Usuario.objects.create(fullname=fullname, email=email, password=password)
        return redirect('index')

    return render(request, 'APPEstoque/cadastro.html')


def index(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(password, usuario.password):
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nome'] = usuario.fullname
                return redirect('dashboard')
            else:
                return render(request, 'APPEstoque/index.html', {
                    'error': 'Senha incorreta'
                })
        except Usuario.DoesNotExist:
            return render(request, 'APPEstoque/index.html', {
                'error': 'E-mail não cadastrado'
            })

    return render(request, 'APPEstoque/index.html')


def dashboard(request):
    containers = Container.objects.all().prefetch_related('produtos')
    pedidos = Pedido.objects.order_by('-data_criacao')[:10]

    total_containers = containers.count()
    total_produtos = Produto.objects.count()
    pedidos_pendentes = Pedido.objects.filter(status_pedido='separar').count()
    containers_ativos = Container.objects.filter(status='ativo').count()

    contexto = {
        'usuario_nome': request.user.fullname if request.user.is_authenticated else 'Admin',
        'containers': containers,
        'pedidos': pedidos,
        'total_containers': total_containers,
        'total_produtos': total_produtos,
        'pedidos_pendentes': pedidos_pendentes,
        'containers_ativos': containers_ativos,
    }

    return render(request, 'APPEstoque/dashboard.html', contexto)


def password(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'APPEstoque/password.html', {
                'error': 'Senhas não conferem!'
            })

        try:
            user = Usuario.objects.get(fullname=fullname, email=email)
            user.set_password(password)
            user.save()
            return redirect('index')
        except Usuario.DoesNotExist:
            return render(request, 'APPEstoque/password.html', {
                'error': 'Usuário não encontrado!'
            })

    return render(request, 'APPEstoque/password.html')


def container(request):
    return render(request, 'APPEstoque/container.html')