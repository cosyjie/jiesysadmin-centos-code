from django.db import models


class ProjectsAbstract(models.Model):
    title = models.CharField(verbose_name='项目名称', max_length=250)
    project_path = models.CharField(verbose_name='项目路径', max_length=1000)
    project_language = models.CharField(verbose_name='开发语言', max_length=20)

    class Meta:
        abstract = True


