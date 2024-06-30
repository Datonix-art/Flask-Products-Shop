document.getElementById("dropdownLink").onclick = function(event) {
  event.preventDefault(); 
  let dropdown = document.getElementById("dropdownMenu");
  if (dropdown.style.display === "block") {
      dropdown.style.display = "none";
  } else {
      dropdown.style.display = "block";
  }
};