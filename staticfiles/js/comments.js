$(document).ready(function () {
    "use strict";

    // 댓글 입력 시 글자 수 카운팅
    $('#comment-input').on('input', function () {
        const length = $(this).val().length;
        $('#char-count').text(length + ' / 200');
    });

    window.editComment = function(commentId) {
        // 기존 댓글 내용을 숨기고 수정 폼을 표시
        document.getElementById('comment-content-' + commentId).style.display = 'none';
        document.getElementById('edit-comment-' + commentId).style.display = 'block';
        
        // 수정 및 삭제 버튼 숨기기
        const editActions = document.querySelectorAll('.comment-actions');
        editActions.forEach(actions => {
            const editButton = actions.querySelector('.btn-edit');
            const deleteButton = actions.querySelector('.btn-danger');
            if (editButton) {
                editButton.style.display = 'none'; // 수정 버튼 숨기기
            }
            if (deleteButton) {
                deleteButton.style.display = 'none'; // 삭제 버튼 숨기기
            }
        });
    };
    
    window.cancelEdit = function(commentId) {
        // 수정 폼을 숨기고 기존 댓글 내용을 다시 표시
        document.getElementById('edit-comment-' + commentId).style.display = 'none';
        document.getElementById('comment-content-' + commentId).style.display = 'block';
        
        // 수정 및 삭제 버튼 다시 보이기
        const editActions = document.querySelectorAll('.comment-actions');
        editActions.forEach(actions => {
            const editButton = actions.querySelector('.btn-edit');
            const deleteButton = actions.querySelector('.btn-danger');
            if (editButton) {
                editButton.style.display = 'block'; // 수정 버튼 보이기
            }
            if (deleteButton) {
                deleteButton.style.display = 'block'; // 삭제 버튼 보이기
            }
        });
    };
    
    

    // AJAX 요청을 통한 좋아요 기능
    window.likePost = function (postId) {
        fetch(`/post/${postId}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        }).then(response => response.json())
            .then(data => {
                $('#like-count').text(data.likes);
            })
            .catch(error => console.error('Fetch error:', error));
    };

    // CSRF 토큰을 가져오는 함수
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie) {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
