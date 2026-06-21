(function () {
  "use strict";

  var form = document.getElementById("assessment-form");
  if (!form) return;

  var slides = Array.prototype.slice.call(form.querySelectorAll(".kegel-slide"));
  var progressFill = document.getElementById("progress-fill");
  var progressPct = document.getElementById("progress-pct");
  var total = window.QUIZ_TOTAL || slides.length;
  var offset = window.QUIZ_PROGRESS_OFFSET || 0;
  var current = typeof window.QUIZ_START === "number" ? window.QUIZ_START : 0;

  if (current < 0 || current >= slides.length) current = 0;

  function currentSlide() {
    return slides[current];
  }

  function isMulti(slide) {
    return slide.getAttribute("data-multi") === "true";
  }

  function isLast() {
    return current === slides.length - 1;
  }

  function updateProgress() {
    var pct = Math.round(((offset + current + 1) / total) * 100);
    if (progressFill) progressFill.style.width = pct + "%";
    if (progressPct) progressPct.textContent = pct + "%";
  }

  function showSlide(index) {
    if (index < 0 || index >= slides.length) return;

    slides.forEach(function (slide, i) {
      var active = i === index;
      slide.classList.toggle("is-active", active);
      slide.setAttribute("aria-hidden", active ? "false" : "true");
      slide.style.display = active ? "block" : "none";
    });

    var target = slides[index];
    target.classList.add("is-animating");
    window.setTimeout(function () {
      target.classList.remove("is-animating");
    }, 260);

    current = index;
    updateProgress();
    window.scrollTo(0, 0);
  }

  function validateSlide(slide) {
    var options = slide.querySelector(".kegel-options");
    if (options) options.classList.remove("has-error");

    var radios = slide.querySelectorAll('input[type="radio"][required]');
    if (radios.length) {
      var name = radios[0].name;
      if (!slide.querySelector('input[name="' + name + '"]:checked')) {
        if (options) options.classList.add("has-error");
        return false;
      }
    }

    var checks = slide.querySelectorAll('input[type="checkbox"]');
    if (checks.length) {
      var cname = checks[0].name;
      if (!slide.querySelector('input[name="' + cname + '"]:checked')) {
        if (options) options.classList.add("has-error");
        return false;
      }
    }

    return true;
  }

  function goNext() {
    if (!validateSlide(currentSlide())) return;
    if (current < slides.length - 1) showSlide(current + 1);
  }

  function goBack() {
    if (current > 0) showSlide(current - 1);
  }

  form.addEventListener("change", function (e) {
    var input = e.target;
    if (!input.matches('input[type="radio"], input[type="checkbox"]')) return;

    var slide = input.closest(".kegel-slide");
    if (!slide || !slide.classList.contains("is-active")) return;

    var options = slide.querySelector(".kegel-options");
    if (options) options.classList.remove("has-error");

    if (input.type === "radio" && !isMulti(slide) && !isLast()) {
      window.setTimeout(goNext, 280);
    }
  });

  form.addEventListener("click", function (e) {
    if (e.target.classList.contains("btn-back-home")) {
      e.preventDefault();
      window.location.href = "/";
      return;
    }
    if (e.target.classList.contains("btn-next")) {
      e.preventDefault();
      goNext();
    }
    if (e.target.classList.contains("btn-back")) {
      e.preventDefault();
      goBack();
    }
  });

  form.addEventListener("submit", function (e) {
    if (!validateSlide(currentSlide())) e.preventDefault();
  });

  showSlide(current);
})();
