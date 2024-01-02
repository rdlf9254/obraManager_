from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class projeto(models.Model):
    STATUS_CHOICES = [
        (0, 'Em espera'),
        (1, 'No Prazo'),
        (2, 'Concluído'),
        (3, 'Atrasado'),
    ]

    STAGE_CHOICES = [
        (0, 'Anteprojeto'),
        (1, 'Planejamento'),
        (2, 'Projeto Básico'),
        (3, 'Licenciamento'),
        (4, 'Mobilização'),
        (5, 'Fundação'),
        (6, 'Estrutura'),
        (7, 'Alvenaria'),
        (8, 'Telhado'),
        (9, 'Hidráulica'),
        (10, 'Elétrica'),
        (11, 'Revestimento Interno'),
        (12, 'Revestimento Externo'),
    ]
    
    proId = models.AutoField(primary_key=True)
    proName = models.CharField(max_length=255)
    proAddress = models.TextField()
    proStatus = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    proCreatedAt = models.DateTimeField(default=timezone.now)
    proLastUpdate = models.DateTimeField(auto_now=True)
    proStage = models.PositiveSmallIntegerField(choices=STAGE_CHOICES)
    proResponsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='responsaveis')
    proGeneralProgress = models.IntegerField()
    proStageProgress = models.IntegerField()
    proNextStageProgress = models.IntegerField()
    proTotalTasks = models.IntegerField()
    proDoneTasks = models.IntegerField()
    proDoingTasks = models.IntegerField()
    proUseCreator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='criadores')

    class Meta:
        db_table = 'projeto'

    def __str__(self):
        return self.proName

class usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    USER_TYPE_CHOICES = [
        (1, 'Administrador'),
        (2, 'Engenheiro'),
        (3, 'MestreObras'),
        (4, 'Cliente'),
    ]
    useType = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=4)
    usePhoto = models.TextField(null=True, blank=True)

    useProjects = models.ManyToManyField(projeto, blank=True)

    class Meta:
        db_table = 'usuario'


    def __str__(self):
        return self.user.username

class fotoProjeto(models.Model):
    phoId = models.AutoField(primary_key=True)
    phoBase = models.TextField()  
    phoCreatedAt = models.DateTimeField(auto_now_add=True)
    phoProjId = models.ForeignKey(projeto, related_name='photos', on_delete=models.CASCADE)

    class Meta:
        db_table = 'fotoProjeto'

class dataGrafico(models.Model):
    graId = models.AutoField(primary_key=True)
    graDate = models.DateTimeField(auto_now_add=True)
    graValue = models.FloatField()
    graProjId = models.ForeignKey(projeto, related_name='graph_data', on_delete=models.CASCADE)
    class Meta:
        db_table = 'dataGrafico'

class visualizarProjeto(models.Model):
    visId = models.AutoField(primary_key=True)
    visCreatedAt = models.DateTimeField(auto_now_add=True)
    visUserId = models.ForeignKey(usuario, related_name='project_views', on_delete=models.CASCADE)
    visProjId = models.ForeignKey(projeto, related_name='viewed_by', on_delete=models.CASCADE)
    class Meta:
        db_table = 'visualizarProjeto'
