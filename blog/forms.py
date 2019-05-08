# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment,City,Location

class PostForm(forms.ModelForm):
    OUTERCHOICES = ((1,'롱패딩'),(2,'숏패딩'), (3,'코트'), (4,'자켓'),(5,'청자켓'), (6, '가디건'), (7, '후드집업'), 
    (8, '트렌치코트'), (9, '점퍼'), (10, '기타/없음'))
    TOPCHOICES=((1, '나시'), (2, '반팔'), (3, '긴팔'), (4, '후드/맨투맨'), (5, '셔츠'), (6, '기타/없음'))
    BOTTOMCHOICES=((1, '청바지'), (2, '면바지'), (3,'반바지'), (4, '기모바지'), (5, '스커트'), (6, '롱스커트'), (7, '원피스'),(8, '기타/없음'))
    ACCCHOICES = ((1, '모자'),(2, '목도리'), (3, '수면양말'),(4, '선글라스'),(5, '기타/없음'))
    top = forms.MultipleChoiceField(choices=TOPCHOICES, widget=forms.CheckboxSelectMultiple()) 
    bottom = forms.MultipleChoiceField(choices=BOTTOMCHOICES, widget=forms.CheckboxSelectMultiple()) 
    acc = forms.MultipleChoiceField(choices=ACCCHOICES, widget=forms.CheckboxSelectMultiple())
    outer = forms.MultipleChoiceField(choices=OUTERCHOICES, widget=forms.CheckboxSelectMultiple())  
    class Meta:
        model=Post
        fields=['body', 'title', 'outer', 'top', 'bottom', 'acc', 'image',]
                
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content', ]
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class' : 'cmcontent'})

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password',]
        
class CityForm(forms.ModelForm):
    class Meta:
        model = City 
        fields = ['name',]

class SignForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['user', 'location',]
        
   