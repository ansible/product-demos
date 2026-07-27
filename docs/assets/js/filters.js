(function () {
  var categoryPills = document.querySelectorAll('[data-filter-category]');
  var items = document.querySelectorAll('.demo-card, .demo-row');
  var searchInput = document.getElementById('demo-search');
  var emptyState = document.getElementById('filter-empty');

  if (!items.length) return;

  var activeCategory = 'all';

  function itemMatchesCategory(item, category) {
    if (category === 'all') return true;
    return item.dataset.category === category;
  }

  function itemMatchesSearch(item, query) {
    if (!query) return true;
    var haystack = (item.dataset.search || '').toLowerCase();
    return haystack.indexOf(query) >= 0;
  }

  function setActivePill(category) {
    categoryPills.forEach(function (pill) {
      pill.classList.toggle('active', pill.dataset.filterCategory === category);
    });
  }

  function applyFilters() {
    var query = searchInput ? searchInput.value.trim().toLowerCase() : '';
    var visibleCount = 0;

    items.forEach(function (item) {
      var show =
        itemMatchesCategory(item, activeCategory) &&
        itemMatchesSearch(item, query);
      item.classList.toggle('hidden', !show);
      if (show) visibleCount += 1;
    });

    document.querySelectorAll('.section').forEach(function (section) {
      var visible = section.querySelectorAll(
        '.demo-card:not(.hidden), .demo-row:not(.hidden)'
      ).length;
      section.style.display = visible > 0 ? '' : 'none';
    });

    var divider = document.querySelector('.section-divider');
    if (divider) {
      var featured = document.getElementById('featured');
      var allDemos = document.getElementById('all-demos');
      var showDivider =
        featured &&
        featured.style.display !== 'none' &&
        allDemos &&
        allDemos.style.display !== 'none';
      divider.style.display = showDivider ? '' : 'none';
    }

    if (emptyState) {
      emptyState.classList.toggle('hidden', visibleCount > 0);
    }
  }

  function activateCategory(category) {
    activeCategory = category;
    setActivePill(category);
    applyFilters();
  }

  categoryPills.forEach(function (pill) {
    pill.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      activateCategory(pill.dataset.filterCategory);
    });

    pill.addEventListener('mousedown', function (e) {
      e.preventDefault();
    });

    pill.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        activateCategory(pill.dataset.filterCategory);
      }
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault();
        var pillsArr = Array.prototype.slice.call(categoryPills);
        var idx = pillsArr.indexOf(pill);
        var next =
          e.key === 'ArrowRight'
            ? pillsArr[(idx + 1) % pillsArr.length]
            : pillsArr[(idx - 1 + pillsArr.length) % pillsArr.length];
        next.focus();
      }
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', applyFilters);
  }

  document.querySelectorAll('.demo-row[data-href]').forEach(function (row) {
    row.addEventListener('click', function (e) {
      if (e.target.closest('a')) return;
      var href = row.dataset.href;
      if (href && href !== '#') {
        window.location.href = href;
      }
    });
  });

  applyFilters();
})();
