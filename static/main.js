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
    document.querySelector('button[class="multisteps-form__progress-btn"]').disabled = true;
  }
  else{
    document.querySelector('button[title="Next"]').disabled = false;
    document.querySelector('button[class="multisteps-form__progress-btn"]').disabled = false;
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

var tag = ''
var start = ''
var end = ''

var data_parcing = []
var data;
function get_tag_par(btn, i){
  clicks += 1;
  btn.querySelector('input[id="partag"]').value = pos_tag_name;
  // btn.querySelector('span').innerHTML = pos_tag_name;
  btn.classList.add('active');


  start = btn.querySelector('input[id="partoken"]').value;
  
  if (clicks == 1){
    data = start ;
    disable_button();
  }

  if (clicks == 2){
    // btn.querySelector('span').innerHTML = pos_tag_name;
    tag = pos_tag_name;
    btn.classList.add('active');
    end = btn.querySelector('input[id="partoken"]').value;
    clicks = 0;
    data = tag + " " + data +  " " + end ;
    
    data_temp = data.split(' ')

    // data_parcing.push(data)

    $(`#selec_${i}`).prepend(`
    <button onclick="delete_button(this)" class="btn text-left col-12 col-sm-12 text-over btn-outline-danger mt-2" type="button">
      <i class="fa fa-close"></i>
      <span class="badge btn-grad">Tag:  </span> <span id="tag" > ${data_temp[0]}</span> 
      <span class="badge btn-success">Start: </span> <span id="start"> ${data_temp[1]} </span> &nbsp;
      <span class="badge btn-danger">End: </span> <span id="end" > ${data_temp[2]} </span> &nbsp;
      <input class="d-none" name="parsing_${i}" value="${data}"></input>
		</button>`);
    enable_button();
    delete_label();

  }
}
  
function disable_button(){
 
  var button_step = document.getElementsByClassName('multisteps-form__progress-btn');
  for (var i = 0; i < button_step.length; i++){
    button_step[i].disabled = true;
  }
  var button_next = document.getElementsByClassName('btn btn-grad ml-auto js-btn-next');
  for (var i = 0; i < button_next.length; i++){
    button_next[i].disabled = true;
  }
  var button_prev = document.getElementsByClassName('btn btn-primary js-btn-prev');
  for (var i = 0; i < button_prev.length; i++){
    button_prev[i].disabled = true;
  }
}

function enable_button(){
  
  var button_next = document.getElementsByClassName('btn btn-grad ml-auto js-btn-next');
  for (var i = 0; i < button_next.length; i++){
    button_next[i].disabled = false;
  }
  var button_step = document.getElementsByClassName('multisteps-form__progress-btn');
  for (var i = 0; i < button_step.length; i++){
    button_step[i].disabled = false;
  }
  var button_prev = document.getElementsByClassName('btn btn-primary js-btn-prev');
  for (var i = 0; i < button_prev.length; i++){
    button_prev[i].disabled = false;
  }
}

function delete_button(btn){
  if (btn.querySelector('i').classList.value == 'fa fa-close'){
      btn.remove();
  }
  else{

  }
}

function delete_label(){
  var button = document.getElementsByClassName("text-token");
  for (var i = 0; i < button.length; i++){
    button[i].classList.remove('active');
  }
}

var tagnew;
function splitLabel(input){
  if (input.value != ','){
    if (input.value.includes(',')){
      tagnew = input.value.replace(',','');
      input.value = '';
      $('#tagnew').prepend(`<button onclick="delete_button(this)" class="btn btn-outline-danger" type="button">
      <i class="fa fa-close"></i>
      <span class="badge btn-grad mt-1">${tagnew}</span>
      <input class="d-none" name="label" value="${tagnew}"></input>
		  </button> `);
    }
  } 
}

var input_tagnew;

function runScript(e) {
  
    if (e.keyCode == 13) {
        input_tagnew = document.getElementById('input_tagnew');
        tagnew = input_tagnew.value;
        input_tagnew.value = ''; 
        $('#tagnew').prepend(`<button onclick="delete_button(this)" class="btn btn-outline-danger" type="button">
        <i class="fa fa-close"></i>
        <span class="badge btn-grad mt-1">${tagnew}</span>
        <input class="d-none" name="label" value="${tagnew}"></input>
        </button> `);
      return false;
    }
}

function preventSubmit(e){
  if (e.keyCode == 13) {
    return false;
  }
}
var projectid;

function chooseExport(btn){
  projectid = btn.getAttribute('data-id');
  $('#exportModal').modal('toggle');
}


function deleteProject(btn){
  projectid = btn.getAttribute('data-id');
  $('#deleteModal').modal('toggle');
  document.getElementById('delete_span').innerHTML = projectid;
  document.getElementById('delete_link').href = `/admin/project/delete?project_id=${projectid}`; 
}


var annotatorid;
function deleteAnnotator(btn){
  annotatorid = btn.getAttribute('data-id');
  $('#deleteModal').modal('toggle');
  document.getElementById('delete_span').innerHTML = annotatorid;
  document.getElementById('delete_link').href = `/admin/collaborator/delete?annotator_username=${annotatorid}`; 
}


function deleteSubmit(btn){
  $.ajax({
    type: 'DELETE',
    url: btn.href,
    success: function(result) {
        if (result == '0') {
            
          location.reload();
            
        } else {
            alert("Cannot Delete!");
        }
    }
  });
  return false;
}

function readNoti(btn){
  var seen = btn.getAttribute('data-id');
}


function get_type(btn, number){
  if (btn.querySelector('i').classList.value == 'fa fa-check mr-1 d-none'){
    var type = btn.querySelector('input[id="type"]').value;
    btn.querySelector('i').classList.remove('d-none');
    document.getElementById('link_download').classList.remove('d-none');
    document.getElementById('link_download').href = `/admin/download?project=${projectid}&type=${type}`;  

    var button_csv = document.getElementById('csv').classList;
    var button_json = document.getElementById('json').classList;
    if (number == 1){
      button_csv.add('d-none');
    }
    else {
      button_json.add('d-none');
    }
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
      dom: '<"text-center mt-2 mb-2"i>t<"container-center mb-0 "p>',
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

function tooltip(){
  $('[data-toggle="tooltip"]').tooltip('toggle');
}
  
function mySubmitFunction(e) {
    e.preventDefault();
    return false;
}

function develop(){
    alert("Chức năng này đang phát triển!")
}
//    var opacity = 0;
//    var intervalID = 0;
//    window.onload = fadeIn;
   
//    function fadeIn() {
//        setInterval(show, 50);
//    }
   
//    function show() {
//        var body = document.getElementById("fade");
//        opacity = Number(window.getComputedStyle(body)
//                            .getPropertyValue("opacity"));
//        if (opacity < 1) {
//            opacity = opacity + 0.1;
//            body.style.opacity = opacity
//        } else {
//            clearInterval(intervalID);
//        }
//    }
    
//     $("#fade").fadeTo(3000, 500).slideUp(500, function(){
//     $("#fade").slideUp(500);
// });

//     $(document).ready(function() {
//         $("#fade").hide();
//         $("#fade").fadeTo(3000, 500).slideUp(500, function() {
//             $("#fade").slideUp(500);
//         });
//     });



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
$('.nav-link').each(function(){
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

