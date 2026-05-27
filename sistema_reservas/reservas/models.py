from django.db import models
from django.contrib.auth.models import User


class PerfilProfessor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.first_name



class Funcionario(models.Model):
    matricula = models.IntegerField(primary_key=True)
    nome = models.TextField()

    class Meta:
        db_table = 'funcionarios'
        managed = False

    def __str__(self):
        return f'{self.nome} ({self.matricula})'

class Sala(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.TextField()
    capacidade = models.IntegerField()

    class Meta:
        db_table = 'salas'
        managed = False
        ordering = ['id']

    def __str__(self):
        return self.nome

class Reserva(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('cancelada', 'Cancelada'),
    ]

    id = models.AutoField(primary_key=True)
    funcionario = models.ForeignKey(
        Funcionario,
        db_column='funcionario_matricula',
        on_delete=models.CASCADE,
        related_name='reservas',
    )
    sala = models.ForeignKey(
        Sala,
        db_column='sala_id',
        on_delete=models.CASCADE,
        related_name='reservas',
    )
    data = models.TextField()
    hora_inicio = models.TextField()
    hora_fim = models.TextField()
    status = models.TextField(default='ativa', choices=STATUS_CHOICES)

    class Meta:
        db_table = 'reservas'
        managed = False
        ordering = ['data', 'hora_inicio']

    def __str__(self):
        return f'{self.sala} - {self.data} {self.hora_inicio}-{self.hora_fim}'
