from django.db import models

# Create your models here.
class PointMutationData(models.Model):
    aligned_sequence = models.CharField(max_length=255, default='')
    reference_sequence = models.CharField(max_length=255, default='')
    nhej = models.BooleanField(default=False)
    unmodified = models.BooleanField(default=False)
    hdr = models.BooleanField(default=False)
    n_deleted = models.DecimalField(max_digits=40, decimal_places=2, default = 0.0)
    n_inserted = models.DecimalField(max_digits=40, decimal_places=2, default = 0.0)
    n_mutated = models.DecimalField(max_digits=40, decimal_places=2, default = 0.0)
    n_reads = models.DecimalField(max_digits=40, decimal_places=2, default = 0.0)
    p_reads = models.DecimalField(max_digits=40, decimal_places=2, default = 0.0)
    experiment = models.CharField(max_length=255, default='')
