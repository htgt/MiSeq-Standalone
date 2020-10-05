from rest_framework import serializers
from crispresso_upload.models import CrispressoData

class CrispressoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrispressoData
        fields = (
            'aligned_sequence',
            'reference_sequence',
            'nhej',
            'unmodified',
            'hdr',
            'n_deleted',
            'n_inserted',
            'n_mutated',
            'n_reads',
            'p_reads',
            'experiment'
        )