const screenBanner = document.getElementById('screen-banner');
const addAllBtn = document.getElementById('add-all-btn');


addAllBtn.addEventListener('click', addAll);


function deleteFiets(nummer){

    let f = JSON.parse(localStorage.getItem('fietsen'));

    for (let i = 0; i < f.fietsen.length; i++) {
        if (f.fietsen[i].id == nummer) {
            f.fietsen.splice(i, 1);
            screenBanner.style.display = 'block';
            screenBanner.innerHTML = `<p id="err-msg">
                                      Fiets nummer ${nummer} is succesvol verwijderd uit de lokale opslag!
                                      </p>`;
            setTimeout(function() {screenBanner.style.display = 'none'}, 10000);
        }
    }

    localStorage.setItem('fietsen', JSON.stringify(f));

    fetchFiets();
}


function addFiets(nummer){

    let f = JSON.parse(localStorage.getItem('fietsen'));

    for (let i = 0; i < f.fietsen.length; ++i) {
        if (f.fietsen[i].id == nummer) {
            var listIndex = i;
            var jdata = f.fietsen[listIndex];
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/add_fiets");
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(JSON.stringify(jdata));

            xhr.onload = function() {
                let data = JSON.parse(xhr.responseText)
                switch (data.Code) {
                    case 200:
                        if (data.Duplicate == "true") {
                            screenBanner.style.display = 'block'
                            screenBanner.innerHTML = `<p id="err-msg">
                                                      Het lijkt erop dat fiets nummer ${jdata.Nummer} al in gebruik is...
                                                      We hebben het nummer voor je veranderd en de fiets succesvol toegevoegd! Het nieuwe nummer is: ${data.Nummer}
                                                      </p>`;

                            //f.fietsen.splice(listIndex, 1);
                            localStorage.setItem('fietsen', JSON.stringify(f));

                            setTimeout(function() {screenBanner.style.display = 'none'}, 10000);
                        } else {
                            screenBanner.style.display = 'block';
                            screenBanner.innerHTML = `<p id="err-msg">
                                                     Fiets nummer ${data.Nummer} is succesvol toegevoegd aan de database!
                                                     </p>`;

                            //f.fietsen.splice(listIndex, 1);
                            localStorage.setItem('fietsen', JSON.stringify(f));

                            setTimeout(function() {screenBanner.style.display = 'none'}, 10000);
                        }
                        break;
                    case 500:
                        screenBanner.style.display = 'block';
                        screenBanner.innerHTML = `<p id="err-msg">
                                                  Er is iets mis gegaan. ${data.Message}
                                                  </p>`;
                        setTimeout(function() {screenBanner.style.display = 'none'}, 10000);
                        break;
                    case 501:
                        screenBanner.style.display = 'block';
                        screenBanner.innerHTML = `<p id="err-msg">
                                                  Er is iets mis gegaan. ${data.Message}
                                                  </p>`;
                        setTimeout(function() {screenBanner.style.display = 'none'}, 10000);
                        break;
                }
            }
        }
    }

    fetchFiets();
}


function fetchFiets() {
    let f = JSON.parse(localStorage.getItem('fietsen')).fietsen;
    var fOutput = document.getElementById('fietsen-output');

    fOutput.innerHTML = '';

    for (let i of f) {
        var id = i.id;
        var Nummer = i.Nummer;
        var Merk = i.Merk;
        var Kleur = i.Kleur;

        fOutput.innerHTML += `<li>
                              ${Nummer}, ${Merk}, ${Kleur}
                              <a onclick="deleteFiets('${id}')"
                              class="btn-delete right"
                              href="#">x</a>
                              <a onclick="addFiets('${id}')"
                              class="btn-add right"
                              href="#">Verwerk</a></li>`;
    }
}


function addAll() {
    let f = JSON.parse(localStorage.getItem('fietsen'));
    const arrayLength = f.fietsen.length;
    var timeoutID;


    for (let i = 0; i < f.fietsen.length; ++i) {
        var jdata = f.fietsen[i];
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/add_fiets");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(jdata));
    }

    f.fietsen.splice(0, arrayLength);
    localStorage.setItem('fietsen', JSON.stringify(f));
    fetchFiets();
}


fetchFiets();
