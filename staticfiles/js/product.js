
//Product price and product mrp validation

var product_price = document.getElementById('input-product_price');
var product_mrp=document.getElementById('input-product_mrp');



function priceValidation(value,mrp){
        if (value<=mrp){
            document.querySelector('#submit').removeAttribute('disabled');
            document.getElementById("productMrpValid"). className = "valid-feedback";
            document.getElementById("productMrpinValid").style.display = "none";
            document.getElementById("product1MrpinValid").style.display = "none";
            document.getElementById("productMrpValid").style.display = "block";

            setTimeout(() => {
                $("#productMrpValid").hide("slow");
//                document.getElementById("productMrpValid").fadeOut('slow');
//                document.getElementById("productMrpValid").style.display = "none";

             }, 2000);

        }else{
            document.querySelector('#submit').setAttribute("disabled", "false");
            document.getElementById('productMrpinValid').innerHTML='Give correct Mrp because selling Price is '+String(value);

            document.getElementById("productMrpinValid").style.display = "block";
        }
        return 1
        }



function priceValidation1(value,mrp){
        if (value<=mrp){
            document.querySelector('#submit').removeAttribute('disabled');
            document.getElementById("product1MrpValid"). className = "valid-feedback";
            document.getElementById("product1MrpinValid").style.display = "none";
            document.getElementById("product1MrpValid").style.display = "block";
            setTimeout(() => {
                $("#product1MrpValid").hide("slow");
//                document.getElementById("productMrpValid").fadeOut('slow');
//                document.getElementById("productMrpValid").style.display = "none";

             }, 2000);

        }else{
            document.querySelector('#submit').setAttribute("disabled", "false");
            document.getElementById('product1MrpinValid').innerHTML='Give correct selling Price '+String(mrp);

            document.getElementById("product1MrpinValid").style.display = "block";
        }
        return 1
        }

let inputBox = $('#input-product_price').val();


$('#input-product_mrp').on('input', function (evt) {
       let mrp1 = evt.target.value;
       let value1=document.getElementById('input-product_price').value;
       let mrp=document.getElementById('input-product_mrp').value;

       priceValidation(Number(value1),Number(mrp));

    });

$('#input-product_price').on('input', function (evt) {
       let mrp1 = evt.target.value;
       let value1=document.getElementById('input-product_price').value;
       let mrp=document.getElementById('input-product_mrp').value;

       priceValidation1(Number(value1),Number(mrp));

    });



//Product name validation

function nameValidation(name){
    if (name.length<=11){
        if (name.length==0){
                document.querySelector('#submit').setAttribute("disabled", "false");
                document.getElementById('productNameInValid').innerHTML='Sorry! please fill that';
                document.getElementById("productNameInValid").style.display = "block";
            }else{
            document.querySelector('#submit').removeAttribute('disabled');
            document.getElementById("productNameValid"). className = "valid-feedback";
            document.getElementById("productNameInValid").style.display = "none";
            document.getElementById("productNameValid").style.display = "block";
            setTimeout(() => {
                $("#productNameValid").hide("slow");
//                document.getElementById("productMrpValid").fadeOut('slow');
//                document.getElementById("productMrpValid").style.display = "none";

             }, 1000);
             }
    }else{


                document.querySelector('#submit').setAttribute("disabled", "false");
            document.getElementById('productNameInValid').innerHTML='Sorry! we provide 11 characters only';

            document.getElementById("productNameInValid").style.display = "block";



    }
    return 1

}


$('#input-product_name').on('input', function (evt) {
       let mrp1 = evt.target.value;
       console.log(typeof mrp1);
       let name=document.getElementById('input-product_name').value;

       nameValidation(name);

    });




//Product name validation

function numberValidation(number,tagId){
        if (typeof Number(number)=='number'){
            document.querySelector('#submit').removeAttribute('disabled');
            document.getElementById("numberValid"). className = "valid-feedback";
            document.getElementById("numberInValid").style.display = "none";
            document.getElementById("numberValid").style.display = "block";
            setTimeout(() => {
                $("#numberValid").hide("slow");
//                document.getElementById("productMrpValid").fadeOut('slow');
//                document.getElementById("productMrpValid").style.display = "none";

             }, 1000);
        }else if (typeof Number(number)=='null'){
            document.querySelector('#submit').setAttribute("disabled", "false");
            document.getElementById('numberInValid').innerHTML="It's not a number!";
            document.getElementById("numberInValid").style.display = "block";
        }
}


$('#input-product_unit').on('input', function (evt) {
       let mrp1 = evt.target.value;
       console.log(typeof mrp1);
       let number=document.getElementById('input-product_unit').value;
       let tagId='#input-product_unit'
       numberValidation(number,tagId);
       console.log(parseInt(mrp1));
       console.log(typeof Number(mrp1));
//       console.log(number.isNaN(parseInt(number)));

    });


//
//$(function(id) {
//        $(id).on('input', function(e) {
//            $(this).val($(this).val().replace(/[^0-9]/g, ''));
//        });
//    });
//
//
//function onlynum() {
//     let ip = document.getElementById("input-product_unit");
//
//        let res = ip.value;
//         if (res != '') {
//            if (isNaN(res)) {
//
//                // Set input value empty
//                ip.value = "";
//
//                // Reset the form
//
//                return false;
//            } else {
//                return true
//
//                }
//                }
//                }
//
//function('#input-product_unit');

//$('#input-product_price').on('input', function (evt) {
//   let price1 = evt.target.value;
////    console.log(price1);
//  });

////console.log("_________________",price.val());
//


//
//product_price.addEventListener('input', function() {
//            document.querySelector('#input-product_price').style.display= "block";
//});


//disabled="disabled"
//let eleman = document.getElementById('submit');
//eleman.setAttribute("disabled", "false");,'#input-product_mrp'