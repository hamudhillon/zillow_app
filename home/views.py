from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
import re
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from home.zillow_ui import zillow_get,check_status
from django.contrib import messages
import json
from rest_framework import status
import uuid
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.response import Response
from home.serializers import ZillowSerializer
from home.models import result
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Api Views------------------------------------------------------------
token_param = openapi.Parameter('Authorization token', in_=openapi.IN_HEADER,
                                description='user token',
                                type=openapi.TYPE_STRING)

connection_param = openapi.Parameter('Connection keep-alive', in_=openapi.IN_HEADER,
                                description='Connection',
                                type=openapi.TYPE_STRING)

class IndexView(APIView):
    # authentication_classes = [SessionAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # @swagger_auto_schema(manual_parameters=[token_param,connection_param])
    def get(self,request):
        try:
            response = {
                'message': 'Welcome to Scrapping Hero API'
            }
            return Response(response)
        except:
            import sys
            print(sys.exc_info())
            response = {
                'message': 'Error'
            }
            return Response(response)

# Parameters For Swagger
sortby_param = openapi.Parameter('sortby', in_=openapi.IN_QUERY,
                                description='sort order',
                                type=openapi.TYPE_STRING)
page_param = openapi.Parameter('page', in_=openapi.IN_QUERY,
                                description='page to navigate',
                                type=openapi.TYPE_STRING)
count_param = openapi.Parameter('count', in_=openapi.IN_QUERY,
                                description='limit for records',
                                type=openapi.TYPE_STRING)

sortorder_param = openapi.Parameter('sortorder', in_=openapi.IN_QUERY,
                                description='sorting order asc,desc',
                                type=openapi.TYPE_STRING)

status_param = openapi.Parameter('status', in_=openapi.IN_QUERY,
                                description='status filter active,inactive',
                                type=openapi.TYPE_STRING)

createdgte_param = openapi.Parameter('created[gte]', in_=openapi.IN_QUERY,
                                description='created date greater than',
                                type=openapi.TYPE_STRING)


createdlte_param = openapi.Parameter('created[lte]', in_=openapi.IN_QUERY,
                                description='created date less than',
                                type=openapi.TYPE_STRING)

updatedgte_param = openapi.Parameter('updated[gte]', in_=openapi.IN_QUERY,
                                description='updated date greater than',
                                type=openapi.TYPE_STRING)

updatedlte_param = openapi.Parameter('updated[lte]', in_=openapi.IN_QUERY,
                                description='updated date less than',
                                type=openapi.TYPE_STRING)

city_param = openapi.Parameter('city', in_=openapi.IN_QUERY,
                                description='city to filter',
                                type=openapi.TYPE_STRING)

state_param = openapi.Parameter('state', in_=openapi.IN_QUERY,
                                description='state to filter',
                                type=openapi.TYPE_STRING)

list_param = openapi.Parameter('list', in_=openapi.IN_QUERY,
                                description='filter by scrapper list',
                                type=openapi.TYPE_STRING)

id_param = openapi.Parameter('id', in_=openapi.IN_QUERY,
                                description='filter by id',
                                type=openapi.TYPE_STRING)

token_param = openapi.Parameter('token', in_=openapi.IN_HEADER,
                                description='user token',
                                type=openapi.TYPE_STRING)


# ------------------------------------------------------------------------------------------

