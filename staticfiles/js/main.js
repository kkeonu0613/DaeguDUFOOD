// main.js

function handlePageChange(event, page) {
    event.preventDefault(); // 기본 링크 동작을 막습니다.

    fetch(`?page=${page}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest', // AJAX 요청임을 명시
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // 페이지 데이터 업데이트
            updateRestaurantList(data.restaurants);
            updatePagination(data.has_previous, data.has_next, data.number, data.num_pages);
            // 스크롤 위치를 변경하지 않음
        })
        .catch(error => console.error('Error:', error));
}

function updateRestaurantList(restaurants) {
    const restaurantContainer = document.getElementById('restaurant-list'); // 식당 목록을 표시할 요소
    restaurantContainer.innerHTML = ''; // 기존 내용 지우기

    restaurants.forEach(restaurant => {
        const restaurantElement = `
            <div class="restaurant-item">
                <img src="${restaurant.image_url}" alt="${restaurant.name}">
                <h2>${restaurant.name}</h2>
                <p>평점: ${restaurant.average_rating}</p>
                <p>위치: ${restaurant.location}</p>
                <p>${restaurant.first_review_text}</p>
            </div>
        `;
        restaurantContainer.innerHTML += restaurantElement; // 새로운 식당 추가
    });
}

function updatePagination(hasPrevious, hasNext, currentPage, totalPages) {
    const paginationContainer = document.querySelector('.step-links');
    paginationContainer.innerHTML = ''; // 기존 내용 지우기

    if (hasPrevious) {
        paginationContainer.innerHTML += `<a href="#" class="main-pagination-btn" onclick="handlePageChange(event, 1)">&laquo;</a>`;
        paginationContainer.innerHTML += `<a href="#" class="main-pagination-btn" onclick="handlePageChange(event, ${currentPage - 1})">◀</a>`;
    }

    paginationContainer.innerHTML += `<span class="main-current">Page ${currentPage} of ${totalPages}.</span>`;

    if (hasNext) {
        paginationContainer.innerHTML += `<a href="#" class="main-pagination-btn" onclick="handlePageChange(event, ${currentPage + 1})">▶</a>`;
        paginationContainer.innerHTML += `<a href="#" class="main-pagination-btn" onclick="handlePageChange(event, ${totalPages})">&raquo;</a>`;
    }
}