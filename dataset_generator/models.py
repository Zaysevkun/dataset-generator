from django.db import models


class DataType(models.Model):
    name = models.CharField(max_length=32)
    data_type = models.CharField(max_length=32)


class Schema(models.Model):
    class SeparatorChoices(models.TextChoices):
        COMMA = ',', 'comma(,)'
        SEMICOLON = ';', 'semicolon(;)'

    class StringCharacterChoices(models.TextChoices):
        DOUBLEQUOTE = '"', 'double-quote(")'
        QUOTE = '\'', 'quote(\')'

    name = models.CharField(max_length=32)
    separator = models.CharField(max_length=1, choices=SeparatorChoices.choices, default=SeparatorChoices.COMMA)
    string_character = models.CharField(
        max_length=1,
        choices=StringCharacterChoices.choices,
        default=StringCharacterChoices.DOUBLEQUOTE
    )
    modified = models.DateField(auto_now=True)
    fields = models.ManyToManyField(DataType, through='Field')


class Field(models.Model):
    schema = models.ForeignKey(Schema, models.CASCADE)
    datatype = models.ForeignKey(DataType, models.CASCADE)
    order = models.IntegerField(max_length=64)


class Dataset(models.Model):
    class StatusChoices(models.TextChoices):
        PROCESSING = 'processing'
        READY = 'ready'

    schema = models.ForeignKey(Schema, models.CASCADE)
    status = models.CharField(max_length=11, choices=StatusChoices.choices, default=StatusChoices.PROCESSING)
    file = models.FileField(upload_to='storage')
