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
      var visible = section.querySelectorAll('.demo-card:not(.hidden), .demo-row:not(.hidden)').length;
      section.style.display = visible > 0 ? '' : 'none';
    });

    if (emptyState) {
      emptyState.classList.toggle('hidden', visibleCount > 0);
    }
  }

  categoryPills.forEach(function (pill) {
    pill.addEventListener('click', function () {
      activeCategory = pill.dataset.filterCategory;
      setActivePill(activeCategory);
      applyFilters();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', applyFilters);
  }

  applyFilters();
})();
