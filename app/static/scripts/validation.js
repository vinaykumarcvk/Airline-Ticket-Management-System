$(document).ready(function () {

  jQuery.validator.addMethod("greaterThan",
    function (value, element, params) {
      if (!/Invalid|NaN/.test(new Date(value))) {
        return new Date(value) > new Date($(params).val());
      }
      return isNaN(value) && isNaN($(params).val())
        || (Number(value) > Number($(params).val()));
    }, 'Must be greater than {0}.');

  jQuery.validator.addMethod("lettersonly", function (value, element) {
    return this.optional(element) || /^[a-z\s]+$/i.test(value);
  }, "Only alphabetical characters");

  $("#loginForm").validate()

  $("#regForm").validate({
    rules: {
      first_name: { lettersonly: true },
      last_name: { lettersonly: true },
      email:{
        email:true,
        remote:{
          url:"is-email-exist",
          type:"get"
        }
      },
      password: {
        minlength: 3
      },
      confirm_password: {
        minlength: 3,
        equalTo: "#password"
      }
    },
    messages: {
      email: {
        remote: "Email address already registered"
      },
      confirm_password: {
        equalTo: "Password and confirm password doesn't match"
      }
    }
  });

  
  $("#airplaneForm").validate({
    rules: {
      airplane_capacity: { number: true }
    }
  });

  $("#flightForm").validate({
    rules: {
      arrival_time:{greaterThan:"#departure_time"},
      available_seats: { number: true },
      fare: { number: true }
    },
    messages:{
      arrival_time:"Arrival time should be greater than Departure Time"
    }
  })

})