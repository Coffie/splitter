from django.shortcuts import render, redirect

def index(request):
    user = request.user

    #TODO: Get necessary information to view
