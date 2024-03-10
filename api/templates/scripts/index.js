
$(document).ready( () => {
    const bodyContent = $('body').html();
    const aboutPages = [`\
            <p>Both Frontend and Backend was done</p>\
            <p>by me although I find my strength in the backend,</p>\
            <p>I wanted to try out the Frontend work it out.</p>\
            <p>It was frustrating at first but now I</p>\
            <p>can say I have a good foundation.</p>\
            <p class="wide-screen">And that is all thanks to</p>\
            <p class="wide-screen">Frontend Masters with their awesome</p>\
            <p class="wide-screen">teaching, I can do some Frontend stuff.</p>`,
            `\
            <p>This website is a mini website to send</p>\
            <p>sms mainly to Ghanaians, due to time</p>\
            <p>constraints and as a result was not able</p>\
            <p>to configure a custom SMPP. More features</p>\
            <p>will be implemented alongside the OpenAI API already integrated.</p>\
            <p class="wide-screen">We'll do more to</p>\
            <p class="wide-screen">enhance the productivity of users on the website.</p>\
            <p class="wide-screen">Definately more improvement ahead.</p>`];
    let aboutPageCount = 0;
    let aboutOriginalContent = $('.about-paragraph').html();
    let aboutPrevContent;


    $('.about-prev').css('opacity', '40%');

    $('.one-go-btn, .sign-up, .sign-up-nav').click( () => {
        $.ajax({
            url: 'http://127.0.0.1:5000/api/sign_up',
            type: 'GET',
            success: (data) => {
                $('body').html(data);
            },
            error: (xhr, status, error) => {
                console.log(error, status);
            }
        });
    });

    $('.login-nav').click(() => {
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
    });

    $('.back-home').click(() => {
        $('body').html(bodyContent);
    });

    $('.one-info-btn').click( () => {
        $('html, body').animate({
            scrollTop: $('.section-five-header').offset().top
        }, 1000);
    });

    $('.about-next').click(() => {

            if (aboutPageCount < 2) {
                aboutPrevContent = $('.about-paragraph').html();
                $('.about-paragraph').html(aboutPages[aboutPageCount]);
                aboutPageCount = aboutPageCount + 1;
            }

            if (aboutPageCount > 1) {
                $('.about-next').css('opacity', '40%');
            } else {
                 $('.about-prev').css('opacity', '100%');
            }
    });

        

    $('.about-prev').click(() => {
        if (aboutPageCount > 1) {
            aboutPageCount = aboutPageCount - 1;
            $('.about-paragraph').html(aboutPrevContent);
        } else if (aboutPageCount === 1) {
            aboutPageCount = aboutPageCount - 1;
            $('.about-paragraph').html(aboutOriginalContent);
        }

        if (aboutPageCount === 0) {
            $('.about-prev').css('opacity', '40%');
        }
        else {
            $('.about-next').css('opacity', '100%');
        }
    });
    

});