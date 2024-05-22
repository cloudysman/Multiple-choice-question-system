from django.db import models

class ClassCode(models.Model):
    join_code = models.CharField(max_length=100, unique=True)
    student_code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.join_code} - {self.student_code}"

class Quiz(models.Model):
    join_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
