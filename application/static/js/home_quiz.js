(function () {
  "use strict";

  var form = document.getElementById("home-quiz-form");
  if (!form) return;

  form.addEventListener("change", function (e) {
    if (!e.target.matches('input[type="radio"]')) return;
    window.setTimeout(function () {
      form.submit();
    }, 220);
  });
})();
