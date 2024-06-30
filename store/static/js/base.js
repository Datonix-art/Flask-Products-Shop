function navToggle() {
  const btn = document.getElementById('nav-btn')
  btn.addEventListener('click', () => {
    if (document.querySelector('.wrapper').classList.contains('toggle')) {
      document.querySelector('.wrapper').classList.remove('toggle')
    } else if (!document.querySelector('.wrapper').classList.contains('toggle')) {
      document.querySelector('.wrapper').classList.add('toggle')
    }
  })
}
navToggle()
