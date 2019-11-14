const datalist = '<datalist placeholder="Vaccine name" id="vaccine"><option value="BCG"><option value="HB1"><option value="HB2"><option value="DTP-HB1"><option value="OPV1"><option value="Hepatitis A"></datalist>';

function addVaccine() {
    let vaccGroup = document.getElementsByClassName('vaccgroup')[0];
    vaccGroup.innerHTML += '<form method="post" class="col-lg-12">{% csrf_token %}{{ form.vaccine_name }}' + datalist + '{{ form.dose_count }}<div class="vacc-date">{{ form.expired }}</div>'
}
