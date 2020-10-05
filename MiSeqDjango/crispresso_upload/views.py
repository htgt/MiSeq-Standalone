import csv, io, zipfile, tarfile, re
from django.shortcuts import render

from decimal import Decimal

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from crispresso_upload.models import CrispressoData
from crispresso_upload.serializers import CrispressoSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def crispresso_upload(request):
    if request.method == 'GET':
        crispresso = CrispressoData.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            crispresso = crispresso.filter(title__icontains=title)
        
        crispresso_serializer = CrispressoSerializer(crispresso, many=True)
        return JsonResponse(crispresso_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':

        count = CrispressoData.objects.all().delete()
        return crispresso_summary(request)
        # will not run code under this
        print(crispresso_files)
        if next(iter(crispresso_files.values())).size > 0:
            return JsonResponse({'status': 'this worked'}, status=status.HTTP_201_CREATED) 
        return JsonResponse(crispresso_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = CrispressoData.objects.all().delete()
        return JsonResponse({'message': '{} Crispressos were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def crispresso_detail(request, pk):
    # find CrispressoData by pk (id)
    try: 
        crispresso = CrispressoData.objects.get(pk=pk) 
        if request.method == 'GET': 
            crispresso_serializer = CrispressoSerializer(crispresso) 
            return JsonResponse(crispresso_serializer.data)
        elif request.method == 'PUT': 
            crispresso_data = JSONParser().parse(request) 
            crispresso_serializer = CrispressoSerializer(crispresso, data=crispresso_data) 
            if crispresso_serializer.is_valid(): 
                crispresso_serializer.save() 
                return JsonResponse(crispresso_serializer.data) 
            return JsonResponse(crispresso_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE': 
            crispresso.delete() 
            return JsonResponse({'message': 'Crispresso was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


    except CrispressoData.DoesNotExist: 
        return JsonResponse({'message': 'The CrispressoData does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # GET / PUT / DELETE CrispressoData
    
        
@api_view(['GET'])
def crispresso_list_published(request):
    crispresso = CrispressoData.objects.filter(published=True)
        
    if request.method == 'GET': 
        crispresso_serializer = CrispressoSerializer(crispresso, many=True)
        return JsonResponse(crispresso_serializer.data, safe=False)

def crispresso_summary(request):
    
    print("request recieved")

    uploaded_file = request.FILES["uploadedFile"]

    print("file being checked")

    if not uploaded_file:
        print("file not valid")
        return JsonResponse(error="Zip of directory could not be found. Please ensure you have uploaded the correct file type.", status=status.HTTP_400_NOT_FOUND)
    
    print("file valid, about to unzip")

    extracted_file_names = ''
    print("Unzipping...")

    uploaded_file_path = uploaded_file.temporary_file_path()

    if zipfile.is_zipfile(uploaded_file):
        with zipfile.open(uploaded_file, 'r|*') as zip:
            extracted_file_names = zip.namelist()
    elif tarfile.is_tarfile(uploaded_file_path):
        with tarfile.open(uploaded_file_path, 'r|*') as tar:
            well_summary = extract_well_information(tar)

    print("unzipped")
    #alleles_data_set = alleles_file.read().decode('UTF-8')
    #alleles_io_string = io.StringIO(alleles_data_set)

    #quant_data_set = quant_file.read().decode('UTF-8')
    #quant_io_string = io.StringIO(quant_data_set)

    #quant_data = get_quant_data(quant_io_string)

    #next(alleles_io_string)

    #reader = csv.reader(alleles_io_string, delimiter='\t')

    data = {
        "extracted file names" : extracted_file_names,
        "summary": {
            "01": {
                "percentages": "quant_data"
            }
        }
    }

    exp = 'EXP2'

    
            
#TODO: Look into serialisers
    
    
    return JsonResponse(data, safe=False)

def extract_well_information(tar_file):
    summary = object
    well = '01'
    alleles_freq_pattern = 'Alleles_frequency_table\.txt$'
    log_pattern = 'CRISPResso_RUNNING_LOG\.txt$'
    quant_pattern = 'Quantification_of_editing_frequency\.txt$'
    well_num_pattern = '/(\d{2})/$'

    print(tar_file.getmembers())

    for tar_info in tar_file.members:
        print("Checking tar info for " + tar_info.name)
        if tar_info.isdir():
            well_match = re.search(well_num_pattern, tar_info.name)
            if well_match:
                well = well_match.group(0)
        elif tar_info.isfile():
            alleles_match = re.search(alleles_freq_pattern, tar_info.name)
            log_match = re.search(log_pattern, tar_info.name)
            quant_match = re.search(quant_pattern, tar_info.name)

            if quant_match:
                data["percentages"] = get_quant_data(tar_file.extractfile(tar_info))
                summary[well] = data
                print(summary)

            if alleles_match or log_match:
                temp_file = tar_file.extractfile(tar_info)
                print("Printing filename")
                print(temp_file.name)


    return summary

def get_well_summary(well_folder, threshold, threshold_percent):
    data

    alleles_file = well_folder["Alleles_frequency_table.txt"]

    if not alleles_file:
        raise IOError(error="Allele frequency table can not be found. Please upload the correct files.")

    try:
        lines = read_alleles_frequency_file(alleles_file, threshold, threshold_percent)
        data = lines.join('\n')
    except:
        raise Exception("Unexpected error occured while reading the Allele frequency table. Please check the data is in the correct format.")





def get_quant_data(io_string):
    lines = io_string.read().split('\n')

    processed_lines = list()

    for line in lines:
        processed_line = line.strip()
        processed_line = processed_line.replace(" ", ":")
        processed_lines.append(processed_line)

    try:
        data = {
            "unmod": processed_lines[1].split(':')[2],
            "nhej": processed_lines[2].split(':')[2],
            "hdr": processed_lines[3].split(':')[2],
            "mix": processed_lines[4].split(':')[3],
            "total": processed_lines[6].split(':')[2]
        }
        return data
    except ValueError:
        raise ValueError("Something went wrong when saving quant data to an object")
        return {}

def read_alleles_frequency_file(io_string, threshold, threshold_percent):
    lines = io_string.read().split('\n')
    threshold = threshold or 0

    processed_lines = list()

    if threshold_percent:
        processed_lines = get_lines_above_threshold(lines)
    elif threshold != 0:
        line_limit = min(threshold, len(lines))
        processed_lines = lines[0:line_limit]

    return processed_lines
    
