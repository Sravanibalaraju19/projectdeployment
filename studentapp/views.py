from django.shortcuts import render

#Create your views here.
def NameDisplay(request):
    return render(request, 'NameDisplay.html')

def StudentHomePage(request):
    return render(request, 'studentapp/StudentHomePage.html')




