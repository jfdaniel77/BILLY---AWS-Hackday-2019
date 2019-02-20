const backendURLPath = 'http://18.204.42.219:8080';
const resizeWidth = 640;
const resizeHeight = 480;
const mockLocationKeys = ['ART', 'SCIENCE', 'PS', 'ION'];
var queryID = '';
var wasteLabels = null;
var mockWasteData = {
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

$( document ).ready(function() {
    $('#cameraBtn').click(function () {
		$('#photo').click();
	});

	$('#photo').change(function () {
		if (photo.files[0]){
			resize(photo.files[0]);
		}
	});

	window.onscroll = function() {scrollFunction()};
	calculateWasteStats();
});


function calculateWasteStats(){
	for (i = 0; i < mockLocationKeys.length; i++) {
        $('#'+mockLocationKeys[i]+"WasteCount").text(mockWasteData[mockLocationKeys[i]].count);
	}
}

function round(value, precision) {
    var multiplier = Math.pow(10, precision || 0);
    return Math.round(value * multiplier) / multiplier;
}

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
		$("#topBtn").show();
	} else {
		$("#topBtn").hide();
	}
}

function resize(file){
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
        fileData.append('image',file);
		
		$.ajax({
			url: backendURLPath.concat('/submit'),
			type: 'POST',
			data: fileData,
			cache: false,
			contentType: false,
			processData: false,
            dataType: 'text',
            success: function(data) {
                analyzeImage(data);
            },
            error: function() {
			    $('#results').text('ERROR: Failed to upload image!');
            }
		});
	} else {
		$('#results').text('WARN: Nothing to upload.');
	}
}

function analyzeImage(data){
	$('#results').text('Analyzing...');
	queryID = data;
	queryResult();
}

function queryResult(){
	$.ajax({
		url: backendURLPath.concat('/query?requestID=').concat(queryID),
		type: 'GET',
        success: function(result) {
            const resultObj = JSON.parse(result);
            queryID = '';
            if (resultObj['Success']){
                $('#results').text('');
                wasteLabels = JSON.parse(JSON.parse(resultObj['data']).replace(/\'/g, '"'))['Labels'];
                highlightLocation();
            } else {
                $('#results').text('ERROR: '.concat(resultObj['Error']));
            }
        },
        error: function() {
            queryResult();
        }
	});
}

function highlightLocation(){
	randomIdx = Math.floor(Math.random() * 4);
	locationKey = mockLocationKeys[randomIdx];
	
	$('#'+locationKey+"Title").addClass("title-highlight");
	$('#'+locationKey+"Body").addClass("body-highlight");

    $('#'+locationKey+"Waste").empty();
    $('#'+locationKey+"Waste").append( "<li style='text-decoration: underline;'>Waste Labels:</li>" );

    for (i=0; i<wasteLabels.length; i++){
        console.log(wasteLabels[i])
        $('#'+locationKey+"Waste").append( "<li>"+wasteLabels[i]['Name']+"</li>" );
    }

    $('html, body').animate({
        scrollTop: $('#'+locationKey+"Title").offset().top
    }, 1000);
}

function binned(locationKey) {
	mockWasteData[locationKey].count++;

    calculateWasteStats();
	
	$('#'+locationKey+"Title").removeClass("title-highlight");
	$('#'+locationKey+"Body").removeClass("body-highlight");
    $('#'+locationKey+"Waste").empty();
}

function scrollToTop() {
	document.body.scrollTop = 0; // For Safari
	document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}