from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.views.decorators.csrf import csrf_exempt 
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from cryptography.fernet import Fernet
from .forms import PasswordResetForm
from . import serializers, models


key = Fernet.generate_key()
fernet = Fernet(key)


@csrf_exempt
@api_view(["GET","POST"]) 
@renderer_classes((JSONRenderer,))
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            serial_number = form.cleaned_data['serial_number']
            associated_user = get_user_model().objects.filter(serial_number=serial_number).first()
            if associated_user:
                encserial_number = fernet.encrypt(serial_number.encode()).decode()
                return Response({"serial_number": encserial_number},status.HTTP_302_FOUND)
    return Response({"message": "something went wrong."},status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(["GET", "POST"]) 
@renderer_classes((JSONRenderer,))
def passwordResetConfirm(request, serial_number):
    try:
        decserial_number = fernet.decrypt(serial_number.encode()).decode()
        user = get_user_model().objects.get(serial_number=decserial_number)
    except:
        user = None

    if user is not None:
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return Response({
                    "message": "Your password changed succesfuly",
                }, status.HTTP_204_NO_CONTENT)
        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form},status=406)
    return Response(
        {
            "message": "something went wrong"
        },
        status.HTTP_400_BAD_REQUEST
    )


class AllSettingsViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    serializer_class = serializers.AllSettingsSerializers
    permission_classes = [IsAuthenticated]
    lookup_field = 'user'
    

    def get_queryset(self):
        user = models.User.objects.filter(id=self.request.user.id).only('id')
        if self.request.user.is_staff:
            return models.AllSettings.objects.prefetch_related('thresholds').all()
        return models.AllSettings.objects.prefetch_related('thresholds').filter(user__in = user.values_list("id"))

    def get_serializer_context(self):
        return {"id" :self.request.user.id}
    

    def create(self, request, *args, **kwargs):
        serializer = serializers.AllSettingsSerializers(
                data=request.data,
                context={"id" :self.request.user.id})
        serializer.is_valid(raise_exception=True)
        settings = serializer.save()
        serializer = serializers.AllSettingsSerializers(settings)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        setting = models.AllSettings.objects.prefetch_related('thresholds').filter(user=self.request.user.id).only('changed')
        page = self.paginate_queryset(setting)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        if setting.exists():
            if setting.values()[0]['changed']:
                setting.update(changed=False)
                serializer = self.get_serializer(setting, many=True)
                return Response(serializer.data)
            return Response({'messages': "nothing changed"},status.HTTP_208_ALREADY_REPORTED)
        serializer = self.get_serializer(setting, many=True)
        return Response(serializer.data,status.HTTP_204_NO_CONTENT)


class ActiveViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ActiveAdminSerializer
    queryset = models.Active.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = models.User.objects.filter(id=self.request.user.id).only('id')
        if self.request.user.is_staff:
            return models.Active.objects.all()
        return models.Active.objects.filter(user__in = user.values_list("id"))   


    def get_serializer_class(self):
        if self.request.user.is_staff:
            if self.request.method == "PUT" or self.request.method == "PATCH":
                return serializers.UpdateActiveAdminSerializer
            return serializers.ActiveAdminSerializer
        return serializers.ActiveSerializer

    def  get_serializer_context(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return {'user_id': self.kwargs['pk']}
        return {"id" :self.request.user.id}

    def create(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            serializer = serializers.ActiveAdminSerializer(
                    data=request.data,
                    context={"id" :self.request.user.id})
            serializer.is_valid(raise_exception=True)
            active = serializer.save()
            serializer = serializers.ActiveAdminSerializer(active)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializer = serializers.ActiveSerializer(
                    data=request.data,
                    context={"id" :self.request.user.id})
        serializer.is_valid(raise_exception=True)
        active = serializer.save()
        serializer = serializers.ActiveSerializer(active)
        return Response(serializer.data, status=status.HTTP_201_CREATED)