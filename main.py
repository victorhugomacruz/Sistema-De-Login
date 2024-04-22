import flet as ft
import sqlite3
import smtplib
import email.message
from random import randint
from time import sleep
import hashlib

# Configurações principais da interface.
def sistema_login(page: ft.Page):
    page.title = 'Sistema de login'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 700
    page.window_width = 900
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.window_resizable = False
    page.window_maximizable = False
    page.fonts = {'Alumni Sans': '/fonts/AlumniSansRegular.ttf'}
    page.window_center()

    # Variável recebe a caixa de diálogo onde o usuário pode inserir seu email para fazer login na conta.
    entry_email_login = ft.TextField(
                    hint_text='Email',
                    width=300,
                    bgcolor='#a1afb8',
                    border_color='#a1afb8',
                    prefix_icon=ft.icons.EMAIL,
                    text_style=ft.TextStyle(font_family='Arial', size=15)
                )
    
    # Variável recebe a caixa de diálogo onde o usuário pode inserir sua senha para fazer login na conta.
    entry_senha_login = ft.TextField(
                    hint_text='Senha',
                    width=300,
                    bgcolor='#a1afb8',
                    border_color='#a1afb8',
                    password=True,
                    can_reveal_password=True,
                    prefix_icon=ft.icons.KEY,
                    text_style=ft.TextStyle(font_family='Arial', size=15)
                )
    
    # Variável recebe a caixa de diálogo onde o usuário pode inserir seu nome para criar sua conta.
    entry_nome_cadastrar = ft.TextField(
                    hint_text='Nome',
                    width=300,
                    bgcolor='#a1afb8',
                    border_color='#a1afb8',
                    prefix_icon=ft.icons.PEOPLE,
                    text_style=ft.TextStyle(font_family='Arial', size=15)
                )
    
    # Variável recebe a caixa de diálogo onde o usuário pode inserir seu email para criar sua conta.
    entry_email_cadastrar = ft.TextField(
                    hint_text='Email',
                    width=300,
                    bgcolor='#a1afb8',
                    border_color='#a1afb8',
                    prefix_icon=ft.icons.EMAIL,
                    text_style=ft.TextStyle(font_family='Arial', size=15)
                )
    
    # Variável recebe a caixa de diálogo onde o usuário pode inserir sua senha para criar sua conta.
    entry_senha_cadastrar = ft.TextField(
                    hint_text='Senha',
                    width=300,
                    bgcolor='#a1afb8',
                    border_color='#a1afb8',
                    password=True,
                    can_reveal_password=True,
                    prefix_icon=ft.icons.KEY,
                    text_style=ft.TextStyle(font_family='Arial', size=15)
                )
    
    # Variável recebe a caixa de diálogo onde o usuário pode inserir o código enviado ao email para restaurar sua senha.
    entry_codigo_senha = ft.TextField(
                    hint_text='Código',
                    width=300,
                    bgcolor='#a1afb8',
                    border_color='#a1afb8',
                    prefix_icon=ft.icons.LOCK_OPEN,
                    text_style=ft.TextStyle(font_family='Arial', size=15)
                )
    
    # Variável recebe a caixa de diálogo onde o usuário pode inserir sua nova senha.
    entry_nova_senha = ft.TextField(
                    hint_text='Senha',
                    width=300,
                    bgcolor='#a1afb8',
                    border_color='#a1afb8',
                    prefix_icon=ft.icons.KEY,
                    text_style=ft.TextStyle(font_family='Arial', size=15),
                    password=True,
                    can_reveal_password=True
                )
    
    # Variável recebe a caixa de diálogo onde o usuário pode confirmar sua nova senha.
    entry_nova_senha_confirmar = ft.TextField(
                    hint_text='Confirmar senha',
                    width=300,
                    bgcolor='#a1afb8',
                    border_color='#a1afb8',
                    prefix_icon=ft.icons.KEY,
                    text_style=ft.TextStyle(font_family='Arial', size=15),
                    password=True,
                    can_reveal_password=True
                )
    

    # Função responsável por exibir os banners na interface, por exemplo, "Conta criada com sucesso".
    def banners(string, cor='red'):
        mensagem = string

        def fechar_banner():
            page.banner.open = False
            page.update()

        page.banner = ft.Banner(
            content=ft.Text(
                value=mensagem,
                color='white',
                text_align='center',
            ),
            actions=[ft.TextButton(text='Ok', on_click=fechar_banner)],
            bgcolor=cor
        )
        page.banner.open = True
        page.update()
        sleep(4)
        fechar_banner()
    

    # Função responsável por gerar uma senha hash.
    def hash_senha(senha):
        return hashlib.sha256(senha.encode()).hexdigest()
    

    # Função responsável por transformar a senha que o usuário digitou em um hash, para verificar se o hash 
    # da senha que o usuário digitou é igual à senha hash que está no banco de dados."
    def verificar_senha(senha_usuario):
        hash = hash_senha(senha_usuario)
        return hash

    
    # Função responsável por executar todos os comandos referente ao banco de dados SQL, inserir dados, manipular...
    def execucoes_sql(query, params=(), fetchone=False):
        resultado = None

        conexao = sqlite3.connect('logins.db')
        cursor = conexao.cursor()
        criar_tabela = """CREATE TABLE IF NOT EXISTS cadastros (
                        id INTEGER PRIMARY KEY,
                        nome VARCHAR(100) NOT NULL,
                        email VARCHAR(100) NOT NULL,
                        senha VARCHAR(64) NOT NULL
                        )"""
        cursor.execute(criar_tabela)
        
        if 'INSERT INTO' in query:
            try:
                cursor.execute(query, params)
                conexao.commit()
                banners('Conta cadastrada com sucesso!', 'green')
                page.go('/')
            
            except sqlite3.Error:
                banners('Ocorreu um erro inesperado, tente novamente ou mais tarde!')
        
        elif fetchone:
            try:
                cursor.execute(query, params)
                conexao.commit()
                resultado = cursor.fetchone() 
                return resultado
            
            except sqlite3.Error:
                banners('Ocorreu um erro inesperado, tente novamente ou mais tarde!')
        else:
            try:
                cursor.execute(query, params)
                conexao.commit()
            
            except sqlite3.Error:
                banners('Ocorreu um erro inesperado, tente novamente ou mais tarde!')
    

    # Função chamada quando o usuário preenche os dados e clica no botão "Criar conta".
    def click_cadastrar(e):
        # Variáveis recebem os valores das caixas de dialogo, onde usuario inseriu seu nome, email e senha.
        nome = entry_nome_cadastrar.value.strip().title()
        email_usuario = entry_email_cadastrar.value.lower()
        senha = entry_senha_cadastrar.value

        # Validações...
        if len(nome.replace(' ', '')) > 100 or nome.isdigit() or nome == '':
            entry_nome_cadastrar.error_text = 'Insira um nome válido!'
            page.update()
        
        elif '@' not in email_usuario or '.' not in email_usuario or ' ' in email_usuario or email_usuario == '':
            entry_email_cadastrar.error_text = 'Insira um email válido!'
            page.update()
        
        elif len(senha) < 10 or len(senha) > 20 or senha == '':
            if len(senha) < 10:
                entry_senha_cadastrar.error_text = 'A senha deve conter no mínimo 10 caracteres'
                page.update()
            elif len(senha) > 20:
                entry_senha_cadastrar.error_text = 'A senha deve conter no máximo 20 caracteres'
                page.update()
            else:
                entry_senha_cadastrar.error_text = 'Insira uma senha válida!'
                page.update()

        else:
            cadastro = execucoes_sql('SELECT email FROM cadastros WHERE email = ?', (email_usuario,), fetchone=True)
            
            if cadastro:
                banners('Oops! Este endereço de e-mail já está registrado em nossa plataforma.')
            else:
                senha_hash = hash_senha(senha)
                cadastro = execucoes_sql('INSERT INTO cadastros (nome, email, senha) VALUES (?, ?, ?)', (nome, email_usuario, senha_hash))

    
    # Função chamada quando o usuário preenche os dados de login e clica no botão "Entrar".
    def click_entrar(e):
        global email_usuario
        # Variáveis recebem os valores das caixas de dialogo, onde usuario inseriu seu email e senha.
        email_usuario = entry_email_login.value.lower()
        senha = entry_senha_login.value

        # Esvaziar as caixas de diálogo.
        entry_email_login.value = None
        entry_senha_login.value = None
        page.update()
        
        # Validações...
        if '@' not in email_usuario or '.' not in email_usuario or ' ' in email_usuario or email_usuario == '':
            entry_email_login.error_text = 'Insira um email válido!'
            page.update()
        
        elif len(senha) < 10 or len(senha) > 20 or senha == '':
            entry_senha_login.error_text = 'A senha deve conter no mínimo 12 caracteres e no máximo 20'
            page.update()
        
        else:
            senha_hash = verificar_senha(senha)
            login = execucoes_sql('SELECT email, senha FROM cadastros WHERE email = ? AND senha = ?', (email_usuario, senha_hash), fetchone=True)

            if not login:
                banners('Oops! Parece que o email ou a senha que você digitou estão '
                        'incorretos. Por favor, verifique e tente novamente.')
            else:
                page.go('/logou')
                banners('Logado com sucesso!', cor='green')


    # Função chamada quando o usuário preenche o email para restaurar a senha, e clica no botão "Enviar código".
    def click_enviar_codigo(e):
        global codigo
        global email_usuario
        # Variável recebe o valor da caixa de dialogo, onde usuario inseriu seu email.
        email_usuario = entry_email_login.value.lower()
        
        # Validação.
        if '@' not in email_usuario or '.' not in email_usuario or ' ' in email_usuario or email_usuario == '':
            entry_email_login.error_text = 'Insira um email válido!'
            page.update()
        else:
            conta = execucoes_sql('SELECT nome, email FROM cadastros WHERE email = ?', (email_usuario,), fetchone=True)

            # Se o endereço de e-mail fornecido existir no banco de dados, um e-mail será enviado para ele, contendo o código de confirmação.
            if conta:
                page.go('/enviou-codigo')
                
                nome = conta[0]
                numeros = [randint(0, 5) for _ in range(5)]
                codigo = ''.join(map(str, numeros))
                
                corpo_email = f"""
                <p>Caro(a) <b>{nome}</b>,</p>
                <p>Você solicitou a redefinição da sua senha de acesso.</p>
                <p>Copie o código abaixo para redefinir sua senha:</p>
                <p><b>{codigo}</b></p>
                """

                msg = email.message.Message()
                msg['Subject'] = "Sistema de Login - Recuperação de Senha"
                msg['From'] = 'victorpago10@gmail.com'
                msg['To'] = email_usuario
                password = 'naftpwwzysydpkdr' 
                msg.add_header('Content-Type', 'text/html; charset=utf-8')
                msg.set_payload(corpo_email )

                s = smtplib.SMTP('smtp.gmail.com: 587')
                s.starttls()

                s.login(msg['From'], password)
                s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

                banners('Código enviado para a caixa de entrada do seu email!', cor='green')

            else:
                banners('Esse email não está cadastrado em nossa plataforma, portanto, não é possível '
                        'você recuperar sua senha')   

    # Função chamada quando o usuário preenche o código para redefinir a senha, e clica no botão "Confirmar".
    def click_confirmar_codigo(e):
        # Váriavel recebe o valor da caixa de diálogo, onde o usuário inseriu o código.
        codigo_usuario = entry_codigo_senha.value

        # Validações...
        if len(codigo_usuario) != 5 or not codigo_usuario.isdigit() or codigo_usuario == '' or codigo_usuario != codigo:
            entry_codigo_senha.error_text = 'Código inválido!'
            page.update()
        else:
            page.go('/confirmou-codigo')

    # Função chamada quando o usuário preenche novas senhas e clica no botão "Redefinir senha".
    def click_redefinir_senha(e):
        # Variáveis recebem os valores das caixas de dialogo, onde usuario inseriu as senhas.
        senha = entry_nova_senha.value
        senha2 = entry_nova_senha_confirmar.value

        # Validações
        if len(senha) < 10 or len(senha) > 20 or senha == '' or senha != senha2:
            if senha != senha2:
                banners('As senhas dos dois campos devem ser iguais!')
            if len(senha) < 10:
                entry_nova_senha.error_text = 'A senha deve conter no mínimo 10 caracteres'
                page.update()
            elif len(senha) > 20:
                entry_nova_senha.error_text = 'A senha deve conter no máximo 20 caracteres'
                page.update()
            else:
                entry_nova_senha.error_text = 'Insira uma senha válida!'
                page.update()
        else:
            senha_hash = hash_senha(senha)
            execucoes_sql('UPDATE cadastros SET senha = ? WHERE email = ?', (senha_hash, email_usuario,))
            
            banners('Sua senha foi redefinida com sucesso!', cor='green')
            page.go('/')


    # Função responsável por trocar a página de navegação (página de login, de cadastro, redefinição de senha...)
    def mudanca_rota(route):
        page.views.clear()
        page.views.append(
            ft.View(
                # Página principal (página de login).
                route='/',
                controls=[
                    ft.Container(
                        bgcolor=ft.colors.WHITE,
                        height=500,
                        width=640,
                        border_radius=20,
                        shadow=ft.BoxShadow(color=ft.colors.BLACK, blur_radius=20),
                        content=ft.Column(
                            controls=[
                                ft.Image('icons/perfil.png', width=130, height=130),
                                ft.Container(
                                    ft.Text(value='ENTRAR', font_family='Alumni Sans', size=45, color='#4c5962'),
                                    padding=ft.padding.only(0, -15)
                                ),
                                ft.Text(value='Por favor, faça login para usar a plataforma', font_family='Arial', size=12, color='#506370'),
                                entry_email_login,
                                entry_senha_login,
                                ft.Container(
                                    content=ft.TextButton(
                                        text='Esqueci minha senha',
                                        scale=0.8,
                                        style=ft.ButtonStyle(color='#43474e'),
                                        on_click=lambda _: page.go('/esqueceu-senha')
                                    ),
                                    padding=ft.padding.only(190, -5)
                                ),
                                ft.Container(
                                    ft.ElevatedButton(
                                        text='Entrar',
                                        bgcolor='#24aea6',
                                        color='#275757',
                                        width=200,
                                        on_click=click_entrar
                                    ),
                                    padding=ft.padding.only(0,-3)
                                ),
                                ft.TextButton(text='Criar uma conta', on_click=lambda _: page.go('/criar')),
                            ],
                            alignment='center',
                            horizontal_alignment='center'
                        ),
                        gradient=ft.LinearGradient(
                            colors=[ft.colors.WHITE, '#a1afb8'],
                            begin=ft.alignment.top_right,
                            end=ft.Alignment(1, 1)                   
                        )
                    )              
                ],
                bgcolor='#405a6b',
                horizontal_alignment='center',
                vertical_alignment='center',
                
            )
        )

        entries = [
            entry_nome_cadastrar,
            entry_email_cadastrar,
            entry_senha_cadastrar,
            entry_codigo_senha,
            entry_nova_senha,
            entry_nova_senha_confirmar
        ]

        # Esvaziar as caixas de diálogo do nome, email, senha, codigo, e novas senhas.
        for entry in entries:
            if hasattr(entry, 'error_text'):
                entry.error_text = None
            if hasattr(entry, 'value'):
                entry.value = None

        page.update()    
       
        if page.route == '/criar':
            page.views.append(
                ft.View(
                    # Página de cadastro.
                    route='/criar',
                    controls=[
                        ft.Container(
                            bgcolor=ft.colors.WHITE,
                            height=500,
                            width=640,
                            border_radius=20,
                            shadow=ft.BoxShadow(color=ft.colors.BLACK, blur_radius=20),
                            content=ft.Column(
                                controls=[
                                    ft.Image('icons/perfil.png', width=130, height=130),
                                    ft.Container(
                                    ft.Text(value='CADASTRAR', font_family='Alumni Sans', size=45, color='#4c5962'),
                                    padding=ft.padding.only(0, -20)
                                ),
                                    entry_nome_cadastrar,
                                    entry_email_cadastrar,
                                    entry_senha_cadastrar,
                                    ft.Container(
                                    ft.ElevatedButton(
                                        text='Criar conta',
                                        bgcolor='#24aea6',
                                        color='#275757',
                                        width=200,
                                        on_click=click_cadastrar
                                    ),
                                    padding=ft.padding.only(0,10)
                                ),
                                    ft.TextButton(text='Já tenho uma conta', on_click=lambda _: page.go('/')),
                                ],
                                alignment='center',
                                horizontal_alignment='center'
                            ),
                            gradient=ft.LinearGradient(
                                colors=[ft.colors.WHITE, '#a1afb8'],
                                begin=ft.alignment.top_right,
                                end=ft.Alignment(0.8, 1)
                            )
                            
                        )
                    ],
                    bgcolor='#405a6b',
                    horizontal_alignment='center',
                    vertical_alignment='center'
                )
            )

        entries = [
            entry_email_login,
            entry_senha_login
        ]

        # Esvaziar as caixas de diálogo de email e senha na página de login.
        for entry in entries:
            if hasattr(entry, 'error_text'):
                entry.error_text = None
            if hasattr(entry, 'value'):
                entry.value = None   
        
        page.update()

        if page.route == '/logou':
            page.views.clear()
            page.views.append(
                ft.View(
                    # Página após fazer login (logou na conta).
                    route='/logou',
                    controls=[ft.Container(
                        bgcolor=ft.colors.WHITE,
                        height=500,
                        width=640,
                        border_radius=20,
                        shadow=ft.BoxShadow(color=ft.colors.BLACK, blur_radius=20),
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    value=f'Olá!\nSeu email: {email_usuario}',
                                    color='black',
                                    font_family='Arial'
                                ),
                                ft.IconButton(
                                    icon=ft.icons.LOGIN,
                                    icon_color='black',
                                    on_click=lambda _: page.go('/')
                                )
                            ],
                            alignment="center",
                            horizontal_alignment="center"
                        )
                    )],
                    bgcolor='#405a6b',
                    horizontal_alignment='center',
                    vertical_alignment='center'
                )
            )
            page.update()

        if page.route == '/esqueceu-senha':
            page.views.clear()
            page.views.append(
                ft.View(
                    # Página para redefinição da senha (esqueceu a senha)
                    route='/esqueceu-senha',
                    controls=[
                        ft.Container(
                            gradient=ft.LinearGradient(
                                colors=[ft.colors.WHITE, '#a1afb8'],
                                begin=ft.alignment.top_right,
                                end=ft.Alignment(1, 1) 
                            ),
                            bgcolor=ft.colors.WHITE,
                            height=500,
                            width=640,
                            border_radius=20,
                            shadow=ft.BoxShadow(color=ft.colors.BLACK, blur_radius=20),
                            content=ft.Column(
                                controls=[
                                    ft.Container(ft.Icon(name=ft.icons.LOCK_RESET, size=150, color='#535f68')),
                                    ft.Container(
                                        ft.Text(
                                            'Esqueceu sua senha?',
                                            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                            theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                            font_family='Arial',
                                            color='#535f68',
                                            size=20
                                        )
                                    ),
                                    ft.Container(
                                        ft.Text(
                                            'Por favor, insira seu email para enviarmos um código para você '
                                            'redefinir sua senha.',
                                            size=12,
                                            font_family='Arial',
                                            color='#506370'
                                        ),
                                        padding=ft.padding.only(0, 5)
                                    ),
                                    ft.Container(
                                        entry_email_login,
                                        padding=ft.padding.only(0, 5)
                                    ),
                                    ft.Container(
                                        ft.ElevatedButton(
                                            text='Enviar código',
                                            bgcolor='#24aea6',
                                            color='#275757',
                                            width=150,
                                            height=35,
                                            on_click=click_enviar_codigo
                                        ),
                                        padding=ft.padding.only(0, 5)
                                    ),
                                    ft.Container(
                                        ft.TextButton(
                                            text='Cancelar',
                                            on_click=lambda _: page.go('/')
                                        )
                                    )
                                ],
                                alignment="center",
                                horizontal_alignment="center"
                            )
                        )
                    ],
                    bgcolor='#405a6b',
                    horizontal_alignment='center',
                    vertical_alignment='center'
                )
            )
            page.update()

        if page.route == '/enviou-codigo':
            page.views.clear()
            page.views.append(
                ft.View(
                    # Página para inserir o código enviado ao email.
                    route='/enviou-codigo',
                    controls=[
                        ft.Container(
                            gradient=ft.LinearGradient(
                                colors=[ft.colors.WHITE, '#a1afb8'],
                                begin=ft.alignment.top_right,
                                end=ft.Alignment(1, 1) 
                            ),
                            bgcolor=ft.colors.WHITE,
                            height=500,
                            width=640,
                            border_radius=20,
                            shadow=ft.BoxShadow(color=ft.colors.BLACK, blur_radius=20),
                            content=ft.Column(
                                controls=[
                                    ft.Container(ft.Icon(name=ft.icons.LOCK_RESET, size=150, color='#535f68')),
                                    ft.Container(
                                        ft.Text(
                                            'Insira o código',
                                            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                            theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                            font_family='Arial',
                                            color='#535f68',
                                            size=20
                                        )
                                    ),
                                    ft.Container(
                                        ft.Text(
                                            'Por favor, insira o código abaixo para você redefinir sua senha',
                                            size=12,
                                            font_family='Arial',
                                            color='#506370'
                                        ),
                                        padding=ft.padding.only(0, 5)
                                    ),
                                    ft.Container(
                                        entry_codigo_senha,
                                        padding=ft.padding.only(0, 5)
                                    ),
                                    ft.Container(
                                        ft.ElevatedButton(
                                            text='Confirmar',
                                            bgcolor='#24aea6',
                                            color='#275757',
                                            width=150,
                                            height=35,
                                            on_click=click_confirmar_codigo
                                        ),
                                        padding=ft.padding.only(0, 5)
                                    ),
                                    ft.Container(
                                        ft.TextButton(
                                            text='Cancelar',
                                            on_click=lambda _: page.go('/')
                                        )
                                    )
                                ],
                                alignment="center",
                                horizontal_alignment="center"
                            )
                        )
                    ],
                    bgcolor='#405a6b',
                    horizontal_alignment='center',
                    vertical_alignment='center'
                )
            )
            page.update()

        if page.route == '/confirmou-codigo':
            page.views.clear()
            page.views.append(
                ft.View(
                    # Página para inserir as novas senhas.
                    route='/confirmou-codigo',
                    controls=[
                        ft.Container(
                            gradient=ft.LinearGradient(
                                colors=[ft.colors.WHITE, '#a1afb8'],
                                begin=ft.alignment.top_right,
                                end=ft.Alignment(1, 1) 
                            ),
                            bgcolor=ft.colors.WHITE,
                            height=500,
                            width=640,
                            border_radius=20,
                            shadow=ft.BoxShadow(color=ft.colors.BLACK, blur_radius=20),
                            content=ft.Column(
                                controls=[
                                    ft.Container(ft.Icon(name=ft.icons.LOCK_RESET, size=150, color='#535f68')),
                                    ft.Container(
                                        ft.Text(
                                            'Redefina sua senha',
                                            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                                            theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                            font_family='Arial',
                                            color='#535f68',
                                            size=20
                                        )
                                    ),
                                    ft.Container(
                                        ft.Text(
                                            'Por favor, crie sua nova senha e insira-a novamente para confirmação',
                                            size=12,
                                            font_family='Arial',
                                            color='#506370'
                                        ),
                                        padding=ft.padding.only(0, 5)
                                    ),
                                    ft.Container(
                                        content=ft.Column([entry_nova_senha, entry_nova_senha_confirmar]),
                                        padding=ft.padding.only(0, 5)
                                    ),
                                    ft.Container(
                                        ft.ElevatedButton(
                                            text='Redefinir senha',
                                            bgcolor='#24aea6',
                                            color='#275757',
                                            width=150,
                                            height=35,
                                            on_click=click_redefinir_senha
                                        ),
                                        padding=ft.padding.only(0, 5)
                                    ),
                                    ft.Container(
                                        ft.TextButton(
                                            text='Cancelar',
                                            on_click=lambda _: page.go('/')
                                        )
                                    )
                                ],
                                alignment="center",
                                horizontal_alignment="center"
                            )
                        )
                    ],
                    bgcolor='#405a6b',
                    horizontal_alignment='center',
                    vertical_alignment='center'
                )
            )
            page.update()


    page.on_route_change = mudanca_rota
    page.go('/')

ft.app(target=sistema_login, assets_dir="assets")