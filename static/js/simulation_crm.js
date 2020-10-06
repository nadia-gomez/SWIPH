
try {
    /*console.log('0')
    console.log('pag -'+document.getElementById("sectorSelector"))
    var sectorSelector=document.getElementById("sectorSelector"); */
    /* console.log('form-'+countryForm) */

    var activeSectors=["Dummy","Food_beverages","Agro_Livestock","Paper","Chemical","Textile","Minning","Wood_Cork","Laundries","Sewage_treatment"];
    /* console.log('1') */
    for (x in activeSectors) {
        /* console.log('for') */
        $('.'+activeSectors[x]).hide();
    }
    /* console.log('country -'+sectorSelector.value) */
    var sector = sectorSelector.value;
    if (sector==null){
        console.log('if1')
        $('.'+sectorForm).show();
        $('.unknown').show(); 
    }
    else{
        /* console.log('else1') */
        if (activeSectors.includes(sector)){
            /* console.log('if2') */
            $('.'+sector).show();
        }
        else{
            /* console.log('else2') */
            $('.unknown').show();
        } 
    }

  }
  catch(error) {
   
  }
  
function showSectors(selectObject) {
    
    var activeSectors=["Dummy","Food_beverages","Agro_Livestock","Paper","Chemical","Textile","Minning","Wood_Cork","Laundries","Sewage_treatment"];
    for (x in activeSectors) {
        $('.'+activeSectors[x]).hide();
    }
    var country = selectObject.value;
    if (activeSectors.includes(country)){
    $('.'+country).show();
    }else{
        $('.unknown').show();   
    }
   
}

function deleteProjectEntry(entry) {
    var $entry = $(entry)
    $entry.parent().remove()
    var id = $entry.data('id')

    $.ajax({
        url: 'delete/' + id,
        method: 'DELETE',
        /*    data:{
                'csrfmiddlewaretoken':csrf_token
            },*/
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        },
    })
}

function show_auxData(entry) {
    $('.auxData').show();
    $('.auxIndus').hide();
   
}
function hide_auxData(entry) {
    $('.auxData').hide(); 
}

function show_auxIndus(entry) {
    $('.auxData').hide();
    $('.auxIndus').show();
   
}
function hide_auxIndus(entry) {
    $('.auxIndus').hide(); 
}

function check_auxData (entry){
    var $self       = $(entry);

    if ($self.is(":checked")) {
      $('.auxData').show();
    } else {
      $('.auxData').hide();
    }
  
  }

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems, options);
  });

  // Or with jQuery

  $(document).ready(function(){
    $('.collapsible').collapsible();
    $(".dropdown-trigger").dropdown();
  });

  try {
    /*console.log('0')
    console.log('pag -'+document.getElementById("sectorSelector"))
    var sectorSelector=document.getElementById("sectorSelector"); */
    /* console.log('form-'+countryForm) */

    var activeStages=["Lead","Visit","Offer","Exit","Follow"];
    /* console.log('1') */
    for (x in activeStages) {
        /* console.log('for') */
        $('.'+activeStages[x]).hide();
    }
    /* console.log('country -'+sectorSelector.value) */
    var stage = stageSelector.value;
    if (stage==null){
        $('.'+stageForm).show();
        $('.Lead').show(); 
    }
    else{
        /* console.log('else1') */
        if (activeStages.includes(stage)){
            /* console.log('if2') */
            $('.'+stage).show();
        }
        else{
            /* console.log('else2') */
            $('.Lead').show();
        } 
    }

  }
  catch(error) {
   
  }
  
function showStages(selectObject) {
    
    var activeStages=["Lead","Visit","Offer","Exit","Follow"];
    for (x in activeStages) {
        $('.'+activeStages[x]).hide();
    }
    var country = selectObject.value;
    if (activeStages.includes(country)){
    $('.'+country).show();
    }else{
        $('.Lead').show();   
    }
   
}