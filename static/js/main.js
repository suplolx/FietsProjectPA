const fNum = document.getElementById('fietsnummer');
const fMer = document.getElementById('merk');
const fFraTyp = document.getElementById('frametype');
const fKle = document.getElementById('kleur');
const fGra = document.getElementById('gravpostcode');
const fFraNum = document.getElementById('framenummer');
const fOpm = document.getElementById('opmerkingen');
const popUp = document.getElementById('screen-banner');
const formSub = document.getElementById('registratie-form');

formSub.addEventListener('submit', function(e) {
    var networkStatus = navigator.onLine ? true : false;
    if (!networkStatus) {
        e.preventDefault();
        popUp.innerHTML = '';
        if (!localStorage.getItem('fietsen')) {
            var offlineToegevoegd = {
                fietsen: [],
            };
            localStorage.setItem('fietsen', JSON.stringify(offlineToegevoegd));
        }
        var f = JSON.parse(localStorage.getItem('fietsen'));
        var fiets = {
            Nummer: fNum.value,
            Merk: fMer.value,
            FrameType: fFraTyp.value,
            Kleur: fKle.value,
            Framenummer: fFraNum.value,
            Gegraveerde_postcode: fGra.value,
            Opmerkingen: fOpm.value,
            Datum: Date.now(),
        }

        f.fietsen.push(fiets);

        localStorage.setItem('fietsen', JSON.stringify(f));

        popUp.innerHTML = '<p id="err-msg"> Fiets nummer ' + fiets.Nummer + ' toegevoegd!</p>';
        popUp.style.display = 'block';

        return false;
    } else {
        return true;
    }
})