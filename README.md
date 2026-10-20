# Cadastro e reconhecimento facial

Aplicação local com Flask que usa a webcam do navegador para cadastrar e
reconhecer um rosto.

## Importante: o GitHub não executa o aplicativo

A página do repositório no GitHub mostra este README e os arquivos do projeto.
Ela não inicia o servidor Flask nem acessa a webcam. Para usar a câmera e o
reconhecimento facial, execute o servidor no seu computador seguindo os passos
abaixo e abra `http://127.0.0.1:5000` no navegador. O endereço só funciona
enquanto o servidor estiver rodando no seu computador.

## Requisitos

- Python 3.10 ou superior
- Webcam e navegador com permissão para acessar a câmera
- Acesso à internet durante a instalação das dependências

## Instalação no Windows

1. Baixe o projeto pelo botão **Code → Download ZIP** no GitHub e extraia o
   arquivo, ou clone o repositório:

   ```powershell
   git clone https://github.com/Apx-Empresa/AC_FACE.git
   cd AC_FACE
   ```

2. No VS Code, abra a pasta que contém `app.py` e abra um terminal nela.
3. Execute os comandos:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Se o PowerShell bloquear a ativação do ambiente virtual, use diretamente o
Python dele:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

4. Deixe o terminal aberto. Quando aparecer `Site iniciado em
   http://127.0.0.1:5000`, abra esse endereço no navegador.
5. Clique em **Iniciar câmera** e permita o acesso à webcam. Digite o nome da
   pessoa e clique em **Cadastrar rosto**. Depois, o site tenta reconhecer o
   rosto cadastrado automaticamente.

Para encerrar o servidor, volte ao terminal e pressione `Ctrl+C`.

### Problemas de instalação no Windows

`face-recognition` usa `dlib`, que pode precisar do CMake e das ferramentas de
compilação C++ do Visual Studio. Se a instalação falhar durante a compilação
de `dlib`, instale esses componentes e repita `pip install -r requirements.txt`.

Se o navegador mostrar `ERR_CONNECTION_REFUSED`, o servidor não está rodando:
confira o terminal, execute `python app.py` na pasta correta e mantenha-o aberto.

O cadastro facial é salvo localmente em `cadastro_facial.json`. Esse arquivo
contém dados biométricos e está excluído do Git por segurança. Não o publique.

## Observação de segurança

Esta demonstração faz reconhecimento facial, mas não inclui detecção de
vivacidade e pode ser enganada por uma foto ou vídeo. Não a utilize como único
controle de acesso em ambientes de produção.
