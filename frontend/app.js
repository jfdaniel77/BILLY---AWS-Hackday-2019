const IDTokenSessionKey = 'AA_BillyWebIDToken';
const AWSCognitoUserPool = {
    UserPoolId: 'us-east-1_cXIjmWeI4',
    ClientId: '5siaa3ns06grv3jhfnnncq4t7j'
};
const AWSCognitoProvider = 'cognito-idp.us-east-1.amazonaws.com/'.concat(AWSCognitoUserPool.UserPoolId);
const AWSCognitoIdentityPoolID = 'us-east-1:1491e474-f9b3-4d19-821b-b6d93466a085';
const AWSCognitoLoginURL = 'https://embryo-billy.auth.us-east-1.amazoncognito.com/login?response_type=token&client_id=' + AWSCognitoUserPool.ClientId + '&redirect_uri=https://dnx78czn5g853.cloudfront.net';

AWS.config.region = 'us-east-1';

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

    let credentials = new AWS.CognitoIdentityCredentials({
        IdentityPoolId: AWSCognitoIdentityPoolID,
        Logins: login
    });

    credentials.get((error) => {
        if (error) {
            sessionStorage.removeItem(IDTokenSessionKey);
            window.location.replace(AWSCognitoLoginURL);
        }
    });
});

const backendURLPath = 'https://z1iphroe61.execute-api.us-east-1.amazonaws.com/prod';
const resizeWidth = 512;
const resizeHeight = 384;
const mockLocationKeys = ['ART', 'SCIENCE', 'PS', 'ION'];
const validObjects = ['Bottle', 'Jar', 'Foil', 'Cup', 'Can', 'Cardboard']
const validLabels = ['Paper', 'Glass', 'Plastic', 'Tin', 'Aluminium']
let queryID = '';
let wasteLabels = null;
let mockWasteData = {
    "ART": {
        "count": 0
    },
    "SCIENCE": {
        "count": 0
    },
    "PS": {
        "count": 0
    },
    "ION": {
        "count": 0
    }
};

$(document).ready(function () {
    $('#cameraBtn').click(function () {
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
    calculateWasteStats();
});


function calculateWasteStats() {
    for (i = 0; i < mockLocationKeys.length; i++) {
        $('#' + mockLocationKeys[i] + "WasteCount").text(mockWasteData[mockLocationKeys[i]].count);
    }
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

function analyzeImage(data) {
    $('#results').text('Analyzing...');
    queryID = data;
    queryResult();
}

function queryResult() {
    $.ajax({
        url: backendURLPath.concat('/query?requestID=').concat(queryID),
        headers: {"Authorization": sessionStorage.getItem(IDTokenSessionKey)},
        type: 'GET',
        success: function (result) {
            const resultObj = JSON.parse(result);
            queryID = '';
            if (resultObj['Success']) {
                $('#results').text('');
                wasteLabels = JSON.parse(JSON.parse(resultObj['data']).replace(/\'/g, '"'))['Labels'];
                filterWasteLabels();
                highlightLocation();
            } else {
                $('#results').text('ERROR: '.concat(resultObj['Error']));
            }
        },
        error: function () {
            queryResult();
        }
    });
}

function filterWasteLabels(){
    let filteredObjects = [];
    let filteredLabels = [];
    wasteLabels.forEach(function(label) {
        const validObject = validObjects.find(function(validData) {
            return validData == label.Name;
        });
        if (typeof validObject !== "undefined")
            filteredObjects.push(validObject);

        const validLabel = validLabels.find(function(validData) {
            return validData == label.Name;
        });
        if (typeof validLabel !== "undefined")
            filteredLabels.push(validLabel);
    });

    wasteLabels = [];

    if (filteredLabels.length == 0 && filteredObjects.length == 0) wasteLabels.push('General Waste');
    else wasteLabels = filteredLabels.concat(filteredObjects);
}

function highlightLocation() {
    const randomIdx = Math.floor(Math.random() * 4);
    const locationKey = mockLocationKeys[randomIdx];

    $('#' + locationKey + "Title").addClass("title-highlight");
    $('#' + locationKey + "Body").addClass("body-highlight");

    $('#' + locationKey + "Waste").empty();
    $('#' + locationKey + "Waste").append("<li style='text-decoration: underline;'>Waste Type:</li>");

    wasteLabels.forEach(function(label) {
        $('#' + locationKey + "Waste").append("<li>" + label + "</li>");
    });

    $('html, body').animate({
        scrollTop: $('#' + locationKey + "Title").offset().top
    }, 1000);
}

function binned(locationKey) {
    mockWasteData[locationKey].count++;

    calculateWasteStats();

    $('#' + locationKey + "Title").removeClass("title-highlight");
    $('#' + locationKey + "Body").removeClass("body-highlight");
    $('#' + locationKey + "Waste").empty();
}

function scrollToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}