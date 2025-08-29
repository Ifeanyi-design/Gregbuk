 const slider = document.getElementById('slider');
const btnLeft = document.getElementById('btn-left');
const btnRight = document.getElementById('btn-right');

let products = Array.from(slider.children);
const productWidth = products[0].offsetWidth + 10;

// Clone enough times to make “infinite” feel
for (let i = 0; i < 10; i++) {
  products.forEach(p => slider.appendChild(p.cloneNode(true)));
}

// Button scroll
btnLeft.addEventListener('click', () => slider.scrollBy({ left: -productWidth, behavior: 'smooth' }));
btnRight.addEventListener('click', () => slider.scrollBy({ left: productWidth, behavior: 'smooth' }));

// Let user scroll freely on touch/drag — no scrollLeft adjustments at all

// the theme modes code

