(function () {
  var toc = document.querySelector('.demo-toc');
  if (!toc) return;

  var body = document.querySelector('.detail-body');
  if (!body) return;

  /* Auto-build TOC from h2 headings in the markdown body — appended after
     the static Workflow / Video links so the sidebar order matches the page. */
  var headings = body.querySelectorAll('h2');
  headings.forEach(function (h2) {
    if (!h2.id) {
      h2.id = h2.textContent
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '');
    }
    var link = document.createElement('a');
    link.href = '#' + h2.id;
    link.className = 'demo-toc__link';
    link.textContent = h2.textContent.trim();
    toc.appendChild(link);
  });

  /* Wrap prerequisites list in a callout box */
  headings.forEach(function (h2) {
    if (h2.textContent.trim().toLowerCase() === 'prerequisites') {
      var ul = h2.nextElementSibling;
      if (ul && (ul.tagName === 'UL' || ul.tagName === 'OL')) {
        var box = document.createElement('div');
        box.className = 'prereq-box';
        ul.parentNode.insertBefore(box, ul);
        box.appendChild(ul);
      }
    }
  });

  /* Highlight active TOC link on scroll */
  var links = toc.querySelectorAll('.demo-toc__link');
  var sections = [];
  links.forEach(function (link) {
    var id = link.getAttribute('href').slice(1);
    var el = document.getElementById(id);
    if (el) sections.push({ id: id, el: el, link: link });
  });

  function setActive(id) {
    links.forEach(function (link) {
      link.classList.toggle('active', link.getAttribute('href') === '#' + id);
    });
  }

  if ('IntersectionObserver' in window && sections.length) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) setActive(entry.target.id);
        });
      },
      { rootMargin: '-20% 0px -60% 0px', threshold: 0 }
    );
    sections.forEach(function (s) { observer.observe(s.el); });
  }
})();