class ZillowApiView(APIView):
    # authentication_classes = [SessionAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # def get_serializer(self):
    #     return ZillowSerializer()
    @swagger_auto_schema(manual_parameters=[id_param,sortby_param,page_param,
                                            count_param,
                                            sortorder_param,status_param,createdgte_param,
                                            createdlte_param,updatedgte_param,updatedlte_param,
                                            city_param,state_param,list_param])
    
    # ---------------------------------------------------------------------------------
    def get(self, request):
        """
        sortby -- sortby field eg:id
        page -- page param
        count -- records limit
        sortorder -- asc,desc
        created[gte] -- to filter by updated date[gte]
        created[lte] -- to filter by created date[lte]
        updated[gte] -- to filter by updated date[gte]
        updated[lte] -- to filter by updated date[lte]
        status -- to filter by status
        city -- to filter by city
        state -- to filter by state
        list -- to filter by scrapper list
        
        """
        try:
            sortby = request.GET.get('sortby', 'id')
            page = request.GET.get('page', 1)
            count = request.GET.get('count', 10)
            sort_order = request.GET.get('sortorder', 'asc')
            created_gte = request.GET.get('created[gte]',None)
            created_lte = request.GET.get('created[lte]', None)
            updated_gte = request.GET.get('updated[gte]', None)
            updated_lte = request.GET.get('updated[lte]', None)
            zstatus = request.GET.get('status', 'active')
            city_filter = request.GET.get('city', None)
            state_filter = request.GET.get('state', None)
            list_filter = request.GET.get('list', None)
            id_filter = request.GET.get('id', None)
            
            if zstatus not in ['active', 'inactive', 'closed']:
                zstatus = 'active'
                
            page = int(page)
            count = int(count)
            if count>10:
                count = 10

            if page == 0 or page == 1:
                offset = 0
            else:
                offset = (page-1)*(count)
            upto = offset + count

            if sort_order == 'desc':
                sortby = '-' + str(sortby)

            JS = None
            total = result.objects.filter(status=zstatus,source='zillow').count()
            # City,State and list filters-------------------------------------------------------
            
            
            if id_filter is not None:
                lsthotels = result.objects.filter(id = id_filter,source='zillow')
                JS = ZillowSerializer(lsthotels, many=True)
            
            if city_filter is not None and state_filter is None and list_filter is None:
                lsthotels = result.objects.filter(city = city_filter, status=zstatus,source='zillow').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)
                
            if city_filter is None and state_filter is not None and list_filter is None:
                lsthotels = result.objects.filter(state = state_filter, status=zstatus,source='zillow').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)
                
            if city_filter is None and state_filter is None and list_filter is not None:
                lsthotels = result.objects.filter(scraper_name = list_filter, status=zstatus,source='zillow').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)
                
            # -------------------------------------------------------------------------------------------------------------------
            
            
            if created_gte is not None and created_lte is not None:
                created_gte = created_gte+('T00:00:00Z')
                created_lte = created_lte+('T23:59:59Z')
                lsthotels = result.objects.filter(created__range=(created_gte, created_lte), status=zstatus,source='zillow').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)

            if created_gte is not None:
                created_gte = created_gte + ('T00:00:00Z')
                lsthotels = result.objects.filter(created__gte=created_gte, status=zstatus,source='zillow').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)

            if created_lte is not None:
                created_lte = created_lte+('T23:59:59Z')
                lsthotels = result.objects.filter(created__lte=created_lte, status=zstatus,source='zillow').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)

            if updated_gte is not None and updated_lte is not None:
                updated_gte = updated_gte+('T00:00:00Z')
                updated_lte = updated_lte+('T23:59:59Z')
                lsthotels = result.objects.filter(updated__range=(updated_gte, updated_lte), status=zstatus,source='zillow').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)


            if updated_gte is not None:
                updated_gte = updated_gte + ('T00:00:00Z')
                lsthotels = result.objects.filter(updated__gte=updated_gte, status=zstatus,source='zillow').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)

            if updated_lte is not None:
                updated_lte = updated_lte+('T23:59:59Z')
                lsthotels = result.objects.filter(updated__lte = updated_lte, status=zstatus,source='zillow').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)

            if JS == None:
                lsthotels = result.objects.filter(status=zstatus,source='zillow').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many =True)

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'zillow data',
                'total':total,
                'zillow': JS.data
            }
            return Response(response)

        except:
            import sys
            print(sys.exc_info())
            response = {
                'status': 'error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Internal Server Error',
                'zillow': []
            }
            return Response(response)


