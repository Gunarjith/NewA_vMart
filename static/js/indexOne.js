

    // --
const PlatformsId = document.getElementById('PlatformsId');
const listPlatformsId = document.getElementById('listPlatformsId');
const arrowUpId1 = document.getElementById('arrowUpId1');

// Function to close the list and reset the arrow image
function closeList() {
    listPlatformsId.style.display = 'none';
    arrowUpId1.src = './img/downArrow.png';
    servicesformsId.style.marginTop = '0px';
    blogId.style.marginTop = '0px';
    partnersId.style.marginTop = '0px';
    logOutId.style.marginTop = '0px';
}

// Add a click event listener to the "Platforms" link
PlatformsId.addEventListener("click", function(event) {
    // Toggle the display of the list and change the arrow image
    if (listPlatformsId.style.display === 'none' || listPlatformsId.style.display === '') {
        listPlatformsId.style.display = 'block';
        listServicessId.style.display = 'none' ;
        listBlogId.style.display = 'none';
        listPartnersId.style.display = 'none';
        arrowUpId1.src = './img/upArrrow.png';
        if (window.innerWidth <= 834) {
            servicesformsId.style.marginTop = '150px';
            blogId.style.marginTop = '0px';
            partnersId.style.marginTop = '0px';
            logOutId.style.marginTop = '0px';
            // servicesformsId.style.marginTop = '0px'
        }
        // servicesformsId.style.marginTop = '170px'
    } else {
        closeList();
    }

    // Prevent the click event from propagating to the document
    event.stopPropagation();
});

// Add a click event listener to the document to close the list when clicking anywhere outside of it
document.addEventListener("click", function() {
    if (listPlatformsId.style.display === 'block') {
        closeList();
    }
});



// -- 

const servicesformsId = document.getElementById('ServicestId');
const listServicessId = document.getElementById('listServicesId');
const arrowUpId2 = document.getElementById('arrowUpId2');

// Function to close the list and reset the arrow image
function closeList1() {
    listServicessId.style.display = 'none';
    arrowUpId2.src = './img/downArrow.png';
    servicesformsId.style.marginTop = '0px';
    blogId.style.marginTop = '0px';
    partnersId.style.marginTop = '0px';
    logOutId.style.marginTop = '0px';
}

// Add a click event listener to the "Platforms" link
servicesformsId.addEventListener("click", function(event) {
    //servicesformsIdToggle the display of the list and change the arrow image
    if (listServicessId.style.display === 'none' || listServicessId.style.display === '') {
        listServicessId.style.display = 'block';
        listBlogId.style.display = 'none';
        listPlatformsId.style.display = 'none';
        listPartnersId.style.display = 'none';
        arrowUpId2.src = './img/upArrrow.png';
        if (window.innerWidth <= 834) {
            blogId.style.marginTop = '120px';
            // servicesformsId.style.marginTop = '170px';
            servicesformsId.style.marginTop = '0px';
            partnersId.style.marginTop = '0px';
            logOutId.style.marginTop = '0px';
        }
    } else {
        closeList1();
    }

    // Prevent the click event from propagating to the document
    event.stopPropagation();
});

// Add a click event listener to the document to close the list when clicking anywhere outside of it
document.addEventListener("click", function() {
    if (listServicessId.style.display === 'block') {
        closeList1();
    }
});


// -- 

const blogId = document.getElementById('blogId');
const listBlogId = document.getElementById('listBlogId');
const arrowUpId3 = document.getElementById('arrowUpId3');

// Function to close the list and reset the arrow image
function closeList2() {
    listBlogId.style.display = 'none';
    arrowUpId3.src = './img/downArrow.png';
    servicesformsId.style.marginTop = '0px';
    blogId.style.marginTop = '0px';
    partnersId.style.marginTop = '0px';
    logOutId.style.marginTop = '0px';
}

