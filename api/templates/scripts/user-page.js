
$(document).ready(() => {
    let userObject;
    let aiTopicText;
    let $messageInputs;
    let hasMessages = 0;
    let temp = `<div class="message-body">
                    Lorem ipsum, dolor sit amet consectetur adipisicing elit. Impedit, quibusdam.
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Sed, consequuntur suscipit. Quae delectus soluta suscipit asperiores sit hic natus impedit.
                </div>

                <div class="message-recipients">12334, 22334</div>

                <div class="message-btn">
                        <button>Delete</button>
                </div>`;

    function updateMessages (message, recipients, messageId) {

        if (hasMessages == 1) {
            $('.message-article').text('');
        }

        console.log('DATA MESSAGE ID\n', messageId);

        $('.message-article').append("<div class='remove-div'>" +
                "<div class='message-body'>" + message + "</div>"
                + "<div class='message-recipients'>" + recipients + " </div>"
                + "<div class='message-btn'>" + "<button data-messageId=\"" + messageId + "\">Delete</button></div>"
                + "</div>");
    }   
    

    $('.back-home').click(() => {
        location.reload();
    });


    $.ajax({
        url: 'http://127.0.0.1:5000/api/users/' + $('.user-id h3').text(),
        type: 'GET',
        success: (data) => {
            userObject = data['object'];
        },
        error: (xhr, status, error) => {
            console.log(error, status);
        }
    });


    $('.user button').click(() => {
        $('.create-message').css('display', 'flex');
    });


    $('#btn-cancel').click(() => {
        $('.create-message').css('display', 'none');
        $('.user-messages textarea').val('');
    });


    $('.ai-topic button').click(() => {
        aiTopicText = $('.ai-topic input[type="text"]').val();

        $('.ai-topic input[type="text"]').val('');

        
        if (String(aiTopicText).length > 0) {
            $.ajax({
                url: 'http://127.0.0.1:5000/api/message/generation',
                type: 'POST',
                data: JSON.stringify({'topic': aiTopicText}),
                contentType: 'application/json',
                timeout: 60000,
                beforeSend: () => {
                    $('#loader').show();
                },
                success: (data) => {
                    $('.ai-message').remove();
        
                    data.forEach(element => {
                        $('.ai-messages').append('<div class="ai-message">' + String(element) + '</div>');
                    });

                    $('.copy-notice').show();
                },
                error: (xhr, status, error) => {
                    alert('ERROR GENERATING MESSAGE TRY AGAIN');
                    console.log(status, error);
                },
                complete: () => {
                    $('#loader').hide();
                }
            });        
        }
    });

   
    $('.ai-messages').on('click', '.ai-message', function () {
        let clickedDiv = $(this);
    
        let text = clickedDiv.text();

        try {
            navigator.clipboard.writeText(text);
            clickedDiv.css('color', 'blueviolet');

            setInterval(() => {
                clickedDiv.css('color', '');
            }, 1000); 
        } catch (err) {
              console.error('Failed to copy: ', err);
        }
    });

    $('#btn-send').click(() => {
        const messageInputDict = {};

        $messageInputs = $('.user-messages textarea');

        $messageInputs.each((index, element) => {
            if ($(element).val().length > 0) {
                messageInputDict[element.name] = $(element).val();
            } else {
                alert('No Input entered');
                return;
            }
        });
        messageInputDict['user_id'] = userObject.user_id;

        console.log(messageInputDict);

                $.ajax({
                    url: 'http://127.0.0.1:5000/api/verify/number',
                    type: 'POST',
                    contentType: 'application/json', 
                    data: JSON.stringify({'recipients': messageInputDict['recipients']}),
                    timeout: 60000,
                    success: (data) => {
                        console.log(data);

                        if (data['False'].length > 0) {
                            alert('Number(s) entered is/are not VALID!');
                        }
                        else {
                            messageInputDict['recipients'] = data['True'];
                            console.log(messageInputDict);
                            $.ajax({
                                url: 'http://127.0.0.1:5000/api/message/send',
                                type: 'POST',
                                contentType: 'application/json',
                                data: JSON.stringify(messageInputDict),
                                timeout: 60000,
                                success: (data) => {
                                    alert('MESSAGE SENT SUCCESSFULLY... :)');
                                    console.log(data);

                                    $.ajax({
                                        url: 'http://127.0.0.1:5000/api/messages/create',
                                        type: 'POST',
                                        contentType: 'application/json',
                                        data: JSON.stringify(messageInputDict),
                                        success: (data) => {
                                            console.log(data);

                                            updateMessages(messageInputDict['message'], messageInputDict['recipients'], data['object']['id'])
                                        },
                                        error: (xhr, error) => {
                                            console.log(error);
                                        }
                                    });
                                },
                                error: (xhr, status, error) => {
                                    console.log(status, error);
                                }
                            });
                       } 
                    },
                    error: (xhr, status, error) => {
                        alert('Error Sending message');
                        console.log(status, error);
                    }
                });
        
    });

    $('.message-article').on('click', '.message-btn button', function () {
        let messageId = $(this).data('messageid');
        let parentDiv = $(this).parent().parent();
        
        $.ajax({
            url: 'http://127.0.0.1:5000/api/messages/delete/' + messageId,
            type: 'POST',
            contentType: 'application/json',
            success: (data) => {
                console.log(data);
                $(parentDiv).remove();
                alert('DELETE SUCCESSFUL...');
            },
            error: (xhr, error) => {
                console.log(error);
            }
        });

        if ($('.message-article').is(':empty')) {
            console.log('I AM EMPTY');
            hasMessages = 0;
            $('.message-article').text('NO MESSAGES').css('text-align', 'center');
        }
    });

    

    setTimeout(() => {
        $.ajax({
            url: 'http://127.0.0.1:5000/api/users/' + userObject['user_id'] + '/messages',
            type: 'GET',
            success: (data) => {
                console.log('MESSAGES\n', data);

                if (data.length > 0) {
                    let i;
                    
                    for (i = 0; i < data.length; i++) {
                        let messageId = data[i]['id'];

                        console.log(data[i]);
                        let messageBody = data[i]['body'];

                        $.ajax({
                            url: 'http://127.0.0.1:5000/api/messages/' + messageId + '/recipients',
                            type: 'GET',
                            success: (data) => {
                                updateMessages(messageBody, data, messageId);
                            },
                            error: (xhr, error) => {
                                console.log(error);
                            }
                        });
                    }
                } else {
                    console.log(userObject);
                    hasMessages = 1;
                    $('.message-article').text('NO MESSAGES').css('text-align', 'center');
                }
            },
            error: (xhr, error) => {
                console.log(error);
            }
        });
    }, 2000);


});