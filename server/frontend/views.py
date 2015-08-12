from frontend.models import *
from frontend.serializers import *
from frontend.permissions import *
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from frontend import fabfile
import re
from fabric.api import *

env.use_ssh_config = True
env.user="webasr"
env.hosts=["squeal.dcs.shef.ac.uk"]

env.password="asr4daweb"

@api_view(('GET',))
def api_root(request, format = None):
    return Response({
        'users': reverse('users', request=request, format=format),
        'uploads': reverse('uploads', request=request, format=format),
        'systems': reverse('systems', request=request, format=format),
        'signup': reverse('signup', request=request, format=format),
        'newupload': reverse('newupload', request=request,format=format),
        })

class UploadList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('transcripts', 'audiofiles')
    def get_queryset(self):
        user = self.request.user
        return Upload.objects.filter(user=user)
    serializer_class = FinishedUploadSerializer

class UploadCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UploadSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        localpath = serializer.data.get('audiofiles')
        command = System.objects.all().get(name=(serializer.data.get('systems'))).command
        re1='.*?'   # Non-greedy match on filler
        re2='((?:[a-z][a-z\\.\\d_]+)\\.(?:[a-z\\d]{3}))(?![\\w\\.])'    # File Name 1
        rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
        m = rg.search(localpath)
        file1 = ''
        if m:
            file1=m.group(1)
        re1='((?:[a-z][a-z0-9_]*))' # Variable Name 1
        rg = re.compile(re1,re.IGNORECASE|re.DOTALL)
        m = rg.search(file1)
        if m:
            filename=m.group(1)
        fabfile.process_execute(localpath,filename,command)    
    


class UploadDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner,)
    queryset = Upload.objects.all()
    serializer_class = FinishedUploadSerializer

class SystemList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = System.objects.all()
    serializer_class = SystemSerializer

class SystemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = System.objects.all()
    serializer_class = SystemSerializer

class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,permissions.IsAdminUser)
    queryset = CustomUser.objects.all()
    serializer_class = AdminUserSerializer
   
class UserDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = CustomUser.objects.all()
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminUserSerializer
        else:
            return UserSerializer

class UserCreate(generics.CreateAPIView):
    serializer_class = NewUserSerializer
    def perform_create(self, serializer):
        serializer.save()










# @api_view(['GET', 'POST'])
# def upload_list(request,format = 'html',):
   
#     if request.method == 'GET':
#         uploads = Upload.objects.all()
#         serializer = UploadSerializer(uploads, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = UploadSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def upload_detail(request, pk, format = 'html'):
  
#     try:
#         upload = Upload.objects.get(pk=pk)
#     except Upload.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = UploadSerializer(upload)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = UploadSerializer(upload, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         upload.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




# @api_view(['GET', 'POST'])
# def system_list(request,format = 'html'):
   
#     if request.method == 'GET':
#         systems = System.objects.all()
#         serializer = SystemSerializer(systems, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = SystemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def system_detail(request, pk, format = 'html'):
  
#     try:
#         system = System.objects.get(pk=pk)
#     except System.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SystemSerializer(upload)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = SystemSerializer(system, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     system.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)