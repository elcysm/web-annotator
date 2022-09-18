function keepData(){
    $(".username").val("Hiii");
}
function add_modal(){
    $('#addModal').modal('toggle'); 
}

$('.multisteps-form__form').change(function() {

var task_value = document.getElementById('task_select').value;
if (task_value == 'aspect'){
  document.getElementById('aspect_section').classList.remove('d-none');
}
else{
  document.getElementById('aspect_section').classList.add('d-none');
}
});

$('.multisteps-form__form').ready(function() {

  document.querySelector('button[title="Next_New"]').disabled = true;
  document.querySelector('button[title="btn_next2"]').disabled = true;
  

  var projects_database = document.getElementById('project').value.replace(/[&\/\\#+()$~%. '":*?<>{}[]/g, "").replace(']','');
  var project_list = projects_database.split(',');


  $('#project_value').on('keyup change',function(){
    var project_input = document.getElementById('project_value').value;
    if (project_input == ' '){
      document.getElementById('project_error').classList.remove('d-none');
      document.getElementById('project_error').innerHTML = "Project must be filled out!";
    }
    else{
      document.getElementById('project_error').classList.add('d-none');
    }

    if (project_list.includes(project_input)){
      document.getElementById('project_error').classList.remove('d-none');
      document.getElementById('project_error').innerHTML = "Project name has been already used!";
    }
    else{
      document.getElementById('project_error').classList.add('d-none');
    }
  });


  $('#file_upload').change(function(){
    var file_input = document.getElementById('file_upload').value;
    if (file_input == ''){
      document.getElementById('file_error').classList.remove('d-none');
      document.getElementById('file_error').innerHTML = "File must be chosen!";
    }
    else{
      document.getElementById('file_error').classList.add('d-none');
    }
  });

  $('.multisteps-form__form').on("mouseover", function(){
    var project_input = document.getElementById('project_value').value;
    var file_input = document.getElementById('file_upload').value;
    var tag_after = document.getElementById('tagnew').innerHTML;

    if ((project_input != '') && (file_input != '') && !(project_list.includes(project_input))){
      document.querySelector('button[title="Next_New"]').disabled = false;
      if (tag_after != ' '){
        document.querySelector('button[title="Submit"]').disabled = false;
      }
      else{
        document.querySelector('button[title="Submit"]').disabled = true;
      }
    }
    else{
      document.querySelector('button[title="Next_New"]').disabled = true;
      document.querySelector('button[title="btn_next2"]').disabled = true;
    }

   
    
  });


});



function new_project(){
  var process = document.getElementById('upload');
  process.classList.remove('d-none');
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


function span_pos(btn){
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


function span(btn, lentoken){
    var button_id = btn.getAttribute('id');
    var button_id_number = button_id.split('_')[1]
    var index_button = button_id.split('_')[0];
    var pre_index = parseInt(button_id_number) - 1;
    var next_index = parseInt(button_id_number) + 1;

    if (pre_index == -1){
        pre_index = 0;
    }
    if (next_index == lentoken){
      next_index = lentoken-1;
    }
    
    var pre_button = document.getElementById(index_button + "_" + pre_index);
    var next_button = document.getElementById(index_button + "_" + next_index);

    while ((pre_button.classList.contains('d-none')) && (pre_index >= 1)){
      pre_index -= 1;
      pre_button = document.getElementById(index_button + "_" + pre_index);
    }
    while ((next_button.classList.contains('d-none')) && (next_index <= lentoken-2)){
      next_index += 1;
      next_button = document.getElementById(index_button + "_" + next_index);
    }
    
    var pre_button_value = pre_button.querySelector('input[class="btn review d-none"]').value;
    var next_button_value = next_button.querySelector('input[class="btn review d-none"]').value;

    var pre_button_label = pre_button.querySelector('input[id="postag"]').value;
    var next_button_label = next_button.querySelector('input[id="postag"]').value;
    var current_button_value = btn.querySelector('input[class="btn review d-none"]').value;

  if (btn.querySelector('i').classList.value == 'close-button d-none'){

    btn.classList.add('btn-outline-success');
    btn.querySelector('span[class="badge btn-grad"]').innerHTML = pos_tag_name;
    btn.querySelector('i').classList.remove('d-none'); 
    btn.querySelector('input[id="postag"]').value = pos_tag_name;
    var current_button_label = btn.querySelector('input[id="postag"]').value;

    if ((current_button_label == pre_button_label)){
        btn.innerHTML =`
        <span class="name_token">${pre_button_value} ${current_button_value}</span>
        <i class="close-button"></i>
        <input class="btn review d-none" name="token_${index_button}" value="${pre_button_value} ${current_button_value}"> 
        <input id="postag" class="btn d-none" name="tag_${index_button}" value="${current_button_label}"> 
        <span id="pos" class="badge btn-grad">${current_button_label}</span>
        `
        pre_button.classList.add('d-none');
        pre_button.querySelector('input[class="btn review d-none"]').value = '';
        pre_button.querySelector('input[id="postag"]').value = current_button_label;
        pre_button.querySelector('i').classList.add('d-none'); 
    }

    if ((current_button_label == next_button_label)){
  
      btn.innerHTML =`
        <span class="name_token">${current_button_value} ${next_button_value}</span>
        <i class="close-button"></i>
        <input class="btn review d-none" name="token_${index_button}" value="${current_button_value} ${next_button_value}"> 
        <input id="postag" class="btn d-none" name="tag_${index_button}" value="${current_button_label}"> 
        <span id="pos" class="badge btn-grad">${current_button_label}</span>
      `
      next_button.classList.add('d-none');
      next_button.querySelector('input[class="btn review d-none"]').value = '';
      next_button.querySelector('input[id="postag"]').value = current_button_label;
      next_button.querySelector('i').classList.add('d-none'); 
    }

    if (((current_button_label == next_button_label) && (current_button_label == pre_button_label))){
      btn.innerHTML =`
        <span class="name_token">${pre_button_value} ${current_button_value} ${next_button_value}</span>
        <i class="close-button"></i>
        <input class="btn review d-none" name="token_${index_button}" value="${pre_button_value} ${current_button_value} ${next_button_value}"> 
        <input id="postag" class="btn d-none" name="tag_${index_button}" value="${current_button_label}"> 
        <span id="pos" class="badge btn-grad">${current_button_label}</span>
      `
      next_button.classList.add('d-none');
      next_button.querySelector('input[class="btn review d-none"]').value = '';
      next_button.querySelector('input[id="postag"]').value = current_button_label;
      next_button.querySelector('i').classList.add('d-none'); 
      pre_button.classList.add('d-none');
      pre_button.querySelector('input[class="btn review d-none"]').value = '';
      pre_button.querySelector('input[id="postag"]').value = current_button_label;
      pre_button.querySelector('i').classList.add('d-none'); 
    }


  }
  else{
    var temp = current_button_value.split(' ');
    if (temp.length != 1){
      var id = button_id_number - temp.length + 1;
      
      while ((document.getElementById(index_button + "_"+ id) == null)){
        id += 1;
      }
      while ((document.getElementById(index_button + "_" + id).querySelector('input[id="postag"]').value != document.getElementById(button_id).querySelector('input[id="postag"]').value)){
        id += 1;
      }
      for (var i = 0; i < temp.length; i++){
        var temp_id = id+i;
        if (document.getElementById(index_button + "_" + temp_id).querySelector('input[id="postag"]').value != document.getElementById(button_id).querySelector('input[id="postag"]').value){
          id+=1;
        }
      }
      while ((document.getElementById(index_button + "_" + id).querySelector('input[id="postag"]').value != document.getElementById(button_id).querySelector('input[id="postag"]').value)){
        id += 1;
      }
      for (var i = 0; i < temp.length; i++){
        document.getElementById(index_button + "_"+ id).classList.remove('btn-outline-success');
        document.getElementById(index_button + "_"+ id).classList.remove('d-none');
        document.getElementById(index_button + "_"+ id).querySelector('span[class="name_token"]').innerHTML = temp[i];
        document.getElementById(index_button + "_"+ id).querySelector('i').classList.add('d-none'); 
        document.getElementById(index_button + "_"+ id).querySelector('input[class="btn review d-none"]').value = temp[i];
        document.getElementById(index_button + "_"+ id).querySelector('input[id="postag"]').value = '';
        document.getElementById(index_button + "_"+ id).querySelector('span[class="badge btn-grad"]').innerHTML = '';
        id += 1;
      }
    }
    else{
      btn.querySelector('i').classList.add('d-none');
      btn.classList.remove('btn-outline-success');
      btn.querySelector('span[class="badge btn-grad"]').innerHTML = '';
      btn.querySelector('input[id="postag"]').value = '';
    }
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
var start_button;
var end_button;
var data_parcing = []
var data;
function get_tag_par(btn, i){
  clicks += 1;
  btn.querySelector('input[id="partag"]').value = pos_tag_name;
  btn.classList.add('active');

  var btn_id = btn.getAttribute('id');
  var data_number = btn_id.split('_')[0];
  var btn_number = btn_id.split('_')[1];

  start = btn.querySelector('input[id="partoken"]').value;
  
  if (clicks == 1){
    data = start ;
    document.body.style.cursor = 'alias';
    disable_button();
    start_button = btn;
    draw_canva(clicks, tag, data_number, btn_number);
  }

  if (clicks == 2){
    tag = pos_tag_name;
    btn.classList.add('active');
    end = btn.querySelector('input[id="partoken"]').value;
    draw_canva(clicks, tag, data_number, btn_number);
    end_button = btn;
    clicks = 0;
    data = tag + " " + data +  " " + end ;
    
    data_temp = data.split(' ')

    

    $(`#selec_${i}`).prepend(`
    <button onclick="delete_button(this)" class="btn text-left col-12 col-sm-12 text-over btn-outline-danger mt-2" type="button">
      <i class="fa fa-close"></i>
      <span class="badge btn-grad">Tag:  </span> <span id="tag" > ${data_temp[0]}</span> 
      <span class="badge btn-success">Start: </span> <span id="start"> ${data_temp[1]} </span> &nbsp;
      <span class="badge btn-danger">End: </span> <span id="end" > ${data_temp[2]} </span> &nbsp;
      <input class="d-none" name="parsing_${i}" value="${data}"></input>
		</button>`);


    document.body.style.cursor = 'default';
    enable_button();
    delete_label();

  }
}




var sx;
var sy;
var height = 0;
var hx;
var hy;
var ctx;
var can;
var button_list = [];

function draw_canva(clicks, tag, data_number, btn_number){

  function drawArrowhead(locx, locy, angle, sizex, sizey) {
    hx = sizex / 2;
    hy = sizey / 2;
    ctx.translate((locx), (locy));
    ctx.rotate(angle);
    ctx.translate(-hx, -hy);
  
    ctx.beginPath();
    ctx.moveTo(0,0);
    ctx.lineTo(0,1*sizey);    
    ctx.lineTo(1*sizex,1*hy);
    ctx.fill();
    }

   // returns radians
   function findAngle(sx, sy, ex, ey) {
    // make sx and sy at the zero point
    return Math.atan((ey - sy) / (ex - sx));
  }

  button_list.push(btn_number);
  var count = 0;
if (clicks == 1){
    
    for (var i = 0; i < button_list.length; i++){
      if (button_list[i] == btn_number){
        count++;
      }
    }

    temp_number = btn_number;
    sx_temp = 100 + 200*(btn_number) ;     //bat dau theo x
    sy = 100 - (30*count);       //bat dau theo y

  
}
if (clicks == 2){
  can = document.getElementById('canvas_' + data_number);
  ctx = can.getContext('2d');
  var ex = 100 + 200*(btn_number);     //diem cuoi cung theo x
  sx = (ex + sx_temp)/2; 
  var ey = 145;     //diem cuoi cung theo y
  ctx.beginPath();
  ctx.fillStyle = "rgba(55, 217, 56,1)";
  ctx.moveTo(sx_temp, 150);
  ctx.quadraticCurveTo( sx, sy , ex, ey);

  for (var i = 0; i < button_list.length; i++){
    if (button_list[i] == temp_number){
      count++;
    }
  }

  ctx.font = "15px Poppins";
  ctx.textAlign = "center";
  ctx.fillText(tag, sx, sy+(count*15));
  ctx.stroke();

  var ang = findAngle(sx, sy, ex, ey);
  if(btn_number<temp_number){
    ang += 135;
  }
  ctx.fillRect(ex, ey, 2, 2);
  drawArrowhead(ex, ey, ang, 12, 12);
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  }
}

function reset1(i){
  can = document.getElementById('canvas_'+i);
  ctx = can.getContext('2d');
  ctx.clearRect(0, 0, can.width, can.height);
  button_list = [];
  $(`#selec_${i}`).remove();
  clicks = 0;
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
}

function delete_label(){
  var button = document.getElementsByClassName("text-token");
  for (var i = 0; i < button.length; i++){
    button[i].classList.remove('active');
  }
}



var input_tagnew;
var tagnew;
function runScript(e) {
    if (e.keyCode == 13) {
        input_tagnew = document.getElementById('input_tagnew');
        tagnew = input_tagnew.value;
        input_tagnew.value = ''; 
        $('#tagnew').prepend(`<button onclick="delete_button(this)" class="btn btn-outline-danger mr-2" type="button">
        <i class="fa fa-close"></i>
        <span class="badge btn-grad mt-1">${tagnew}</span>
        <input class="d-none" name="label" value="${tagnew}"></input>
        </button>`);
      document.querySelector('button[title="Submit"]').disabled = false;
      return false;
    }
}

var input_entity;
var entity_new;
function runScript_entity(e) {
  if (e.keyCode == 13) {
    input_entity = document.getElementById('input_entity');
    entity_new = input_entity.value;
    input_entity.value = ''; 
      $('#tag_entity').prepend(`<button onclick="delete_button(this)" class="btn btn-outline-danger mr-2" type="button">
      <i class="fa fa-close"></i>
      <span class="badge btn-grad">${entity_new}</span>
      <input class="d-none" name="label_entity" value="${entity_new}"></input>
      </button>`);
    document.querySelector('button[title="Submit"]').disabled = false;
    return false;
  }
}

var input_attribute;
var attribute_new;
function runScript_attribute(e) {
  if (e.keyCode == 13) {
    input_attribute = document.getElementById('input_attribute');
    attribute_new = input_attribute.value;
    input_attribute.value = ''; 
      $('#tag_attribute').prepend(`<button onclick="delete_button(this)" class="btn btn-outline-danger mr-2" type="button">
      <i class="fa fa-close"></i>
      <span class="badge btn-grad">${attribute_new}</span>
      <input class="d-none" name="label_attribute" value="${attribute_new}"></input>
      </button>`);
    document.querySelector('button[title="Submit"]').disabled = false;
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