# ------------------------------------------------------------------------------------------

class CraigsApiView(APIView):
    # authentication_classes = [SessionAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # def get_serializer(self):
    #     return ZillowSerializer()
    @swagger_auto_schema(manual_parameters=[id_param,sortby_param,page_param,
                                            count_param,
                                            sortorder_param,status_param,createdgte_param,
                                            createdlte_param,updatedgte_param,updatedlte_param,
                                            city_param,state_param,list_param])
    
    # ---------------------------------------------------------------------------------
    def get(self, request):
        """
        sortby -- sortby field eg:id
        page -- page param
        count -- records limit
        sortorder -- asc,desc
        created[gte] -- to filter by updated date[gte]
        created[lte] -- to filter by created date[lte]
        updated[gte] -- to filter by updated date[gte]
        updated[lte] -- to filter by updated date[lte]
        status -- to filter by status
        city -- to filter by city
        state -- to filter by state
        list -- to filter by scrapper list
        
        """
        try:
            sortby = request.GET.get('sortby', 'id')
            page = request.GET.get('page', 1)
            count = request.GET.get('count', 10)
            sort_order = request.GET.get('sortorder', 'asc')
            created_gte = request.GET.get('created[gte]',None)
            created_lte = request.GET.get('created[lte]', None)
            updated_gte = request.GET.get('updated[gte]', None)
            updated_lte = request.GET.get('updated[lte]', None)
            zstatus = request.GET.get('status', 'active')
            city_filter = request.GET.get('city', None)
            state_filter = request.GET.get('state', None)
            list_filter = request.GET.get('list', None)
            id_filter = request.GET.get('id', None)
            
            if zstatus not in ['active', 'inactive', 'closed']:
                zstatus = 'active'
                
            page = int(page)
            count = int(count)
            if count>10:
                count = 10

            if page == 0 or page == 1:
                offset = 0
            else:
                offset = (page-1)*(count)
            upto = offset + count

            if sort_order == 'desc':
                sortby = '-' + str(sortby)

            JS = None
            total = result.objects.filter(status=zstatus,source='craigslist').count()
            # City,State and list filters-------------------------------------------------------
            
            
            if id_filter is not None:
                lsthotels = result.objects.filter(id = id_filter,source='craigslist')
                JS = ZillowSerializer(lsthotels, many=True)
            
            if city_filter is not None and state_filter is None and list_filter is None:
                lsthotels = result.objects.filter(city = city_filter, status=zstatus,source='craigslist').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)
                
            if city_filter is None and state_filter is not None and list_filter is None:
                lsthotels = result.objects.filter(state = state_filter, status=zstatus,source='craigslist').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)
                
            if city_filter is None and state_filter is None and list_filter is not None:
                lsthotels = result.objects.filter(scraper_name = list_filter, status=zstatus,source='craigslist').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)
                
            # -------------------------------------------------------------------------------------------------------------------
            
            
            if created_gte is not None and created_lte is not None:
                created_gte = created_gte+('T00:00:00Z')
                created_lte = created_lte+('T23:59:59Z')
                lsthotels = result.objects.filter(created__range=(created_gte, created_lte), status=zstatus,source='craigslist').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)

            if created_gte is not None:
                created_gte = created_gte + ('T00:00:00Z')
                lsthotels = result.objects.filter(created__gte=created_gte, status=zstatus,source='craigslist').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)

            if created_lte is not None:
                created_lte = created_lte+('T23:59:59Z')
                lsthotels = result.objects.filter(created__lte=created_lte, status=zstatus,source='craigslist').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)

            if updated_gte is not None and updated_lte is not None:
                updated_gte = updated_gte+('T00:00:00Z')
                updated_lte = updated_lte+('T23:59:59Z')
                lsthotels = result.objects.filter(updated__range=(updated_gte, updated_lte), status=zstatus,source='craigslist').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)


            if updated_gte is not None:
                updated_gte = updated_gte + ('T00:00:00Z')
                lsthotels = result.objects.filter(updated__gte=updated_gte, status=zstatus,source='craigslist').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)

            if updated_lte is not None:
                updated_lte = updated_lte+('T23:59:59Z')
                lsthotels = result.objects.filter(updated__lte = updated_lte, status=zstatus,source='craigslist').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many=True)

            if JS == None:
                lsthotels = result.objects.filter(status=zstatus,source='craigslist').order_by(sortby)[offset:upto]
                JS = ZillowSerializer(lsthotels, many =True)

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'craigslist data',
                'total':total,
                'craigslist': JS.data
            }
            return Response(response)

        except:
            import sys
            print(sys.exc_info())
            response = {
                'status': 'error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Internal Server Error',
                'craigslist': []
            }
            return Response(response)





