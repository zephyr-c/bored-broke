$('#username').on('change', (evt) => {
    $.get('current_users', $('#username').val(), (res) =>
        if(res === True)){
        alert("Someone is already using that name!")
    };
});

$('#user-registration').on('submit', (evt) => {
    evt.preventDefault();

    const formData = {
    username: $("#username").val()
    password: $("#password").val() name="password" required><br>
    email: $("#email").val()
    fname: $("#fname").val()
    lname: $("#lname").val()
    location: $("#location").val()
    phone: $("#phone").val()
    };

    $.post('/register', formData, (res) =>
})


$.post('/save-event', evt.target.attr('name'), (res) =>