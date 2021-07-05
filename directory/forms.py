from django import forms


class ImportDataForm(forms.Form):
    data_csv_file = forms.FileField(
        widget=forms.FileInput(attrs={'accept': '.csv'}))
    images_zip_file = forms.FileField(
        widget=forms.FileInput(attrs={'accept': '.zip'}))
