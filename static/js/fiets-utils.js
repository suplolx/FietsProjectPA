function deleteFiets(nummer){
    let f = JSON.parse(localStorage.getItem('fietsen'));

    for (var i = 0; i < f.fietsen.length; i++) {
        console.log(nummer)
        console.log(f.fietsen[i].Nummer)
        if (f.fietsen[i].Nummer == nummer) {
            console.log("if true")
            f.fietsen.splice(i, 1);
        }
    }
    localStorage.setItem('fietsen', JSON.stringify(f));

    fetchFiets();

}

function fetchFiets() {
    var f = JSON.parse(localStorage.getItem('fietsen')).fietsen;
    var fOutput = document.getElementById('fietsen-output');

    fOutput.innerHTML = '';

    for (var i = 0; i < f.length; i++) {
        var Nummer = f[i].Nummer;
        var Merk = f[i].Merk;
        var Kleur = f[i].Kleur;

        fOutput.innerHTML += '<li>'+ Nummer + ', ' + Merk + ', ' + Kleur + '<a onclick="deleteFiets(' +Nummer+ ')" class="btn-delete" href="#">Verwerk</a></li>';
    }
}

fetchFiets();