# Instalação
É necessário ter o Python 3.6 ou mais instalado para poder rodar o projeto. Você pode acessar o site oficial https://www.python.org/downloads/ para poder fazer o download.

Após ter o Python instalado, crie uma pasta e depois navegue até ela no seu terminal.

### Virtual environment
Acho bacana a ideia de criar um ambiente virtual para organizar bem o projeto, você pode pular essa parte se achar necessário!

1 - Dentro da pasta criada, digite no terminal
```sh
$ python3 -m venv bot-env
```

2 - Ative o ambiente usando
```sh
$ source bot-env/bin/activate
```
No Windows você pode ativar utilizando
```sh
$ bot-env\Scripts\activate.bat
```

3 - Entre na pasta chamada include ou Include.
Você deverá colocar os arquivo do bot dentro desta pasta!

### Mão na massa
Clone o repositório e digite o comando
```sh
$ pip3 install -r requirements.txt
```
Isso fará com que todas as dependências do projeto sejam baixadas.

Agora é necessário criar o arquivo  `.env` e colocar as variáveis `BOT_DISCORD_TOKEN` que precisará ter o token de autorização do BOT que pode ser pego criando uma aplicação e no discord (você pode seguir este [passo a passo](https://discordpy.readthedocs.io/en/latest/discord.html) de como criar uma aplicação e um BOT da documentação do wrapper em que estamos utilizando), e `BOT_PREFIX` que será o prefixo dos comandos do BOT, segue um exemplo:
```
BOT_PREFIX=.
BOT_DISCORD_TOKEN=toKeN.doBoT-.Aqui
```

Prontinho, agora basta digitar `python3 main.py` que BOT irá ligar!

## Nota
No link que deixamos para a criação da aplicação e do BOT, também é dito como convida o BOT para o seu servidor para que você possa testar perfeitamente!

Se o BOT não enviar uma mensagem assim que entrar no servidor, tente menciona-lo, se não responder, verifique as permissões do BOT!
