function keepData(){
    $(".username").val("Hiii");
}
function add_modal(){
    $('#addModal').modal('toggle'); 
}

function get_project(){
  var projects = document.getElementById('project').value;
  project = document.getElementById('project_value').value;
  if (projects.includes(project)){
    document.querySelector('button[title="Next"]').disabled = true;
    document.querySelector('button[title="Next"]').classList.add('no-drop');
  }
  else{
    document.querySelector('button[title="Next"]').disabled = false;
  }
}



var pos_tag_name = '';

$(document).ready(function(){
  document.getElementsByClassName('postag_name')[0].classList.add('btn-grad');
  pos_tag_name = document.getElementsByClassName('postag_name')[0].innerHTML;
});

function get_tag(btn){
  pos_tag_name = btn.innerHTML;
  list_tag = document.getElementsByClassName('postag_name');
  for(var i=0; i<list_tag.length; i++) {
    list_tag[i].classList.remove('btn-grad')
  }
  btn.classList.add('btn-grad');
}

function span(btn){
  if (btn.querySelector('i').classList.value == 'close-button d-none'){
    btn.classList.add('btn-outline-success');
    btn.querySelector('span').innerHTML = pos_tag_name;
    btn.querySelector('input[id="postag"]').value = pos_tag_name;
    btn.querySelector('i').classList.remove('d-none'); 
  }
  else{
    btn.querySelector('i').classList.add('d-none');
    btn.classList.remove('btn-outline-success');
    btn.querySelector('span').innerHTML = '';
    btn.querySelector('input[id="postag"]').value = '';
  }
}


function span_textclass(btn){
  if (btn.querySelector('i').classList.value == 'fa fa-check d-none'){
    btn.classList.add('active');
    text_tag_name =  btn.querySelector('input[id="tag"]').value
    btn.querySelector('input[id="texttag"]').value = text_tag_name;
    btn.querySelector('i').classList.remove('d-none'); 
  }
  else{
    btn.querySelector('i').classList.add('d-none');
    btn.classList.remove('active');
    btn.querySelector('input[id="texttag"]').value = '';
  }
}

var clicks = 0;
var count = 0;

var tag = ''
var start = ''
var end = ''

var data_parcing = []
var data;
function get_tag_par(btn){
  clicks += 1;
  btn.querySelector('input[id="partag"]').value = pos_tag_name;
  btn.querySelector('span').innerHTML = pos_tag_name + count;

  tag = btn.querySelector('span').innerHTML;
  start = btn.querySelector('input[id="partoken"]').value;
  
  if (clicks == 1){
    data = tag + " " + start ;
  }

  if (clicks == 2){
    btn.querySelector('span').innerHTML = pos_tag_name + count;
    end = btn.querySelector('input[id="partoken"]').value;
    count +=1;
    clicks = 0;
    data = data +  " " + end ;
    data_parcing.push(data)
    click();
  } 
}

function click(){
  for (i = 0; i <data_parcing.length; i++){
    alert(data_parcing[i])
  }
}





$(document).ready(function(){
     var multipleCancelButton = new Choices('#choices-multiple-remove-button', {
        removeItemButton: true,
        // maxItemCount:1,
        // searchResultLimit:1,
        // renderChoiceLimit:1
      }); 

      
 });

 $(document).ready(function() {
  $('#example').DataTable( {
      "pageLength": 5,
      dom: '<"top mt-2 mb-2"i>t<"container-center mb-0 "p>',
  } );
} );

function copyToClipboard() {
    var copyText = document.getElementById("link").value;
    navigator.clipboard.writeText(copyText).then(() => {
        document.getElementById("copy").innerHTML = "Copied!"; 
        document.getElementById("check").classList.remove('d-none');
        $('[data-toggle="tooltip"]').tooltip('toggle');
    });
  }

function mySubmitFunction(e) {
    e.preventDefault();
    return false;
}

function develop(){
    alert("Chức năng này đang phát triển!")
}
   var opacity = 0;
   var intervalID = 0;
   window.onload = fadeIn;
   
   function fadeIn() {
       setInterval(show, 50);
   }
   
   function show() {
       var body = document.getElementById("fade");
       opacity = Number(window.getComputedStyle(body)
                           .getPropertyValue("opacity"));
       if (opacity < 1) {
           opacity = opacity + 0.1;
           body.style.opacity = opacity
       } else {
           clearInterval(intervalID);
       }
   }
    
    $("#fade").fadeTo(3000, 500).slideUp(500, function(){
    $("#fade").slideUp(500);
});

    $(document).ready(function() {
        $("#fade").hide();
        $("#fade").fadeTo(3000, 500).slideUp(500, function() {
            $("#fade").slideUp(500);
        });
    });



(function ($) {
    "use strict";


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    

    

})(jQuery);



