# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django import forms
# Create your models here. 


class Post(models.Model):
    OUTERCHOICES = ((1,'롱패딩'),(2,'숏패딩'), (3,'코트'), (4,'자켓'),(5,'청자켓'), (6, '가디건'), (7, '후드집업'), 
    (8, '트렌치코트'), (9, '점퍼'), (10, '기타/없음'))
    TOPCHOICES=((1, '나시'), (2, '반팔'), (3, '긴팔'), (4, '후드/맨투맨'), (5, '셔츠'), (6, '기타/없음'))
    BOTTOMCHOICES=((1, '청바지'), (2, '면바지'), (3,'반바지'), (4, '기모바지'), (5, '스커트'), (6, '롱스커트'), (7, '원피스'), (8, '기타/없음'))
    ACCCHOICES = ((1, '모자'),(2, '목도리'), (3, '수면양말'),(4, '선글라스'), (5, '기타/없음'))
    title = models.CharField(max_length=400)
    pub_date = models.DateTimeField(default=timezone.now)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=20)
    outer=models.CharField(max_length=255)
    top=models.CharField(max_length=255)
    bottom=models.CharField(max_length=255)
    acc=models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True)
    
    def get_outer_str_list(self):
        clist = dict(self.OUTERCHOICES)
        outers = self.outer.replace('[', '').replace(']', '').replace('u', '').replace('\'', '').split(',')
        strlist = list()
        for outer in outers:
            strlist.append(clist.get(int(outer)))
        return strlist
        
    def get_top_str_list(self):
        clist = dict(self.TOPCHOICES)
        tops = self.top.replace('[', '').replace(']', '').replace('u', '').replace('\'', '').split(',')
        strlist = list()
        for top in tops:
            strlist.append(clist.get(int(top)))
        return strlist
        
    def get_bottom_str_list(self):
        clist = dict(self.BOTTOMCHOICES)
        bottoms = self.bottom.replace('[', '').replace(']', '').replace('u', '').replace('\'', '').split(',')
        strlist = list()
        for bottom in bottoms:
            strlist.append(clist.get(int(bottom)))
        return strlist
    
    def get_acc_str_list(self):
        clist = dict(self.BOTTOMCHOICES)
        accs = self.acc.replace('[', '').replace(']', '').replace('u', '').replace('\'', '').split(',')
        strlist = list()
        for acc in accs:
            strlist.append(clist.get(int(acc)))
        return strlist    
            
    
    
class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    author=models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content=models.TextField()
    time=models.DateTimeField(default=timezone.now)

class City(models.Model):
    name = models.CharField(max_length=200)

class Location(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    location=models.CharField(max_length=200)
    
