//select elements

var errorMsg = document.getElementById("error-message");
var wordCount = document.getElementById("word-count")


opmerkingen.addEventListener('keyup', function() {
  if (opmerkingen.value.length <= 200) {
    wordCount.innerHTML = 200 - opmerkingen.value.length;
  }
})
