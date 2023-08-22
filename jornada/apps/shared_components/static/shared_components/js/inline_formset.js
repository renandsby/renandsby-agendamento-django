function add_formset(event,formset){
  event.preventDefault();
  var form_idx = $('#id_'+formset+'-TOTAL_FORMS').val();
  $('#'+formset+'_formset').append($('#'+formset+'_empty_form').html().replace(/__prefix__/g, form_idx));
  $('#id_'+formset+'-TOTAL_FORMS').val(parseInt(form_idx) + 1);
  $( document ).trigger( "inlineformset_added");
}

