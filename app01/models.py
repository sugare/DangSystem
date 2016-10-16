from django.db import models
from django.contrib.auth.models import User

class single(models.Model):
    content = models.CharField(max_length=200)
    question_ans = models.IntegerField()

    def __str__(self):
        return self.content


class sin_ans(models.Model):
    question = models.ForeignKey(single, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    mask = models.IntegerField()

    def __str__(self):
        return self.content


class multi(models.Model):
    content = models.CharField(max_length=200)
    question_ans = models.IntegerField()

    def __str__(self):
        return self.content


class mul_ans(models.Model):
    question = models.ForeignKey(multi, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    mask = models.IntegerField()

    def __str__(self):
        return self.content


class judge(models.Model):
    content = models.CharField(max_length=200)
    question_ans = models.IntegerField()

    def __str__(self):
        return self.content


class rec(models.Model):
    # user_id = models.CharField(max_length=15)
    username = models.ForeignKey(User)
    question_id = models.CharField(max_length=15)
    user_rec = models.CharField(max_length=10)

    def __str__(self):
        return self.question_id


class mask(models.Model):
    user_id = models.CharField(max_length=15)
    username = models.CharField(max_length=15)
    s_mask = models.IntegerField(default=0)
    m_mask = models.IntegerField(default=0)
    j_mask = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.user_id


class survey_data(models.Model):
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.content


class survey_choice(models.Model):
    question = models.ForeignKey(survey_data, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    mask = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text




