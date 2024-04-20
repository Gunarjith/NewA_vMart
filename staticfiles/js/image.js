const domainName=location.protocol + "//" + location.host
console.log(domainName);


$( document ).ready(function() {
    // setInterval(function () {
        $.ajax({
            type:"GET",
            url:domainName+"/avatar",
    
           
            success:function(response){
               console.log("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj");
            //    console.log(domainName+"/profile/avatar");
                console.log(response.imagepath);
                console.log(response.color1);
                console.log(response.color2);
                console.log(response.color3);

                document.getElementById('userImage').src=response.imagepath
                // document.getElementById('dashBoardNavVailo').style.backgroundColor=response.color1;
                // document.getElementById('sideBarDashBoardVailoUl').style.backgroundColor=response.color2;
                // document.getElementById('bodyId').style.backgroundColor=response.color3;
//                document.getElementById('navbarvmartbgc').style.backgroundColor=response.color4;
//                document.getElementById('maincustomervailobgc').style.backgroundColor=response.color5;
                // console.log('mohan changes');

                
               

            },
            error:function(response){
                alert("An Error Occured")
                }
    
    });
    
    // },5000);
    });
    
    

// formValidation.js

function checkFormValidity() {
    const form = document.getElementById("form1");
    const submitButton = document.getElementById("submitBtn");
    let isAnyFieldFilled = false;

    // Iterate through all form elements
    for (let i = 0; i < form.elements.length; i++) {
        const element = form.elements[i];
        if (element.type !== "submit" && element.value.trim() !== "") {
            isAnyFieldFilled = true;
            break;
        }
    }

    if (isAnyFieldFilled) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}

// Attach the checkFormValidity function to oninput event of all input fields
const inputFields = document.querySelectorAll("#form1 input");
inputFields.forEach((input) => {
    input.addEventListener("input", checkFormValidity);
});