const IDTokenSessionKey = 'AA_BillyWebIDToken';
const AWSCognitoUserPool = {
    UserPoolId: 'us-east-1_cXIjmWeI4',
    ClientId: '5siaa3ns06grv3jhfnnncq4t7j'
};
const AWSCognitoProvider = 'cognito-idp.us-east-1.amazonaws.com/'.concat(AWSCognitoUserPool.UserPoolId);
const AWSCognitoIdentityPoolID = 'us-east-1:1491e474-f9b3-4d19-821b-b6d93466a085';
const AWSCognitoLoginURL = 'https://embryo-billy.auth.us-east-1.amazoncognito.com/login?response_type=token&client_id=' + AWSCognitoUserPool.ClientId + '&redirect_uri=https://dnx78czn5g853.cloudfront.net';

let AWSCredentials = null;

AWS.config.region = 'us-east-1';

const backendURLPath = 'https://z1iphroe61.execute-api.us-east-1.amazonaws.com/prod';
const resizeWidth = 512;
const resizeHeight = 384;
const labels = ['Metal', 'Paper', 'Glass', 'Cardboard', 'Trash', 'Plastic'];
let queryID = '';

$(document).ready(function () {
    const url = window.location.href;
    if (url.indexOf('#id_token=') < 0 && !sessionStorage.getItem(IDTokenSessionKey))
        window.location.replace(AWSCognitoLoginURL);

    if (!sessionStorage.getItem(IDTokenSessionKey)) {
        const startIdx = url.indexOf('#id_token=') + '#id_token='.length;
        const tokenInfo = url.substring(startIdx, url.length).split('&');
        sessionStorage.setItem(IDTokenSessionKey, tokenInfo[0]);
    }

    let provider = AWSCognitoProvider;
    let login = {};
    login[provider] = sessionStorage.getItem(IDTokenSessionKey);

    AWSCredentials = new AWS.CognitoIdentityCredentials({
        IdentityPoolId: AWSCognitoIdentityPoolID,
        Logins: login
    });

    AWSCredentials.get((error) => {
        if (error) {
            sessionStorage.removeItem(IDTokenSessionKey);
            window.location.replace(AWSCognitoLoginURL);
        } else {
            configureUIActions();
        }
    });
});

function configureUIActions(){
    $('#cameraBtn').click(function () {
        reset();
        $('#photo').click();
    });

    $('#photo').change(function () {
        if (photo.files[0]) {
            resize(photo.files[0]);
        }
    });

    window.onscroll = function () {
        scrollFunction()
    };
}

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        $("#topBtn").show();
    } else {
        $("#topBtn").hide();
    }
}

function resize(file) {
    const fileName = file.name;
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = event => {
        const img = new Image();
        img.src = event.target.result;
        img.onload = () => {
            const elem = document.createElement('canvas');
            elem.width = resizeWidth;
            elem.height = resizeHeight;
            const ctx = elem.getContext('2d');
            // img.width and img.height will contain the original dimensions
            ctx.drawImage(img, 0, 0, resizeWidth, resizeHeight);
            ctx.canvas.toBlob((blob) => {
                const resizedFile = new File([blob], fileName, {
                    type: 'image/jpeg',
                    lastModified: Date.now()
                });

                upload(resizedFile);

            }, 'image/jpeg', 1);
        },
            reader.onerror = error => $('#results').text('ERROR: '.concat(error));
    };
}

function upload(file) {
    AWSCredentials.get((error) => {
        if (error) {
            sessionStorage.removeItem(IDTokenSessionKey);
            window.location.replace(AWSCognitoLoginURL);
        } else {
            if (file) {
                $('#results').text('Uploading...');

                var fileData = new FormData();
                fileData.append('image', file);

                $.ajax({
                    url: backendURLPath.concat('/submit'),
                    headers: {"Authorization": sessionStorage.getItem(IDTokenSessionKey)},
                    type: 'POST',
                    data: fileData,
                    cache: false,
                    contentType: false,
                    processData: false,
                    dataType: 'text',
                    success: function (data) {
                        analyzeImage(data);
                    },
                    error: function () {
                        $('#results').text('ERROR: Failed to upload image!');
                    }
                });
            } else {
                $('#results').text('WARN: Nothing to upload.');
            }
        }
    });
}

function analyzeImage(data) {
    $('#results').text('Analyzing...');
    queryID = data;
    queryResult();
}

function queryResult() {
    if (queryID == ''){
        $('#results').text('ERROR: Missing query ID!');
        return;
    }

    AWSCredentials.get((error) => {
        if (error) {
            sessionStorage.removeItem(IDTokenSessionKey);
            window.location.replace(AWSCognitoLoginURL);
        } else {
            $.ajax({
                url: backendURLPath.concat('/query?requestID=').concat(queryID),
                headers: {"Authorization": sessionStorage.getItem(IDTokenSessionKey)},
                type: 'GET',
                success: function (result) {
                    const resultObj = JSON.parse(result);
                    queryID = '';
                    if (resultObj['Success']) {
                        $('#results').text('');
                        const predictions = JSON.parse(JSON.parse(resultObj['data']))['predictions'];
                        if (predictions && predictions.length > 0) {
                            $('#' + labels[predictions[0]['predicted_label'] - 1]).show();
                            highlightLocation(labels[predictions[0]['predicted_label'] - 1]);
                        } else $('#results').text('ERROR: Unidentified waste type!');
                    } else {
                        $('#results').text('ERROR: '.concat(resultObj['Error']));
                    }
                },
                error: function () {
                    queryResult();
                }
            });
        }
    });
}

function highlightLocation(id) {
    $('html, body').animate({
        scrollTop: $('#' + id).offset().top
    }, 1000);
}

function binned(){
    reset();
    scrollToTop();
}

function reset(){
    $('.waste-type').each(function(){
        $(this).hide();
    });
}

function scrollToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}