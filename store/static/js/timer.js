function updateRemainingTime() {
  fetch('/remaining_time')
  .then(response => response.json())
  .then(data => {
   let remainingSeconds = data.remaining_time_in_seconds;
   let days = Math.floor(remainingSeconds / 86400);
   let hours = Math.floor((remainingSeconds % 86400) / 3600);
   let minutes = Math.floor((remainingSeconds % 3600) / 60);
   let seconds = Math.floor(remainingSeconds % 60);
   if(seconds < 10 && seconds >= 0) {
     seconds = "0" + seconds;
   }
   document.getElementById('days').innerHTML = days
   document.getElementById('hours').innerHTML = hours
   document.getElementById('minutes').innerHTML = minutes
   document.getElementById('seconds').innerHTML = seconds
  })
}

if (window.location.pathname == '/home' || window.location.pathname == '/') {  
  setInterval(updateRemainingTime, 1000)
}