var current = location.pathname;
$('.navbar-nav .nav-link').each(function(){
    var $this = $(this);
    if ($this.attr('href') === current){
        $this.addClass('active');
    }
})




const DOMstrings = {
    stepsBtnClass: 'multisteps-form__progress-btn',
    stepsBtns: document.querySelectorAll('.multisteps-form__progress-btn'),
    stepsBar: document.querySelector('.multisteps-form__progress'),
    stepsForm: document.querySelector('.multisteps-form__form'),
    stepsFormTextareas: document.querySelectorAll('.multisteps-form__textarea'),
    stepFormPanelClass: 'multisteps-form__panel',
    stepFormPanels: document.querySelectorAll('.multisteps-form__panel'),
    stepPrevBtnClass: 'js-btn-prev',
    stepNextBtnClass: 'js-btn-next'
  };
  
  //remove class from a set of items
  const removeClasses = (elemSet, className) => {
    
    elemSet.forEach(elem => {
      
      elem.classList.remove(className);
      
    });
    
  };
  
  //return exect parent node of the element
  const findParent = (elem, parentClass) => {
    
    let currentNode = elem;
  
    while(! (currentNode.classList.contains(parentClass))) {
      currentNode = currentNode.parentNode;
    }
    
    return currentNode;
    
  };
  
  //get active button step number
  const getActiveStep = elem => {
    return Array.from(DOMstrings.stepsBtns).indexOf(elem);
  };
  
  //set all steps before clicked (and clicked too) to active
  const setActiveStep = (activeStepNum) => {
    
    //remove active state from all the state
    removeClasses(DOMstrings.stepsBtns, 'js-active');
    
    //set picked items to active
    DOMstrings.stepsBtns.forEach((elem, index) => {
      
      if(index <= (activeStepNum) ) {
        elem.classList.add('js-active');
      }
      
    });
  };
  
  //get active panel
  const getActivePanel = () => {
    
    let activePanel;
    
    DOMstrings.stepFormPanels.forEach(elem => {
      
      if(elem.classList.contains('js-active')) {
        
        activePanel = elem;
      }
      
    });
    
    return activePanel;
                                      
  };
  
  //open active panel (and close unactive panels)
  const setActivePanel = activePanelNum => {
    
    //remove active class from all the panels
    removeClasses(DOMstrings.stepFormPanels, 'js-active');
    
    //show active panel
    DOMstrings.stepFormPanels.forEach((elem, index) => {
      if(index === (activePanelNum)) {
        
        elem.classList.add('js-active');
     
        // setFormHeight(elem);
        
      }
    })
    
  };
  
  //set form height equal to current panel height
  const formHeight = (activePanel) => {
    
    const activePanelHeight = activePanel.offsetHeight;
    
    DOMstrings.stepsForm.style.height = `${activePanelHeight}px`;
    
  };
  
  const setFormHeight = () => {
    const activePanel = getActivePanel();
  
    formHeight(activePanel);
  }
  
  //STEPS BAR CLICK FUNCTION
  DOMstrings.stepsBar.addEventListener('click', e => {
    
    //check if click target is a step button
    const eventTarget = e.target;
    
    if(!eventTarget.classList.contains(`${DOMstrings.stepsBtnClass}`)) {
      return;
    }
    
    //get active button step number
    const activeStep = getActiveStep(eventTarget);
    
    //set all steps before clicked (and clicked too) to active
    setActiveStep(activeStep);
    
    //open active panel
    setActivePanel(activeStep);
  });
  
  //PREV/NEXT BTNS CLICK
  DOMstrings.stepsForm.addEventListener('click', e => {
    
    const eventTarget = e.target;
    
    //check if we clicked on `PREV` or NEXT` buttons
    if(! ( (eventTarget.classList.contains(`${DOMstrings.stepPrevBtnClass}`)) || (eventTarget.classList.contains(`${DOMstrings.stepNextBtnClass}`)) ) ) 
    {
      return;
    }
    
    //find active panel
    const activePanel = findParent(eventTarget, `${DOMstrings.stepFormPanelClass}`);
    
    let activePanelNum = Array.from(DOMstrings.stepFormPanels).indexOf(activePanel);
    
    //set active step and active panel onclick
    if(eventTarget.classList.contains(`${DOMstrings.stepPrevBtnClass}`)) {
      activePanelNum--;
    
    } else {
      
      activePanelNum++;
    
    }
    
    setActiveStep(activePanelNum);
    setActivePanel(activePanelNum);
    
  });

  
  //changing animation via animation select !!!YOU DON'T NEED THIS CODE (if you want to change animation type, just change form panels data-attr)
  
  const setAnimationType = (newType) => {
    DOMstrings.stepFormPanels.forEach(elem => {
      elem.dataset.animation = newType;
    })
  };
  
  const newAnimationType = 'slideHorz';
  setAnimationType(newAnimationType);

