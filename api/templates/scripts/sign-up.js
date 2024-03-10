$(document).ready(() => {
    $('.back-home').click(() => {
        location.reload();
    });


    $('.sign-up-form').submit((event) => {
        let $loginInputs;
        let formDict = {};

        event.preventDefault();

        $loginInputs = $(".sign-up-form input[type='text']");
        
        $loginInputs.each((index, inputElement) => {
            formDict[inputElement.name] = $(inputElement).val();
        });

        if (isNaN(formDict['number'])) {
            $(".number").addClass('login-input-id');
            
            setTimeout(function () {
                $(".number").removeClass('login-input-id');
            }, 2000)
        } else {
            $.ajax({
                url: 'http://127.0.0.1:5000/api/users/create',
                type: 'POST',
                data: JSON.stringify(formDict),
                contentType: 'application/json',
                success: (data) => {
                    userObject = data.object;

                    $('.sign-up-form').html('Your Unique ID is:\
                                            ' + '<h2>' + userObject.user_id + '</h2>\
                                            Please copy this ID and keep it SAFE.\
                                            This ID would be used to login.\
                                            <h3>Press ENTER to continue</h3>');
                    
                    $(document).keydown((event) => {
                        if (event.key === 'Enter') {
                            $.ajax({
                                url: 'http://127.0.0.1:5000/api/login',
                                type: 'GET',
                                success: (data) => {
                                    $('body').html(data);
                                },
                                error: (xhr, status, error) => {
                                    console.log(error, status);
                                }
                            });
                        }
                    });

                }, 
                error: (xhr, status, error) => {
                    console.log(status, error);
                }
            });

            $(".sign-up-form input[type='text']").val('');
        }

    });
});