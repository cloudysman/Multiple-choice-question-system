function joinQuiz() {
    var studentCode = document.getElementById('studentCode').value;
    var joinCode = document.getElementById('joinCode').value;
    if (studentCode && joinCode) {
        // AJAX request gửi đến server
        fetch('/verify-codes/', {  // Địa chỉ API server cần sửa cho phù hợp
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Đảm bảo bạn đã lấy token CSRF
            },
            body: JSON.stringify({student_code: studentCode, join_code: joinCode})
        })
        .then(response => response.json())
        .then(data => {
            if (data.valid) {
                alert('Tham gia thành công!');
                window.location.href = '/next-page/';
            } else {
                alert('Mã sinh viên hoặc mã tham gia không đúng');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert('Vui lòng nhập đầy đủ mã sinh viên và mã tham gia');
    }
}

// Hàm lấy cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
