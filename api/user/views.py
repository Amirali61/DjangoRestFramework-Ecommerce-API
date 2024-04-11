from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CostumUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model,login,logout
from django.views.decorators.csrf import csrf_exempt
import random
import re

# Create your views here.

def generate_session_token(length=10):
    chars = [chr(i) for i in range(97,123)]
    strs = [str(i) for i in range(10)]
    token = ''
    for _ in range(length):
        token += random.SystemRandom().choice(chars+strs)
    return token

''' create signin function '''
@csrf_exempt
def signin(request):
    if  not request.method=='POST':
        return JsonResponse({'error':'send a post request with valid parameters'})
    username = request.POST['email']
    password = request.POST['password']

    if not re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',username):
        return JsonResponse({'error':'enter a valid email'})
    if len(password) <5:
        return JsonResponse({'error':'your password is too short'})
    
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)
        if user.check_password(password):
            user_dict = UserModel.objects.filter(email=username).values().first()
            user_dict.pop('password')
            if user.session_token != '0':
                user.session_token = '0'
                user.save()
                return JsonResponse({'error':'session already exists'})
            token = generate_session_token()
            user.session_token = token
            user.save()
            login(request=request,user=user)
            return JsonResponse({'token':token,'user':user_dict})
        else:
            return JsonResponse({'error':'wrong password'})
        
    except UserModel.DoesNotExist:
        return JsonResponse({'error':'invalid email address'})
    

''' create signout function '''
@csrf_exempt
def signout(request,id):
    logout(request=request)

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = '0'
        user.save()
    except UserModel.DoesNotExist:
        return JsonResponse({'error':'user id does not exist'})
    
    return JsonResponse({'success':'logout success'})




''' User viewset to use in router '''
class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create':[AllowAny]}
    queryset = CostumUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]