// Add a click event listener to the "Platforms" link
blogId.addEventListener("click", function(event) {
    //servicesformsIdToggle the display of the list and change the arrow image
    if (listBlogId.style.display === 'none' || listBlogId.style.display === '') {
        listBlogId.style.display = 'block';
        listPlatformsId.style.display ='none';
        listServicessId.style.display = 'none' ;
        listPartnersId.style.display = 'none';
        arrowUpId3.src = './img/upArrrow.png';
        if (window.innerWidth <= 834) {
            partnersId.style.marginTop = '60px';
            blogId.style.marginTop = '0px';
            servicesformsId.style.marginTop = '0px';
            logOutId.style.marginTop = '0px';
        }
    } else {
        closeList2();
    }

    // Prevent the click event from propagating to the document
    event.stopPropagation();
});

// Add a click event listener to the document to close the list when clicking anywhere outside of it
document.addEventListener("click", function() {
    if (listBlogId.style.display === 'block') {
        closeList2();
    }
});


// -- 

const partnersId = document.getElementById('PartnersId');
const listPartnersId = document.getElementById('listPartnersId');
const arrowUpId4 = document.getElementById('arrowUpId4');
const logOutId = document.getElementById('logOutId');

// Function to close the list and reset the arrow image
function closeList3() {
    listPartnersId.style.display = 'none';
    arrowUpId4.src = './img/downArrow.png';
    servicesformsId.style.marginTop = '0px';
    logOutId.style.marginTop = '0px';
}

// Add a click event listener to the "Platforms" link
partnersId.addEventListener("click", function(event) {
    //servicesformsIdToggle the display of the list and change the arrow image
    if (listPartnersId.style.display === 'none' || listPartnersId.style.display === '') {
        listPartnersId.style.display = 'block';
        listBlogId.style.display = 'none';
        listPlatformsId.style.display = 'none';
        listServicessId.style.display = 'none';
        arrowUpId4.src = './img/upArrrow.png';
        if (window.innerWidth <= 834) {
            logOutId.style.marginTop = '60px';
            servicesformsId.style.marginTop = '0px';
            blogId.style.marginTop = '0px';
            partnersId.style.marginTop = '0px';
        }
    } else {
        closeList3();
    }

    // Prevent the click event from propagating to the document
    event.stopPropagation();
});

// Add a click event listener to the document to close the list when clicking anywhere outside of it
document.addEventListener("click", function() {
    if (listPartnersId.style.display === 'block') {
        closeList3();
    }
});


menuOpen = document.getElementById('menuOpen')
displayMbId = document.getElementById('displayMbId')
menuId = document.getElementById('menuId')

function closeList4() {
    displayMbId.style.display = 'none';
    menuId.src = './img/menuOpen.png';
}
menuOpen.addEventListener('click',function(){
    if(displayMbId.style.display === 'none' || displayMbId.style.display === '' ){
        displayMbId.style.display='block';
        menuId.src = './img/menuClose.png';
        blogId.style.marginTop = '0px';
    }
    else{
        closeList4();

    }
    event.stopPropagation();
})
// document.addEventListener("click", function() {
//     if (displayMbId.style.display === 'block') {
//         closeList4();
//     }
// });


const text = "Whatsapp";
const outputElement = document.getElementById("output");
let index = 0;
let direction = 1; // 1 for forward, -1 for backward

function updateText() {
  outputElement.textContent = text.slice(0, index);

  if (direction === 1) {
    index++;
    if (index > text.length) {
      direction = -1;
      setTimeout(updateText, 1000); // Pause before erasing
    } else {
      setTimeout(updateText, 100); // Type speed
    }
  } else {
    index--;
    if (index < 0) {
      direction = 1;
      setTimeout(updateText, 1000); // Pause before typing
    } else {
      setTimeout(updateText, 50); // Erase speed
    }
  }
}

updateText(); // Start the animation


// const slider = document.querySelector("[data-slider]");

