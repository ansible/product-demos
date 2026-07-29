(function () {
  var toc = document.querySelector('.demo-toc');
  var body = document.querySelector('.detail-body');

  /*
   * Enforced section order on every demo detail page:
   *
   *  1. Description          (lead paragraph — already first in markdown)
   *  2. Workflow              (Mermaid diagram, rendered by layout)
   *  3. Video walkthrough     (YouTube embed, rendered by layout)
   *  4. Prerequisites         ── from markdown ──
   *  5. Configure credentials
   *  6. Survey prompts
   *  7. Job templates
   *  8. Why it matters
   *  9. Presenter walkthrough
   * 10. Talking points
   * 11. Related demos
   */

  /* Move Workflow and Video into the detail-body, right after the lead
     paragraph(s) and before the first <h2>. */
  if (body) {
    var workflow = document.getElementById('workflow');
    var video = document.getElementById('video');
    var firstH2 = body.querySelector('h2');

    if (firstH2) {
      if (video) {
        body.insertBefore(video, firstH2);
      }
      if (workflow) {
        body.insertBefore(workflow, video || firstH2);
      }
    }
  }

  if (!toc || !body) return;

  /* ── Build sidebar TOC ─────────────────────────────────────── */

  /* Collect all h2s now present in the body (including moved sections) */
  var allH2s = body.querySelectorAll('h2');

  /* Remove any static TOC links — we rebuild from scratch */
  var oldLinks = toc.querySelectorAll('.demo-toc__link');
  oldLinks.forEach(function (l) { l.remove(); });

  allH2s.forEach(function (h2) {
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

  /* ── Wrap prerequisites list in a callout box ──────────────── */
  allH2s.forEach(function (h2) {
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

  /* ── Highlight active TOC link on scroll ───────────────────── */
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
