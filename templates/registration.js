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