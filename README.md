# Cadastro e reconhecimento facial

Aplicação local com Flask que usa a webcam do navegador para cadastrar e
reconhecer um rosto.

## Requisitos

- Python 3.10 ou superior
- Webcam e navegador com permissão para acessar a câmera

## Instalação no Windows

Abra o terminal na pasta do projeto e execute:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Abra http://127.0.0.1:5000, permita o acesso à webcam, clique em **Iniciar
câmera**, informe o nome e selecione **Cadastrar rosto**.

O cadastro facial é salvo localmente em `cadastro_facial.json`. Esse arquivo
contém dados biométricos e está excluído do Git por segurança. Não o publique.

## Observação de segurança

Esta demonstração faz reconhecimento facial, mas não inclui detecção de
vivacidade e pode ser enganada por uma foto ou vídeo. Não a utilize como único
controle de acesso em ambientes de produção.
