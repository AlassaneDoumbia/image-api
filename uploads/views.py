# importing os module  
import os 
import uuid

from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.generics import GenericAPIView
from uploads.serializers import FileSerializer

# Create your views here.
def rename_file(filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    # return '/'.join(['images', str('avatar').lower(), filename])
    return filename

def saveFile(file, path, attemps):

    if attemps >= 3:
        return None
    try:
        print("Saving File "+file.name)
        print(type(file))
        new_name = rename_file(file.name)
        path = default_storage.save(path+"/"+new_name, ContentFile(file.read()))
        tmp_file = os.path.join("media", path)
        print(tmp_file)
        return tmp_file
    except:
        print("Something went wrong when saving the file")
        attemps = attemps + 1
        saveFile(file,path,attemps)
    return

def createDirectory(app, dir):
    try: 
        # paths = os.path.join("", app) 
        directory = app+"-"+dir
        paths = os.path.join("", directory) 
        # path exists or not
        isExist = os.path.exists(paths)
        print(isExist)
        if isExist:
            print("Directory already created '% s' : " % directory)
            return True
        os.mkdir(paths) 
        print("Directory '% s' created" % directory)
        return True
    except OSError as error: 
        print(error) 
        return False


@api_view(['GET'])
def ping(request):
    """
    List all code snippets, or create a new snippet.
    """
    return Response("Connexion Okay", status=status.HTTP_201_CREATED)

@api_view(['POST'])
def upload(request):
    """
    List all code snippets, or create a new snippet.
    """
    currentSite     = get_current_site(request).domain
    body = request.data
    app = body["app"]
    dir = body["dir"]
    file = body["file"]
    print(body)
    print(app)
    print(dir)
    print(file.name)
    tmp_file = saveFile(file,app+"-"+dir,0)
    
    if tmp_file is None:
        return Response("Erreur lors de l'enregistrement du fichier", status=status.HTTP_400_BAD_REQUEST)
    # createDir = createDirectory("geotrac","images")

    return Response(currentSite+"/"+tmp_file, status=status.HTTP_200_OK)

class RegisterView(GenericAPIView):
    serializer_class = FileSerializer

    # Method with post
    def post(self, request):
        body = request.data
        currentSite     = get_current_site(request).domain
        # relativeLink    = reverse('email-verify')
        # serializer = self.serializer_class(data=body)
        print(body)
        print(currentSite)