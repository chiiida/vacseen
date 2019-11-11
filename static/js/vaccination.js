function addVaccine() {
    let vaccGroup = document.getElementsByClassName('vaccgroup')[0];
    vaccGroup.innerHTML += '<div class="row m-auto"><div class="dot-outer"><div class="dot-inner"></div></div><form method="post" class="col-lg-12"><input class="col-lg-6 form-control-vacc vacc-name" placeholder="Vaccine name" /><select class="col-lg-2 form-control-vacc vacc-dose"><option selected>Dose 1</option><option>Dose 2</option></select><input class="col-lg-2 form-control-vacc vacc-date" type="date" max="3000-12-31"placeholder="Expired" /></form></div>';
}