// const track = slider.querySelector("[data-slider-track]");
// const prev = slider.querySelector("[data-slider-prev]");
// const next = slider.querySelector("[data-slider-next]");

// if (track) {
//   prev.addEventListener("click", () => {
//     next.removeAttribute("disabled");

//     track.scrollTo({
//       left: track.scrollLeft - track.firstElementChild.offsetWidth,
//       behavior: "smooth"
//     });
//   });

//   next.addEventListener("click", () => {
//     prev.removeAttribute("disabled");

//     track.scrollTo({
//       left: track.scrollLeft + track.firstElementChild.offsetWidth,
//       behavior: "smooth"
//     });
//   });

//   track.addEventListener("scroll", () => {
//     const trackScrollWidth = track.scrollWidth;
//     const trackOuterWidth = track.clientWidth;

//     prev.removeAttribute("disabled");
//     next.removeAttribute("disabled");

//     if (track.scrollLeft <= 0) {
//       prev.setAttribute("disabled", "");
//     }

//     if (track.scrollLeft === trackScrollWidth - trackOuterWidth) {
//       next.setAttribute("disabled", "");
//     }
//   });
// }

// const slider = document.querySelector("[data-slider]");
// const track = slider.querySelector("[data-slider-track]");
// const prev = slider.querySelector("[data-slider-prev]");
// const next = slider.querySelector("[data-slider-next]");

// if (track) {
//   prev.addEventListener("click", () => {
//     next.removeAttribute("disabled");

//     track.scrollTo({
//       left: track.scrollLeft - track.clientWidth, // Scroll by the width of the viewport
//       behavior: "smooth"
//     });
//   });

//   next.addEventListener("click", () => {
//     prev.removeAttribute("disabled");

//     track.scrollTo({
//       left: track.scrollLeft + track.clientWidth, // Scroll by the width of the viewport
//       behavior: "smooth"
//     });
//   });

//   track.addEventListener("scroll", () => {
//     prev.removeAttribute("disabled");
//     next.removeAttribute("disabled");

//     if (track.scrollLeft <= 0) {
//       prev.setAttribute("disabled", "");
//     }

//     if (track.scrollLeft >= track.scrollWidth - track.clientWidth) {
//       next.setAttribute("disabled", "");
//     }
//   });
// }



const slider = document.querySelector("[data-slider]");
const track = slider.querySelector("[data-slider-track]");
const prev = slider.querySelector("[data-slider-prev]");
const next = slider.querySelector("[data-slider-next]");

let numVisibleSlides = 0; // Number of visible slides based on container width

function updateVisibleSlides() {
  const containerWidth = slider.clientWidth;
  const slideWidth = track.firstElementChild.clientWidth + 20; // 20px for column-gap

  numVisibleSlides = Math.floor(containerWidth / slideWidth);
  const visibleTrackWidth = numVisibleSlides * slideWidth;
  track.style.width = visibleTrackWidth + "px";
}

if (track) {
  // Call updateVisibleSlides when the page loads and when the window is resized
  window.addEventListener("load", updateVisibleSlides);
  window.addEventListener("resize", updateVisibleSlides);

  prev.addEventListener("click", () => {
    next.removeAttribute("disabled");

    track.scrollTo({
      left: track.scrollLeft - track.clientWidth,
      behavior: "smooth",
    });
  });

  next.addEventListener("click", () => {
    prev.removeAttribute("disabled");

    track.scrollTo({
      left: track.scrollLeft + track.clientWidth,
      behavior: "smooth",
    });
  });

  track.addEventListener("scroll", () => {
    prev.removeAttribute("disabled");
    next.removeAttribute("disabled");

    if (track.scrollLeft <= 0) {
      prev.setAttribute("disabled", "");
    }

    if (track.scrollLeft >= track.scrollWidth - track.clientWidth) {
      next.setAttribute("disabled", "");
    }
  });
}


 