from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import DefaultPagination
from . import models, serializers, filters


class BrowserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    serializer_class = serializers.BrowserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.BrowserFilter
    ordering_fields = ['date']

    def get_queryset(self):
        receiver = models.Receiver.objects.prefetch_related('user').filter(user_id=self.request.user.id).all()
        if receiver.values().count() > 0 and not self.request.user.is_staff:
            return models.Browser.objects.prefetch_related('receiver').filter(receiver=receiver.values()[0]['id']).all()
        return models.Browser.objects.prefetch_related('receiver').all()


    def create(self, request, *args, **kwargs):
        receiver = models.Receiver.objects.prefetch_related('user').filter(user_id=self.request.user.id)
        browser = models.Browser.objects.filter(date=request.data['date'])
        if browser.values().count() > 0 and browser.filter(receiver=receiver.values()[0]['id']).values().count() > 0:
            return Response({'error': 'Data already exists.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if receiver.values().count() > 0:
            serializer = serializers.CreateBrowserSerializer(
                data=request.data,
                context={'id': receiver.values()[0]['id']})
        else:
            serializer = serializers.CreateBrowserSerializer(
                data=request.data,
                context={'id':'1'}
            )
        serializer.is_valid(raise_exception=True)
        browser = serializer.save()
        serializer = serializers.BrowserSerializer(browser)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateBrowserSerializer
        return serializers.BrowserSerializer

    


class AlarmListViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    serializer_class = serializers.AlarmListSerializer
    # pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.AlarmListFilter

    def get_queryset(self):
        receiver = models.Receiver.objects.prefetch_related("user").filter(user=self.request.user.id).only('id')
        browser = models.Browser.objects.prefetch_related("receiver").filter(receiver=receiver.values()[0]['id']).only('id')
        if self.request.user.is_staff:
            return models.AlarmList.objects.prefetch_related('browse').all()
        return models.AlarmList.objects.prefetch_related('browse').filter(browse__in = browser.values_list("id"))

        
    def create(self, request, *args, **kwargs):
        if isinstance(request.data['alarm_list'], list):
            serializer = serializers.AlarmListCreateSerializer(data=request.data)
        else:
            serializer = serializers.AlarmListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class ArrayDataViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = models.ArrayData.objects.prefetch_related('browse').all()
    serializer_class = serializers.ArrayDataViewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ArrayDataFilter


def download_file(request,folder, file_name):
    uploaded_file = models.ArrayData.objects.get(array_data= folder + '/' + file_name)
    response = HttpResponse(uploaded_file.array_data, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.array_data.name}"'
    return response

    # def get_queryset(self):
    #     receiver = models.Receiver.objects.prefetch_related("user").filter(user=self.request.user.id).only('id')
    #     browser = models.Browser.objects.prefetch_related("receiver").filter(receiver=receiver.values()[0]['id']).only('id')
    #     if self.request.user.is_staff:
    #         return models.ArrayData.objects.prefetch_related('browse').all()
    #     return models.ArrayData.objects.prefetch_related('browse').filter(browse__in = browser.values_list("id"))

    
    # def create(self, request, *args, **kwargs):
    #     if isinstance(request.data['array_data'], list):
    #         serializer = serializers.ArrayDataSerializer(data=request.data)
    #     else:
    #         serializer = serializers.ArrayDataViewSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EventIndexPlotViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = models.EventIndexPlot.objects.prefetch_related('browse').all()
    serializer_class = serializers.EventIndexPlotSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.EventIndexPlotFilter

    def get_queryset(self):
        receiver = models.Receiver.objects.prefetch_related("user").filter(user=self.request.user.id).only('id')
        browser = models.Browser.objects.prefetch_related("receiver").filter(receiver=receiver.values()[0]['id']).only('id')
        if self.request.user.is_staff:
            return models.EventIndexPlot.objects.prefetch_related('browse').all()
        return models.EventIndexPlot.objects.prefetch_related('browse').filter(browse__in = browser.values_list("id"))
    
    def create(self, request, *args, **kwargs):
        if isinstance(request.data['event_index_plot'], list):
            serializer = serializers.EventIndexPlotCreateSerializer(data=request.data)
        else:
            serializer = serializers.EventIndexPlotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class EventLocationPrintViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = models.EventLocationPrint.objects.prefetch_related('browse').all()
    serializer_class = serializers.EventLocationPrintSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.EventLocationPrintFilter

    def get_queryset(self):
        receiver = models.Receiver.objects.prefetch_related("user").filter(user=self.request.user.id).only('id')
        browser = models.Browser.objects.prefetch_related("receiver").filter(receiver=receiver.values()[0]['id']).only('id')
        if self.request.user.is_staff:
            return models.EventLocationPrint.objects.prefetch_related('browse').all()
        return models.EventLocationPrint.objects.prefetch_related('browse').filter(browse__in = browser.values_list("id"))
    
    def create(self, request, *args, **kwargs):
        if isinstance(request.data['event_location_print'], list):
            serializer = serializers.EventLocationPrintCreateSerializer(data=request.data)
        else:
            serializer = serializers.EventLocationPrintSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class TableListViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = models.TableList.objects.prefetch_related('browse').all()
    serializer_class = serializers.TableListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.TableListFilter

    def get_queryset(self):
        receiver = models.Receiver.objects.prefetch_related("user").filter(user=self.request.user.id).only('id')
        browser = models.Browser.objects.prefetch_related("receiver").filter(receiver=receiver.values()[0]['id']).only('id')
        if self.request.user.is_staff:
            return models.TableList.objects.prefetch_related('browse').all()
        return models.TableList.objects.prefetch_related('browse').filter(browse__in = browser.values_list("id"))


    def create(self, request, *args, **kwargs):
        # if isinstance(request.data[''], list):
        serializer = serializers.TableListCreateSerializer(data=request.data)
        # else:
            # serializer = serializers.TableListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class XDataViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = models.XData.objects.prefetch_related('browse').all()
    serializer_class = serializers.XDataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.XDataFilter

    def get_queryset(self):
        receiver = models.Receiver.objects.prefetch_related("user").filter(user=self.request.user.id).only('id')
        browser = models.Browser.objects.prefetch_related("receiver").filter(receiver=receiver.values()[0]['id']).only('id')
        if self.request.user.is_staff:
            return models.XData.objects.prefetch_related('browse').all()
        return models.XData.objects.prefetch_related('browse').filter(browse__in = browser.values_list("id"))



class AlarmTableViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    serializer_class = serializers.AlarmTableSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.AlarmTableFilter

    def get_queryset(self):
        receiver = models.Receiver.objects.prefetch_related("user").filter(user=self.request.user.id).only('id')
        browser = models.Browser.objects.prefetch_related("receiver").filter(receiver=receiver.values()[0]['id']).only('id')
        if self.request.user.is_staff:
            return models.AlarmTable.objects.prefetch_related('browse').all()
        return models.AlarmTable.objects.prefetch_related('browse').filter(browse__in = browser.values_list("id"))

    
    def create(self, request, *args, **kwargs):
        serializer = serializers.AlarmTableCreateSerializer(
                data=request.data,
                context={"date" :models.Browser.objects.filter(id=self.request.data["browse"]).values()[0]['date']})
        serializer.is_valid(raise_exception=True)
        browser = serializer.save()
        # serializer = serializers.AlarmTableSerializer(browser)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class SystemAlarmViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    serializer_class = serializers.SystemAlarmSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.SystemAlarmFilter

    def get_queryset(self):
        receiver = models.Receiver.objects.prefetch_related("user").filter(user=self.request.user.id).only('id')
        browser = models.Browser.objects.prefetch_related("receiver").filter(receiver=receiver.values()[0]['id']).only('id')
        if self.request.user.is_staff:
            return models.SystemAlarm.objects.prefetch_related('browse').all()
        return models.SystemAlarm.objects.prefetch_related('browse').filter(browse__in = browser.values_list("id"))

    
    def create(self, request, *args, **kwargs):
        serializer = serializers.SystemAlarmSerializer(
                data=request.data,
                context={"date" :models.Browser.objects.filter(id=self.request.data["browse"]).values()[0]['date']})
        serializer.is_valid(raise_exception=True)
        system_alarm = serializer.save()
        serializer = serializers.SystemAlarmSerializer(system_alarm)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EndFiberViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    serializer_class = serializers.EndFiberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.EndFiberFilter

    def get_queryset(self):
        receiver = models.Receiver.objects.prefetch_related("user").filter(user=self.request.user.id).only('id')
        # browser = models.Browser.objects.prefetch_related("receiver").filter(receiver=receiver.values()[0]['id']).only('id')
        if self.request.user.is_staff:
            return models.EndFiber.objects.prefetch_related('receiver').all()
        return models.EndFiber.objects.prefetch_related('receiver').filter(receiver__in = receiver.values_list("id"))

    
    def create(self, request, *args, **kwargs):
        serializer = serializers.EndFiberSerializer(
                data=request.data,
                context={"id" :models.Receiver.objects.filter(user=self.request.user.id).values()[0]['id']})
        serializer.is_valid(raise_exception=True)
        end_fiber = serializer.save()
        serializer = serializers.EndFiberSerializer(end_fiber)
        return Response(serializer.data, status=status.HTTP_201_CREATED)