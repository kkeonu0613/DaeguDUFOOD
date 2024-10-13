document.addEventListener('DOMContentLoaded', function () {
    console.log('menuToggle.js loaded');
    var menuToggle = document.querySelector('.menu-toggle');
    var menuContent = document.querySelector('.menu-content');
    var searchBar = document.getElementById('search-bar');
    var searchBtn = document.getElementById('search-btn');
    var searchWarning = document.getElementById('search-warning');
    var searchInfo = document.getElementById('search-info');
    var currentPosition = document.getElementById('current-position');
    var totalKeywords = document.getElementById('total-keywords');
    var searchIndex = 0;
    var keyword = '';
    var previousKeyword = '';

    menuContent.style.display = 'none';
    searchBar.style.display = 'none';
    searchBtn.style.display = 'none';

    menuToggle.addEventListener('click', function () {
        var isMenuVisible = menuContent.style.display === 'block';

        if (isMenuVisible) {
            menuContent.style.display = 'none';
            searchBar.style.display = 'none';
            searchBtn.style.display = 'none';
        } else {
            menuContent.style.display = 'block';
            searchBar.style.display = 'block';
            searchBtn.style.display = 'block';
        }
    });

    function removeHighlights() {
        var highlightedElements = menuContent.querySelectorAll('.highlighted');
        highlightedElements.forEach(function (element) {
            element.outerHTML = element.innerHTML;
        });
    }

    function highlightKeyword(keyword) {
        removeHighlights();

        var content = menuContent.innerHTML;
        var escapedKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        var highlightedContent = content.replace(new RegExp(escapedKeyword, 'gi'), '<span class="highlighted">$&</span>');
        menuContent.innerHTML = highlightedContent;
    }

    function scrollToKeyword(index) {
        var highlightedElements = document.querySelectorAll('.highlighted');
        highlightedElements.forEach(function (element) {
            element.classList.remove('current-highlighted');
        });
        if (highlightedElements[index]) {
            highlightedElements[index].scrollIntoView({ behavior: 'smooth', block: 'center' });
            highlightedElements[index].classList.add('current-highlighted');
        }
    }

    function executeSearch() {
        var newKeyword = document.getElementById('search-bar').value.trim().toLowerCase();
        if (newKeyword === keyword) {
            return;
        }

        removeHighlights();

        if (newKeyword !== '') {
            highlightKeyword(newKeyword);
            keyword = newKeyword;

            var highlightedElements = document.querySelectorAll('.highlighted');
            totalKeywords.textContent = highlightedElements.length;
            currentPosition.textContent = 1;

            if (highlightedElements.length > 0) {
                highlightedElements[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                highlightedElements[0].classList.add('current-highlighted');
                searchWarning.style.display = 'none';  // 검색 결과가 있으면 경고 메시지 숨기기
                searchInfo.style.display = 'block';
            } else {
                searchWarning.style.display = 'block';  // 검색 결과가 없으면 경고 메시지 표시
                searchInfo.style.display = 'none';
            }
        } else {
            removeHighlights();
            searchInfo.style.display = 'none';
            searchWarning.style.display = 'none';
        }
    }

    document.getElementById('search-btn').addEventListener('click', function () {
        var keyword = document.getElementById('search-bar').value.trim().toLowerCase();
        if (keyword === previousKeyword) {
            return;
        } else {
            previousKeyword = keyword;
            executeSearch();

            totalKeywords.textContent = document.querySelectorAll('.highlighted').length;
            currentPosition.textContent = 1;
        }
    });

    document.getElementById('next-btn').addEventListener('click', function () {
        var highlightedElements = document.querySelectorAll('.highlighted');
        if (highlightedElements.length > 0) {
            searchIndex = (searchIndex + 1) % highlightedElements.length;
            currentPosition.textContent = searchIndex + 1;
            scrollToKeyword(searchIndex);
        }
    });
});
