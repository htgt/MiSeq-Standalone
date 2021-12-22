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
from point_mutation.parsers.indel_parser import IndelParser
from point_mutation.parsers.frequency_parser import FrequencyParser
from point_mutation.discover import DiscoverFolders
from point_mutation.file_uploader import FileUploader


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

    print('getting indel_parsr')
    indel_parser = IndelParser()

    data = request.session['data']

    max_wells = 384 if data['large_plate'] else 96

    well_num = oligo_index.zfill(2)
    experiments = data['summary'][well_num]['experiments']
    gene = data['summary'][well_num]['gene']
    details = data['summary'][well_num]['details']
    print('getting indel_stats')
    indel_stats = indel_parser.load_directory(data['file_path'], well_num, exp)
    ##designs = data['designs']['summary']['1'][]
    print('got_indel_stats: ')
    print(indel_stats)

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

        file_path = request.POST['folderPath'] + request.POST['item'] + '/'

        return point_mutation_view(request, file_path)

@api_view(['GET'])
def point_mutation_upload_folder(request):
    return render(request, 'point_mutation_upload_folder.dj.html')

@api_view(['GET'])
def allele_summary(request, miseq, oligo_index, exp, limit):

    freq_parser = FrequencyParser()

    data = request.session['data']
    well_num = oligo_index.zfill(2)

    crispr = data['summary'][well_num]['crispr']
    allele_freq_data = freq_parser.get_allele_freq_data(data['file_path'], well_num, exp, limit)

    context = {
        'crispr': crispr,
        'data' : allele_freq_data
    }

    return

def allele_summary_ajax(request):
    if request.is_ajax and request.method == 'GET':
        oligo_index = request.GET.get('oligo_index', None)
        exp = request.GET.get('exp', None)
        limit = request.GET.get('limit', None)

        freq_parser = FrequencyParser()

        data = request.session['data']
        well_num = oligo_index.zfill(2)

        crispr = data['summary'][well_num]['crispr'][exp]
        allele_freq_data = freq_parser.get_allele_freq_data(data['file_path'], well_num, exp, limit)
        
        context = {
            'crispr': crispr,
            'data' : allele_freq_data
        }

        return JsonResponse(context, status = 200)

def point_mutation_summary(file_path):
    
    if not file_path:
        file_path = '/home/ubuntu/dev/miseq-standalone/testFiles/Miseq_093/'

    parser = CrispressoParser()
    
    data = {
        'file_path': file_path,
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

def folder_upload_ajax(request):
    try:
     if request.is_ajax and request.method == 'POST':
        path = request.POST["filePath"]
        file = request.FILES.get("file")

        file_uploader = FileUploader()

        file_uploader.handle_files(path, file)

        return JsonResponse({}, status = 200)
    except:
        return JsonResponse({}, status = 400)
