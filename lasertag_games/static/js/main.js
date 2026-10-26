document.addEventListener('DOMContentLoaded', function () {
  var button = document.getElementById('toggle-arena');
  var info = document.getElementById('arena-info');
  if (!button || !info) {
    return;
  }
  button.addEventListener('click', function () {
    info.hidden = !info.hidden;
    button.textContent = info.hidden ? 'Показать арену' : 'Скрыть арену';
  });
});
