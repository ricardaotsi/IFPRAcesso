from django.db import models

class Identificador(models.Model):
    nome_id = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nome_id
        
class Pessoa(models.Model):
    nome_pessoa = models.CharField(max_length=50, unique=True)
    id_pessoa = models.ForeignKey(Identificador, on_delete=models.PROTECT)
    cracha_pessoa = models.IntegerField(unique=True)
    matricula_pessoa = models.BigIntegerField(unique=True)
    ano_entrada = models.IntegerField()
    ativo = models.CharField(max_length=1, default="S")
    def __str__(self):
        return self.nome_pessoa
