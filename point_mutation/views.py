"""Standard API methods for displaying MiSeq data"""
import re
import zipfile
import tarfile
from django.http import request

from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader

from rest_framework import status
from rest_framework.decorators import api_view

from point_mutation.parsers.crispresso_parser import CrispressoParser
from point_mutation.discover import DiscoverFolders

@api_view(['GET']) ### TODO: HOME to allow for input file path, POST to redirect to dynamic URL with folder name i.e. Miseq_093
def home(request):
    if request.method == 'GET':
        context = discover_folders('/var/data/uploadedFiles/')

        return render(request, 'index.html', context)

### 
# Home to have extensible folder selection based on discovery of what miseq folders have been added. Docker to have persistant volume using docker compose. 
# selecting a folder from home loads miseq view
# upload folders to volume by script (perhaps a UI later, be aware this will take time.)
# title of page to be "Point Mutation - [Folder Name]"
### 


def discover_folders(base_folder_path):

        discover_folders = DiscoverFolders()

        return discover_folders.get_dirs(base_folder_path)

def point_mutation_view(request, file_path):
    context = point_mutation_summary(file_path)

    request.session['data'] = context

    return render(request, 'point_mutation.dj.html', context)
    
@api_view(['GET'])
def point_mutation_allele(request, miseq, oligo_index, exp):

    data = request.session['data']

    max_wells = 384 if data['large_plate'] else 96

    well_num = oligo_index.zfill(2)
    experiments = data['summary'][well_num]['experiments']
    gene = data['summary'][well_num]['gene']
    details = data['summary'][well_num]['details']
    indel_stats = data['summary'][well_num]
    ##designs = data['designs']['summary']['1'][]

    context = data
    context['miseq'] = miseq
    context['oligoIndex'] = oligo_index
    context['selection'] = exp
    context['maxWells'] = max_wells
    context['experiments'] = experiments
    context['gene'] = gene
    context['details'] = details
    context['indelStats'] = indel_stats

    return render(request, 'point_mutation_allele.dj.html', context)

@api_view(['POST'])
def point_mutation_upload(request):
    if request.method == 'POST':

        print("request recieved")

        file_path = request.POST['folderPath'] + request.POST['item'] + '/'

        print(file_path)

        return point_mutation_view(request, file_path)

@api_view(['GET'])
def point_mutation_upload_folder(request):
    return render(request, 'point_mutation_upload_folder.dj.html')

def point_mutation_summary(file_path):
    
    if not file_path:
        file_path = '/home/ubuntu/dev/miseq-standalone/testFiles/Miseq_093/'

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

    return data
