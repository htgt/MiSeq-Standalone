from rest_framework import serializers
from point_mutation.models import PointMutationData

class PointMutationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PointMutationData
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