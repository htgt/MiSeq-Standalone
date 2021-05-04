"""Standard API methods for displaying MiSeq data"""
import zipfile
import tarfile

from django.http.response import JsonResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view

from crispresso_upload.parsers.crispresso_parser import CrispressoParser

### TODO: Rename crispresso app name to something more appropriate

@api_view(['GET'])
def home(request):
    if request.method == 'GET':
        context = crispresso_summary('/home/ubuntu/dev/miseq-standalone/testFiles/Plate_test/')

        return render(request, 'point_mutation.dj.html', context)

@api_view(['POST'])
def crispresso_upload(request):
    if request.method == 'POST':

        print("request recieved")

        return JsonResponse(crispresso_summary(request.POST["filePath"]), safe=False)
        # will not run code under this
        #crispresso_files = {}
        #print(crispresso_files)
        #if next(iter(crispresso_files.values())).size > 0:
        #    return JsonResponse({'status': 'this worked'}, status=status.HTTP_201_CREATED)
        #return JsonResponse("", status=status.HTTP_400_BAD_REQUEST)

def crispresso_summary(file_path):
    
    if not file_path:
        file_path = '/home/ubuntu/dev/miseq-standalone/testFiles'

    parser = CrispressoParser()

    #if zipfile.is_zipfile(uploaded_file_path):
    #    with zipfile.ZipFile.open(uploaded_file_path, 'r|*') as zip_file:
    #        extracted_file_names = zip_file.namelist()
    #elif tarfile.is_tarfile(uploaded_file_path):
    #    with tarfile.open(uploaded_file_path, 'r|*') as tar_file:
    #        parser.global_threshold = 1000
    #        parser.threshold_percent = 5
    #        parser.load_directory(tar_file, uploaded_file_path)
    
    data = {
        'summary': {
            '01': {
                'percentages': 'quant_data'
            }
        }
    }

    parser.global_threshold = 1000
    parser.threshold_percent = 5
    data.update(parser.load_directory(file_path))

    print('data in views: ', data)

    return data
