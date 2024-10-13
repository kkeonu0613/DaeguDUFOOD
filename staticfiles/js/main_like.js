document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // 기본 클릭 동작 방지
            const restaurantId = this.dataset.restaurantId; // 식당 ID 가져오기
            const heartIcon = this.querySelector('.heart-icon'); // 하트 아이콘
            const isAuthenticated = this.dataset.isAuthenticated === 'true'; // 사용자 인증 여부

            if (!isAuthenticated) {
                alert("로그인이 필요합니다.");
                window.location.href = "/login/";
                return;
            }

            // 현재 하트 상태 확인
            const isLiked = heartIcon.classList.contains('filled');

            fetch(`/like/restaurant/${restaurantId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken, // CSRF 토큰
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.likes !== undefined) {
                    // 아이콘 상태 변경
                    if (!isLiked) {
                        heartIcon.classList.add('filled'); // 좋아요 추가
                        heartIcon.style.color = 'red'; // 색상 변경
                        alert("좋아요를 눌렀습니다!"); // 메시지 출력
                    } else {
                        heartIcon.classList.remove('filled'); // 좋아요 제거
                        heartIcon.style.color = 'gray'; // 색상 변경
                        alert("좋아요를 취소했습니다!"); // 메시지 출력
                    }

                    // main 페이지로 리다이렉트
                    window.location.href = mainUrl; // main 페이지로 이동
                } else {
                    alert(data.message || '오류가 발생했습니다. 다시 시도해 주세요.'); // 오류 메시지 출력
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("오류가 발생했습니다. 다시 시도해 주세요.");
            });
        });
    });
});
