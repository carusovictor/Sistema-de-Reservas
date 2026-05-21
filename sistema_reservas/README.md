# Sistema de Reservas de Salas

Sistema simples de reservas usando Django + SQLite.

## Como rodar

1. Abra a pasta `sistema_reservas` no terminal.
2. Crie um ambiente virtual, se quiser:

```bash
python -m venv venv
```

3. Ative o ambiente virtual:

Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

Windows CMD:

```bash
venv\Scripts\activate.bat
```

4. Instale o Django:

```bash
pip install -r requirements.txt
```

5. Rode o servidor:

```bash
python manage.py runserver
```

6. Acesse no navegador:

```txt
http://127.0.0.1:8000/
```

## Regras implementadas

- Segunda a sexta: reservas permitidas de 07:00 até 22:00.
- Sábado: reservas permitidas de 07:00 até 12:00.
- Domingo: bloqueado.
- O sistema bloqueia conflito de horário para a mesma sala, na mesma data.
- Se o funcionário não existir, ele é cadastrado automaticamente pela matrícula e nome informados.
- Se a matrícula já existir, o sistema usa o funcionário existente.
- Cancelar reserva muda o status para `cancelada`, sem apagar o histórico.

## Banco de dados

O arquivo `db.sqlite` já está dentro do projeto e contém as salas cadastradas.
