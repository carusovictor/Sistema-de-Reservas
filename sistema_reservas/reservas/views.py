from datetime import date, datetime

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Funcionario, Reserva, Sala


def dentro_do_horario_permitido(data_reserva: date, inicio: str, fim: str):
    """Retorna (ok, mensagem). Regras:
    - Segunda a sexta: 07:00 às 22:00
    - Sábado: 07:00 às 12:00
    - Domingo: proibido
    """
    if inicio >= fim:
        return False, 'O horário de início precisa ser menor que o horário de fim.'

    dia_semana = data_reserva.weekday()  # segunda=0, domingo=6

    if dia_semana <= 4:
        abertura, fechamento = '07:00', '22:00'
    elif dia_semana == 5:
        abertura, fechamento = '07:00', '12:00'
    else:
        return False, 'Não é permitido reservar salas aos domingos.'

    if inicio < abertura or fim > fechamento:
        return False, f'Horário inválido. Para essa data, as reservas são permitidas de {abertura} às {fechamento}.'

    return True, ''


def existe_conflito(sala_id: int, data_txt: str, inicio: str, fim: str):
    return Reserva.objects.filter(
        sala_id=sala_id,
        data=data_txt,
        status='ativa',
        hora_inicio__lt=fim,
        hora_fim__gt=inicio,
    ).exists()


def painel(request):
    if request.method == 'POST':
        sala_id = request.POST.get('sala_id')
        nome = request.POST.get('nome', '').strip()
        matricula = request.POST.get('matricula', '').strip()
        data_txt = request.POST.get('data')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fim = request.POST.get('hora_fim')

        if not all([sala_id, nome, matricula, data_txt, hora_inicio, hora_fim]):
            messages.error(request, 'Preencha todos os campos da reserva.')
            return redirect('painel')

        try:
            matricula_int = int(matricula)
            data_reserva = datetime.strptime(data_txt, '%Y-%m-%d').date()
            sala = Sala.objects.get(id=sala_id)
        except ValueError:
            messages.error(request, 'Matrícula ou data inválida.')
            return redirect('painel')
        except Sala.DoesNotExist:
            messages.error(request, 'Sala selecionada não existe.')
            return redirect('painel')

        ok, mensagem = dentro_do_horario_permitido(data_reserva, hora_inicio, hora_fim)
        if not ok:
            messages.error(request, mensagem)
            return redirect('painel')

        if existe_conflito(sala.id, data_txt, hora_inicio, hora_fim):
            messages.error(request, 'Essa sala já possui uma reserva ativa nesse intervalo de horário.')
            return redirect('painel')

        funcionario, criado = Funcionario.objects.get_or_create(
            matricula=matricula_int,
            defaults={'nome': nome},
        )

        if not criado and funcionario.nome != nome:
            funcionario.nome = nome
            funcionario.save(update_fields=['nome'])

        Reserva.objects.create(
            funcionario=funcionario,
            sala=sala,
            data=data_txt,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            status='ativa',
        )

        messages.success(request, 'Reserva criada com sucesso.')
        return redirect('painel')

    hoje = date.today().isoformat()
    agora = datetime.now().strftime('%H:%M')

    salas = Sala.objects.all()
    reservas_ativas = Reserva.objects.select_related('funcionario', 'sala').filter(status='ativa')
    reservas = reservas_ativas.order_by('data', 'hora_inicio')[:20]

    reservas_hoje = reservas_ativas.filter(data=hoje).count()
    em_uso_agora = reservas_ativas.filter(
        data=hoje,
        hora_inicio__lte=agora,
        hora_fim__gt=agora,
    ).count()

    salas_em_uso_ids = set(
        reservas_ativas.filter(
            data=hoje,
            hora_inicio__lte=agora,
            hora_fim__gt=agora,
        ).values_list('sala_id', flat=True)
    )

    total_salas = salas.count()
    salas_disponiveis = total_salas - len(salas_em_uso_ids)

    contexto = {
        'salas': salas,
        'reservas': reservas,
        'reservas_hoje': reservas_hoje,
        'total_salas': total_salas,
        'salas_disponiveis': salas_disponiveis,
        'em_uso_agora': em_uso_agora,
        'salas_em_uso_ids': salas_em_uso_ids,
    }
    return render(request, 'reservas/index.html', contexto)


@require_POST
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.status = 'cancelada'
    reserva.save(update_fields=['status'])
    messages.success(request, 'Reserva cancelada com sucesso.')
    return redirect('painel')
