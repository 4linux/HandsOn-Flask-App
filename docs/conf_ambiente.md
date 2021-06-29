# Configurações do ambiente

Nossa Configuração inicial consiste em clonar o reposítorio no github e criar o ambiente virtual.


## Clonando o reposítorio

acesse o repositorio em `https://github.com/4linux/HandsOn-Flask-App`
clique em clone e copie o link do repositorio.
vá até seu diretorio desejado e use `git clone <link-repositorio>`.

## Criando o ambiente virtual e instalando a dependências.

bom, agora que temos o projeto clonado na nossa máquina precisamos criar nosso ambiente virtual, utilizaremos o virtualenv para isso.


para criar nosso ambiente virtual, entre no diretorio do projeto e execute:

- Linux: `virtualenv -p python3 venv`
- Windows `virtualenv .`

para ativa-lo:

- Linux: `source venv/bin/activate`
- Windows: `virtualenv .` 
