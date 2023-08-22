from django.forms.widgets import ClearableFileInput, SplitDateTimeWidget, DateInput, TimeInput


class CustomPictureInput(ClearableFileInput):
    initial_text = "Foto Atualmente"
    input_text = "Alterar a Foto"
    template_name = "core/widgets/custom_picture_input.html"

class CustomAttachmentInput(ClearableFileInput):
    initial_text = ""
    input_text = "Alterar"
    template_name = "core/widgets/custom_attachment_input.html"


class CustomSplitDateTimeWidget(SplitDateTimeWidget):
    template_name = "core/widgets/custom_split_datetime.html"
    
    def __init__(
        self, 
        date_format=None,
        time_format=None,
    ):
        date_attrs = {
            "type" : "date",
            "class" : "form-control"
        }
        time_attrs = {
            "type":"time",
            "step":"any",
            "class" : "form-control"
        }
        
        super().__init__(date_attrs=date_attrs, time_attrs=time_attrs, date_format=date_format, time_format=time_format)
        
      