if (window.location.pathname == '/about') {   
    let carouselFirst = document.querySelector(".carousel");
    let firstCardWidth = document.querySelector(".card").offsetWidth;
    let arrowBtns = document.querySelectorAll(".founders-container svg");

    arrowBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            carouselFirst.scrollLeft += btn.id === "left" ? -firstCardWidth : firstCardWidth;
        });
    });
}
