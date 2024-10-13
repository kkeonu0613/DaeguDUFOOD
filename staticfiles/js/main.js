// main.js

function handlePageChange(event, page) {
    event.preventDefault(); // �⺻ ��ũ ������ �����ϴ�.

    fetch(`?page=${page}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest', // AJAX ��û���� ���
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // ������ ������ ������Ʈ
            updateRestaurantList(data.restaurants);
            updatePagination(data.has_previous, data.has_next, data.number, data.num_pages);
            // ��ũ�� ��ġ�� �������� ����
        })
        .catch(error => console.error('Error:', error));
}

function updateRestaurantList(restaurants) {
    const restaurantContainer = document.getElementById('restaurant-list'); // �Ĵ� ����� ǥ���� ���
    restaurantContainer.innerHTML = ''; // ���� ���� �����

    restaurants.forEach(restaurant => {
        const restaurantElement = `
            <div class="restaurant-item">
                <img src="${restaurant.image_url}" alt="${restaurant.name}">
                <h2>${restaurant.name}</h2>
                <p>����: ${restaurant.average_rating}</p>
                <p>��ġ: ${restaurant.location}</p>
                <p>${restaurant.first_review_text}</p>
            </div>
        `;
        restaurantContainer.innerHTML += restaurantElement; // ���ο� �Ĵ� �߰�
    });
}

function updatePagination(hasPrevious, hasNext, currentPage, totalPages) {
    const paginationContainer = document.querySelector('.step-links');
    paginationContainer.innerHTML = ''; // ���� ���� �����

    if (hasPrevious) {
        paginationContainer.innerHTML += `<a href="#" class="main-pagination-btn" onclick="handlePageChange(event, 1)">&laquo;</a>`;
        paginationContainer.innerHTML += `<a href="#" class="main-pagination-btn" onclick="handlePageChange(event, ${currentPage - 1})">��</a>`;
    }

    paginationContainer.innerHTML += `<span class="main-current">Page ${currentPage} of ${totalPages}.</span>`;

    if (hasNext) {
        paginationContainer.innerHTML += `<a href="#" class="main-pagination-btn" onclick="handlePageChange(event, ${currentPage + 1})">��</a>`;
        paginationContainer.innerHTML += `<a href="#" class="main-pagination-btn" onclick="handlePageChange(event, ${totalPages})">&raquo;</a>`;
    }
}