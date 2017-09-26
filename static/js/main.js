//select elements
var addBtn = document.getElementById("formBtn");
var fietsnummer = document.getElementById("fietsnummer");
var merk = document.getElementById("merk");
var frametype = document.getElementById("frametype");
var kleur = document.getElementById("kleur");
var framenummer = document.getElementById("framenummer");
var gravpostcode = document.getElementById("gravpostcode");
var opmerkingen = document.getElementById("opmerkingen");
var errorMsg = document.getElementById("error-message");
var wordCount = document.getElementById("word-count")

addBtn.addEventListener('click', function(e) {
let elemList = [fietsnummer, merk, frametype, kleur, framenummer, gravpostcode];
  if ((fietsnummer.value.length <= 0) || (merk.value.length <= 0) || (frametype.value.length <= 0) ||
  (framenummer.value.length <= 0) || (kleur.value.length <= 0) ||
  (gravpostcode.value.length <= 0)) {
    for (let item of elemList) {
      if (item.value.length <= 0) {
        item.style.borderColor = "#ff3a3a";
      } else {
        item.style.borderColor = "#c9e6ff";
      }
    }
    errorMsg.innerHTML = "&times; Niet alle verplichte velden zijn ingevuld";
    e.preventDefault();
  } else {
    return false;
  }
});


opmerkingen.addEventListener('keyup', function() {
  if (opmerkingen.value.length <= 200) {
    wordCount.innerHTML = 200 - opmerkingen.value.length;
  }
})
