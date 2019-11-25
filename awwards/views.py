from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from .models import Project, Rate, Review
from django.contrib.auth.models import User
from .forms import( UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProjectPostForm, RateForm, ReviewForm)
from django.contrib.auth.decorators import login_required




