from django.shortcuts import render

def errorResponse(request,errorMsg):
    return render(request,'error.html',{
        'errorMsg':errorMsg
    })
