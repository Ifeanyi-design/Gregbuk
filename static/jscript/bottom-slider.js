const slider = document.getElementById('slider2');
const btnLeft = document.getElementById('btn-left2');
const btnRight = document.getElementById('btn-right2');

let products = Array.from(slider.children);
const gap = 10; // same as your CSS gap
const productWidth = products[0].offsetWidth + gap;

// Clone enough times to simulate "infinite" scrolling
for (let i = 0; i < 5; i++) {  // adjust number if you have many products
  products.forEach(p => slider.appendChild(p.cloneNode(true)));
}

// Button scroll
btnLeft.addEventListener('click', () => {
  slider.scrollBy({ left: -productWidth, behavior: 'smooth' });
});
btnRight.addEventListener('click', () => {
  slider.scrollBy({ left: productWidth, behavior: 'smooth' });
});

// Optional: drag to scroll
let isDown = false;
let startX;
let scrollLeft;

slider.addEventListener('mousedown', (e) => {
  isDown = true;
  slider.classList.add('active'); // optional styling
  startX = e.pageX - slider.offsetLeft;
  scrollLeft = slider.scrollLeft;
});
slider.addEventListener('mouseleave', () => {
  isDown = false;
  slider.classList.remove('active');
});
slider.addEventListener('mouseup', () => {
  isDown = false;
  slider.classList.remove('active');
});
slider.addEventListener('mousemove', (e) => {
  if(!isDown) return;
  e.preventDefault();
  const x = e.pageX - slider.offsetLeft;
  const walk = (x - startX) * 2; // scroll-fast multiplier
  slider.scrollLeft = scrollLeft - walk;
});