const images = [
  { src: "assets/img1.jpg", type: "usps" },
  { src: "assets/img2.jpg", type: "dimensions" },
  { src: "assets/img3.jpg", type: "items_included" }
];

let current = 0;
let productData = {};

const carouselImg = document.getElementById("carousel-img");
const overlay = document.getElementById("overlay");
const overlayTitle = document.getElementById("overlay-title");
const overlayList = document.getElementById("overlay-list");

const params = new URLSearchParams(window.location.search);
const productSlug = params.get("product");
const dataFile = `usps_${productSlug}.json`;

fetch(dataFile)
  .then(res => res.json())
  .then(data => {
    productData = data;
    updateOverlay();
  })
  .catch(err => {
    console.error("Could not load product JSON:", err);
  });

document.getElementById("next").addEventListener("click", () => {
  current = (current + 1) % images.length;
  updateCarousel();
});

document.getElementById("prev").addEventListener("click", () => {
  current = (current - 1 + images.length) % images.length;
  updateCarousel();
});

function updateCarousel() {
  carouselImg.src = images[current].src;
  updateOverlay();
}

function updateOverlay() {
  overlayList.innerHTML = "";

  const type = images[current].type;
  const list = productData[type];

  if (list && Object.keys(list).length > 0) {
    overlay.classList.remove("hidden");
    overlayTitle.textContent =
      type === "usps"
        ? "Voordelen"
        : type === "dimensions"
        ? "Afmetingen"
        : "Inhoud verpakking";

    if (Array.isArray(list)) {
      list.forEach(usp => {
        const li = document.createElement("li");
        li.textContent = usp;
        overlayList.appendChild(li);
      });
    } else {
      for (const [key, val] of Object.entries(list)) {
        const li = document.createElement("li");
        li.textContent = `${key}: ${val}`;
        overlayList.appendChild(li);
      }
    }
  } else {
    overlay.classList.add("hidden");
  }
}