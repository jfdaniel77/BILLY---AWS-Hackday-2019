$(document).ready(function () {
    const tokenPayload = JSON.parse(atob(sessionStorage.getItem(IDTokenSessionKey).split(".")[1]));

    const email = tokenPayload['email'];
    const givenName = tokenPayload['given_name'];
    const familyName = tokenPayload['family_name'];

    $('#fullName').text(givenName + ' ' + familyName);
    $('#emailAddress').text(email);
});