# ===================================================











def home(request):
    return render(request, 'homepage.html')


@login_required(login_url='/login/')
def roompage(request):
    return render(request, 'room.html')


def craeteusername(email):
    username = email.split("@")[0]
    username = re.sub('[^A-Za-z0-9\.]+', '', username)
    username = username.lower()
    orignam_uname = username
    exists = True
    count = 1
    while exists:
        exists = User.objects.filter(username=username).exists()
        if exists:
            if count < 10:
                username = orignam_uname + "0" + str(count)

            else:
                username = orignam_uname + str(count)
            count += 1
    return username.lower()


def Token_register(request):
    try:
        lastname = ''
        token_key = None
        msg = None
        if request.method == "POST":
            exists_check = request.POST.get('txt_email')

            user_msg = User.objects.filter(email=exists_check).count()
            if user_msg > 0:
                msg = 'Email Already Exists'
            else:
                usr_password = request.POST.get('txt_password')
                objU = User()
                objU.first_name = request.POST.get('txt_fname')
                objU.last_name = lastname
                username = craeteusername(request.POST.get(
                    'txt_email'))  # create username from email
                objU.username = username
                objU.email = request.POST.get('txt_email')
                objU.password = usr_password
                objU.set_password(objU.password)
                objU.is_active = True
                objU.is_superuser = False
                objU.is_staff = False
                objU.save()
                token = Token.objects.create(user=objU)
                token_key = token.key
        return render(request, 'Token_register.html', {"token": token_key, "msg": msg})

    except:
        import sys
        return HttpResponse(str(sys.exc_info()))


def login1(request):
    msg = None
    if request.method == "POST":
        username = request.POST.get('txt_username')
        password = request.POST.get('txt_password')
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):

                objuser = user
            else:
                objuser = None

        except:
            objuser = None

        if objuser is not None:
            if objuser.is_active:
                login(request, objuser)
                token = Token.objects.get_or_create(user=objuser)
                token = token[0]
                token_key = token.key
                msg = token_key
            return render(request, 'room.html', {"msg1": msg})
            # return HttpResponseRedirect('/room/')
        else:
            msg = 'Wrong Password'
    return render(request, 'login.html', {"msg1": msg})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def runnscrapper(request):
    print("hello")
    check_status()
    return render(request, 'homepage.html')

@login_required(login_url='/login/')
def ProcessCsvFiles(request):
    
    print('Hreee')
    data = {}
    print(request.method)
    if "GET" == request.method:
        return render(request, "upload_csv.html", data)
    # if not GET, then proceed with processing
    try:

        csv_file = request.FILES["csv_file"]
        print(csv_file)
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponse('Csv Error')
    #if file is too large, return message
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponse('Csv Error')
        
        
        try:
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split(" ")
            for line in lines:
                print(line)
                import sys
                data=json.dumps(str(zillow_get(line)))
                print(sys.exc_info())
                print(type(data))
                print(data)
            return HttpResponse(data)
            
        except:
            return HttpResponse('Error')

    except:
        return HttpResponse('Error')


