from django import forms


class ExplorerForm(forms.Form):
    service_type = forms.CharField(label='service type', max_length=100, )
    waveband = forms.CharField(label="waveband", max_length=100, )
