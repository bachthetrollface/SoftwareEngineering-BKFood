const community = document.getElementById("community");
const hiddenElement = document.querySelector(".subnav");

// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


community.addEventListener("mouseover", () => {
  hiddenElement.style.display = "block";
});
hiddenElement.addEventListener("mouseover", () => {
  hiddenElement.style.display = "block";
});

community.addEventListener("mouseout", () => {
  hiddenElement.style.display = "none";
});
hiddenElement.addEventListener("mouseout", () => {
  hiddenElement.style.display = "none";
});