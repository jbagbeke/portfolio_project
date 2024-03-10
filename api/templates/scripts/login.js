
$(document).ready(() => {
    $('.back-home').click(() => {
        location.reload();
    });


    $('.login-form').submit((event) => {
        let $loginInputs;
        let formDict = {};

        event.preventDefault();

        $loginInputs = $(".login-form input[type='text']");
        $loginInputs.each((index, inputElement) => {
            formDict[inputElement.name] = $(inputElement).val();
        });

        if (isNaN(formDict['user_id'])) {
            $(".login-info").addClass('login-input-id');
            
            setTimeout(function () {
                $(".login-info").removeClass('login-input-id');
            }, 2000)

        } else {
            $(".login-form input[type='text']").val('');

            $.ajax({
                url: 'http://127.0.0.1:5000/api/users/login',
                type: 'POST',
                data: JSON.stringify(formDict),
                contentType: 'application/json',
                success: (data) => {
                    $('body').html(data);
                },
                error: (xhr, status, error) => {
                    alert('NO USER ID FOUND. CHECK AND TRY AGAIN!')
                    console.log(status, error);
                }
            });
        }

    });
});