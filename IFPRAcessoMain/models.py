from django.db import models

class Identificador(models.Model):
    nome_id = models.CharField(max_length=50)
    def __str__(self):
        return self.nome_id
        
class Pessoa(models.Model):
    nome_pessoa = models.CharField(max_length=50)
    id_pessoa = models.ForeignKey(Identificador, on_delete=models.PROTECT)
    cracha_pessoa = models.IntegerField()
    matricula_pessoa = models.IntegerField()
    ano_entrada = models.IntegerField()

