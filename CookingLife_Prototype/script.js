const urlParams = new URLSearchParams(window.location.search);
const productSlug = urlParams.get("product");

const images = ["assets/img1.jpg", "assets/img2.jpg"];
let current = 0;

const carouselImg = document.getElementById("carousel-img");
const uspOverlay = document.getElementById("usp-overlay");
const uspList = document.getElementById("usp-list");

let usps = [];

if (productSlug) {
  fetch(`usps_${productSlug}.json`)
    .then(response => {
      if (!response.ok) throw new Error("USP file not found.");
      return response.json();
    })
    .then(data => {
      usps = data;
    })
    .catch(err => {
      console.error("Could not load USPs:", err);
    });
}

// Carousel navigation
document.getElementById("next").addEventListener("click", () => {
  current = (current + 1) % images.length;
  carouselImg.src = images[current];
  checkOverlay();
});

document.getElementById("prev").addEventListener("click", () => {
  current = (current - 1 + images.length) % images.length;
  carouselImg.src = images[current];
  checkOverlay();
});

function checkOverlay() {
  if (current === 1 && usps.length > 0) {
    uspOverlay.classList.remove("hidden");
    uspList.innerHTML = "";
    usps.forEach(usp => {
      const li = document.createElement("li");
      li.textContent = usp;
      uspList.appendChild(li);
    });
  } else {
    uspOverlay.classList.add("hidden");
  }
}