from django.db import models
from apps.projectmodule.models import ProjectsAbstract


class PythonVersions(models.Model):
    version = models.CharField(verbose_name='python版本', max_length=15)


class PythonProjects(ProjectsAbstract):
    pass




