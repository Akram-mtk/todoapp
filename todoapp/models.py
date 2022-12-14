from django.db import models

class Person(models.Model):
    user_name = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.user_name


class Task(models.Model):
    task_content = models.CharField(max_length=100)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.owner) + " / " + self.task_content