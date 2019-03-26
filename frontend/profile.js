$(document).ready(function () {
    const tokenPayload = JSON.parse(atob(sessionStorage.getItem(IDTokenSessionKey).split(".")[1]));

    const email = tokenPayload['email'];
    const givenName = tokenPayload['given_name'];
    const familyName = tokenPayload['family_name'];

    $('#fullName').text(givenName + ' ' + familyName);
    $('#emailAddress').text(email);

    animateBadge();
});

function animateBadge(){
    $("#badgeImg").fadeIn("slow", function() {
        setTimeout(function(){
            $('#badgeImg').fadeOut("slow", function(){
                $("#badgeImg").fadeIn("slow", function(){
                    $("#badgeImg").fadeIn("slow", function() {
                        setTimeout(function(){
                            $('#badgeImg').fadeOut("slow", function(){
                                $("#badgeImg").fadeIn("slow");
                                animateCollectedPoints();
                            });
                        }, 1500);
                    });
                });
            });
        }, 1500);
    });
}

function animateCollectedPoints(){
    $("#collectedPoints").fadeIn("slow", function() {
        setTimeout(function(){
            $('#collectedPoints').fadeOut("slow", function(){
                $("#collectedPoints").fadeIn("slow", function(){
                    $("#collectedPoints").fadeIn("slow", function() {
                        setTimeout(function(){
                            $('#collectedPoints').fadeOut("slow", function(){
                                $("#collectedPoints").fadeIn("slow");
                            });
                        }, 1500);
                    });
                });
            });
        }, 1500);
    });
}