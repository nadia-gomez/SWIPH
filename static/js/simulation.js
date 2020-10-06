function deleteSimulationEntry(entry) {
    var $entry = $(entry)
    $entry.parent().remove()
    var id = $entry.data('id')

    $.ajax({
        url: 'entry/delete/' + id,
        method: 'DELETE',
        /*    data:{
                'csrfmiddlewaretoken':csrf_token
            },*/
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        },
    })
}



function simulationGIF(entry) {
    $('.ajaxProgress').show();
    $('.hideForm').hide();

}

function bizGIF(entry) {
    $('.ajaxProgress').show();
    $('.hideForm').hide();
    window.location="spain"

}

function simulationGIF2(entry) {
    $('.ajaxProgress2').show();
    $('.hideForm').hide();
}

function simulationGIF3(entry) {
    $('.ajaxProgress3').show();
    $('.hideForm').hide();
}

$(window).scroll(function () {
    var scrollTop = $(window).scrollTop();
    var opacity = -130 + (scrollTop) / 2
    if (opacity <= 0) {
        opacity = 0
    }
    $('#headerFade').css({
        'opacity': opacity / 100
    });
});
$('.unknown').hide()
try {
    console.log('0')
    console.log('pag -' + document.getElementById("countrySelector"))
    var countrySelector = document.getElementById("countrySelector");
    console.log('form-' + countryForm)
    var activeCountries = ["KE","RO","GH","MR","DE","CV","AR","BD","US","UY","AU","EG","BR","CY","GR","EC","JO","LB","PS","TN","IN", "CH", "NI", "SV", "ES", "ZA", "MA", "IT", "CL", "VE", "MX", "CR", "PA", "CO", "FR", "PT","SA", "unknown"];
    /* console.log('1') */
    for (x in activeCountries) {
        /* console.log('for') */
        $('.' + activeCountries[x]).hide();
    }
    /*  console.log('country -'+countrySelector.value) */
    var country = countrySelector.value;
    if (country == null) {
        /* console.log('if1') */
        $('.' + countryForm).show();
        $('.unknown').hide();
    }
    else {
        /* console.log('else1') */
        if (activeCountries.includes(country)) {
            /*  console.log('if2') */
            $('.' + country).show();
        }
        else {
            /* console.log('else2') */
            $('.unknown').show();
        }
    }

}
catch (error) {

}





function showLocations(selectObject) {

    var activeCountries = ["KE","RO","GH","MR","DE","CV","AR","BD","US","UY","AU","EG","BR","CY","GR","EC","JO","LB","PS","TN","IN", "CH", "NI", "SV", "ES", "ZA", "MA", "IT", "CL", "VE", "MX", "CR", "PA", "CO", "FR", "PT","SA", "unknown"];
    for (x in activeCountries) {
        $('.' + activeCountries[x]).hide();
    }
    var country = selectObject.value;
    if (activeCountries.includes(country)) {
        $('.' + country).show();
    } else {
        $('.unknown').show();
    }

}


$('.count').each(function () {
    $(this).prop('Counter', 0).animate({
        Counter: $(this).text()
    }, {
            duration: 4000,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now));
            }
        });
});


$(document).ready(function () {
    $('.sidenav').sidenav();
});
