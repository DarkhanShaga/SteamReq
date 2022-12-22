from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    mailing_address = models.CharField(max_length=200, blank=True)
    gpu_model = models.ForeignKey('GPU', on_delete=models.CASCADE, null=True)
    cpu_model = models.ForeignKey('CPU', on_delete=models.CASCADE, null=True)
    ram_model = models.ForeignKey('RAM', on_delete=models.CASCADE, null=True)


class GPU(models.Model):
    gpu_name = models.CharField(max_length=40)
    teraflops = models.FloatField(null=True)

    def __str__(self):
        return self.gpu_name


class CPU(models.Model):
    cpu_name = models.CharField(max_length=40)
    gaming_rate = models.IntegerField(null=True)

    def __str__(self):
        return self.cpu_name


class RAM(models.Model):
    ram_amount = models.FloatField(null=True)

    def __str__(self):
        return str(self.ram_amount) + str(' GB')
