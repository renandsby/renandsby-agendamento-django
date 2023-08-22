from django import forms

class Bootstrap5FormClassInjecter:
    @staticmethod
    def handle_field(field):
        match type(field.widget):
            case forms.widgets.TextInput:
                return Bootstrap5FormClassInjecter._handle_text(field)
            
            case forms.widgets.Select:
                return Bootstrap5FormClassInjecter._handle_select(field)
            
            case forms.widgets.NullBooleanSelect:
                return Bootstrap5FormClassInjecter._handle_select(field)
                
            case forms.widgets.SelectMultiple:
                return Bootstrap5FormClassInjecter._handle_select_multiple(field)
            
            case forms.widgets.CheckboxInput:
                return Bootstrap5FormClassInjecter._handle_checkbox(field)
            
            case forms.widgets.CheckboxSelectMultiple:
                return Bootstrap5FormClassInjecter._handle_checkbox(field)

            case forms.widgets.DateInput:
                return Bootstrap5FormClassInjecter._handle_date(field)

            case forms.widgets.DateTimeInput:
                return Bootstrap5FormClassInjecter._handle_datetime(field)
            
            case forms.widgets.SplitDateTimeWidget:
                return Bootstrap5FormClassInjecter._handle_split_datetime(field)
            
            case forms.widgets.TimeInput:
                return Bootstrap5FormClassInjecter._handle_time(field)

            case _:
                return Bootstrap5FormClassInjecter._handle_fallback(field)
    
    @staticmethod
    def _handle_text(field):
        field.widget.attrs['class'] = field.widget.attrs.get('class', "") + ' form-control'
     
    @staticmethod       
    def _handle_select(field):
        field.widget.attrs['class'] = field.widget.attrs.get('class', "") + ' form-select'
    
    @staticmethod       
    def _handle_select_multiple(field):
        field.widget.attrs['class'] = field.widget.attrs.get('class', "") + ' form-control'
        field.widget.attrs['style'] = field.widget.attrs.get('style', "") + " min-height:95%; height:150px;" 

    @staticmethod
    def _handle_checkbox(field):
        field.widget.attrs['class'] = field.widget.attrs.get('class', "") + ' form-check-input'
    
    @staticmethod
    def _handle_date(field):
        field.widget = forms.widgets.DateInput(format=f"%Y-%m-%d",attrs={"type":"date"})
        field.widget.attrs['class'] = field.widget.attrs.get('class', "") + ' form-control'
    
    @staticmethod
    def _handle_datetime(field):
        field.widget = forms.widgets.DateTimeInput(format=f"%Y-%m-%dT%H:%M",attrs={"type":"datetime-local"})
        field.widget.attrs['class'] = field.widget.attrs.get('class', "") + ' form-control'
    
    @staticmethod
    def _handle_split_datetime(field):
        field.widget.widgets[0].input_type = "date"
        field.widget.widgets[0].format = f"%Y-%m-%d"
        field.widget.widgets[0].attrs['class'] = field.widget.widgets[0].attrs.get('class', "") + ' mw-2 w-50 form-control mb-2'
        field.widget.widgets[1].input_type = "time"
        field.widget.widgets[1].attrs['class'] = field.widget.attrs.get('class', "") + ' ms-2 w-50 form-control mb-2'
        field.widget.widgets[1].attrs['step'] = "any"    
        
    @staticmethod
    def _handle_time(field):
        field.widget = forms.widgets.TimeInput(format=f"%H:%I", attrs={"type":"time"})
        field.widget.attrs['class'] = field.widget.attrs.get('class', "") + ' form-control'
        field.widget.attrs['step'] = "any"
    
    @staticmethod    
    def _handle_fallback(field):
        field.widget.attrs['class'] = field.widget.attrs.get('class', "") + ' form-control'