var cells = document.getElementsByTagName('td');
// Itera sobre cada celda
for (var i = 0; i < cells.length; i++) {

    var text = cells[i].innerText;

    var wrappedText = text.replace(/(.{50}(?:\s|$))/g, "$1\n");

    cells[i].innerText = wrappedText;
}