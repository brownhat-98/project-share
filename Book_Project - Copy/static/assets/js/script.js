function showAlert() {
    var username = document.getElementById('username').value;
    var first_name = document.getElementById('first_name').value;
    var last_name = document.getElementById('last_name').value;
    var email = document.getElementById('email').value;
    var password1 = document.getElementById('password1').value;
    var password2 = document.getElementById('password2').value;

    if (!username || !first_name || !last_name || !email || !password1 || !password2) {
        alert('please fill out the required fields');
    } else {
        alert('Registration Successful');
    }
}

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

const csrftoken = getCookie('csrftoken');

$(document).ready(function() {
    $(document).on('click', '.add-to-cart', function(event) {
        event.preventDefault();
        var productId = $(this).data('product-id');
        var button = $(this);

        $.ajax({
            type: 'POST',
            url: "{% url 'userapp:cart_add' %}",
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                product_id: productId,
                action: 'post'
            },
            success: function(response) {
                if (response.success) {
                    button.removeClass('btn-outline-primary').addClass('btn-success').text('Added to cart');
                    console.log(response.message);
                } else {
                    console.error(response.message);
                }
            },
            error: function(xhr, errmsg, err) {
                console.error(errmsg);
            }
        });
    });
});
