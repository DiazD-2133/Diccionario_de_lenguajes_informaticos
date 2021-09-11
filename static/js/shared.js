/* Buscar Las clases o selectors en el documento html */
var itemsList = document.querySelector('.items');
var lareralBar = document.querySelector('.lareral-bar');
var backdrop = document.querySelector('.backdrop');


lareralBar.addEventListener('click', function() {
    /* mobileNav.style.display = 'block'; Entra en la propiedad 'Display' de la clase */
    lareralBar.classList.remove('movil-lareral-bar')

    lareralBar.classList.add('mobile-nav__items'); /* Agregar una clase al objeto seleccionado */

    backdrop.classList.add('open');
    itemsList.classList.add('open');
});


if (backdrop) {
    backdrop.addEventListener('click', function() {
        lareralBar.classList.remove('mobile-nav__items');
        lareralBar.classList.add('movil-lareral-bar')
        backdrop.classList.remove('open');
        itemsList.classList.remove('open');
    });
}

var items = document.querySelectorAll('.item_a');

for (var i = 0; i < items.length; i++) {
  items[i].addEventListener("click", function() {
    var current = document.querySelector("active");
    if (current) {
      current.classList.remove("active");
   }
    this.classList.add('active');
  });
}
