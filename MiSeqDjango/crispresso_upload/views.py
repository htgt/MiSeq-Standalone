"""Standard API methods for displaying MiSeq data"""
import zipfile
import tarfile

from django.http.response import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view

from crispresso_upload.parsers.crispresso_parser import CrispressoParser

### TODO: Rename crispresso app name to something more appropriate.

@api_view(['POST'])
def crispresso_upload(request):
    if request.method == 'POST':
        return crispresso_summary(request)
        # will not run code under this
        #crispresso_files = {}
        #print(crispresso_files)
        #if next(iter(crispresso_files.values())).size > 0:
        #    return JsonResponse({'status': 'this worked'}, status=status.HTTP_201_CREATED)
        #return JsonResponse("", status=status.HTTP_400_BAD_REQUEST)

def crispresso_summary(request):
    
    print("request recieved")

    uploaded_file = request.FILES["uploadedFile"]

    print("file being checked")

    if not uploaded_file:
        print("file not valid")
        return JsonResponse(data="", error="Zip of directory could not be found. Please ensure you have uploaded the correct file type.", status=status.HTTP_404_NOT_FOUND)
    
    print("file valid, about to unzip")

    extracted_file_names = ''
    print("Unzipping...")

    uploaded_file_path = uploaded_file.temporary_file_path()

    parser = CrispressoParser()

    if zipfile.is_zipfile(uploaded_file):
        with zipfile.ZipFile.open(uploaded_file, 'r|*') as zip_file:
            extracted_file_names = zip_file.namelist()
    elif tarfile.is_tarfile(uploaded_file_path):
        with tarfile.open(uploaded_file_path, 'r|*') as tar_file:
            parser.global_threshold = 1000
            parser.threshold_percent = 5
            parser.load_tar_file(tar_file, uploaded_file_path)

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

    return JsonResponse(data, safe=False)
