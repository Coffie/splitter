from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from .forms import SignUpForm
# from django.http import HttpResponse

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # user.refresh_from_db()
#             # user.userprofile.customer_id = form.cleaned_data.get('customer_id')
#             # user.userprofile.account_id = form.cleaned_data.get('account_id')
#             user.save()
#             # raw_password = form.cleaned_data.get('password')
#             # user = authenticate(username=user.username, password=user.raw_password)
#             login(request.user)
#             return HttpResponse("<h3>Success!!</h3>")
#     else:
#         form = SignUpForm()
#     return render(request, 'userprofile/signup.html', {'form': form})
