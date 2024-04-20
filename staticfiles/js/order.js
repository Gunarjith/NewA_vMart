 let domainName1=location.protocol + "//" + location.host
 console.log(domainName1);

//let globalVar='paid'
function cliendStatusOAD(a){
    console.log(a,'aaaaaaaaaaaaaaaaaa');
    MyJavaScript(a);
    cartStatus(a)
//    globalVar=globalVar+''
//    globalVar=globalVar+a
}

function cartStatus(saved){
    let cartStatus=localStorage.getItem('cartStatus');
    if (cartStatus){
        'hi'
           cartTok=localStorage.setItem('cartStatus',saved);
        // let findlink = document.getElementsById("link_to");
        // findlink.href = "https://wa.me/917411722847?text=Menu_"+cartTok;
    }else{
    console.log('nowTocken',cartStatus);
        cartTok=localStorage.setItem('cartStatus',saved);

    }
}
function statusGet(){
    let statusGet=localStorage.getItem('cartStatus');
    return statusGet;
}
cartStatus('paid');

// function acceptFunction(orderHeader_id){
//     console.log('getttttttttttttttttttt')
//     let request1 = new XMLHttpRequest();
//     let urlAccept=domainName1+'/order/acceptPost/'+String(orderHeader_id);
//     console.log(urlAccept);
//     request1.open("GET", urlAccept, true);
//     request1.send();
// }
// function demo(){
//     console.log("helloCJ")
// }
$(document).on("click", ".button", function (orderHeader_id){
    console.log('getttttttttttttttttttt')
    let request1 = new XMLHttpRequest();
    let urlAccept=domainName1+'/order/acceptPost/'+String(orderHeader_id);
    console.log(urlAccept);
    request1.open("GET", urlAccept, true);
    request1.send();
}); 

$( document ).ready(function() {

setInterval(function () {
    $.ajax({
        type:"GET",
        url:domainName1+"/order/ajaxUpdate",


        success:function(response){
            var liveUpdateList=response.LiveUpdate;
            console.log(response.LiveUpdate);
            console.log(liveUpdateList[0],'orders');
            let ordersLive=liveUpdateList[0];
            let acceptLive=liveUpdateList[1];
            let delivered=liveUpdateList[2];
            // let allLive=liveUpdateList[3];


            document.getElementById("ordersLiveId").innerHTML = ordersLive;
            document.getElementById("acceptLiveId").innerHTML = acceptLive;
            document.getElementById("deliveredId").innerHTML = delivered;
            // document.getElementById("allLiveId").innerHTML = allLive;
          
        },
        error:function(response){
            alert("An Error Occured")
            }

});

},30000);
});




$( document ).ready(function() {
// setInterval(function () {
    $.ajax({
        type:"GET",
        url:domainName1+"/order/orderAjax",

        // data:{CSRF: 'kasfsfskjfksjvbksbvkj','a1':Number(product__id),'tokki':cartTok},
        success:function(response){
//            console.log("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj");
            console.log(response.paidUsers);
            var y=1;
            var orderCountNumber=''
            for (let x of response.paidUsers) {
                let orderCount="Order-"+String(y);
                let orderNumber=x.customer_number;
                console.log(x.order_date,'__________')
                var timeDp=x.order_date.toString().split('T')[1];
                var time=x.order_date.toString().split('T')[1];
                var dateDp=x.order_date.toString().split('T')[0]
                let time2=time.split(':');
                let time3=time2[0]+':'+time2[1]
                let date=new Date();
                console.log(date);
                let date1=date.toISOString().slice(0, 19).replace('T', ' ');
                let date2=date.toString().slice(0, 19).replace('T', ' ');
//                console.log(date.toISOString().split('T')[0]);
//                console.log(date.toTimeString().split(' ')[0]);
                var dateLive=date.toISOString().split('T')[0];
                var orderHeaderId=x.id;
                console.log(orderHeaderId,"idddddddddddddd");
//                console.log(time3);

                 if(x.order_date.toString().split('T')[0]==date.toISOString().split('T')[0]){

                    if ((Number(time2[0])>12)&&(Number(time2[0])!=24)){
                    let changeTime=Number(time2[0]);
                    let changeTime1=changeTime-12;
                    let time3=String(changeTime1)+':'+time2[1]+' pm'

                    orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                    y=y+1;
                }
                    else if(Number(time2[0])==24){
                    let time3=time2[0]+':'+time2[1]+' am';

                    orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                    y=y+1;

                }
                    else if(Number(time2[0])==12){
                    let time3=time2[0]+':'+time2[1]+' pm';

                    orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                    y=y+1;

                }
                    else{

                    let time3=time2[0]+':'+time2[1]+' am';

                    orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                    y=y+1;
                }


                 }else{
                       let time31=dateDp.split('-');
                       let dayIn=time31[2];
                       let monthIn=time31[1];
                       let yearIn=time31[0];
//                       console.log('hiiiiiiiiiiiiiiiiiiiiii');
                       let time3=dayIn+'-'+monthIn+'-'+yearIn;

                       orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                       y=y+1;
                 }



////
//                console.log(x.customer_number);
//                orderCountNumber=orderCountNumber+'<div class="userBlock"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"class="text-decoration-none"><div class="imageSender"><img src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png" class="img-cover"></div><div class="senderDetails"><div class="sendHead"><h4>'+String(orderCount)+'</h4><p class="senderTime">'+String(time3)+'</p></div><div class="senderNumber"><p>'+String(orderNumber)+'</p><div class="spinner-grow text-success" role="status"><span class="sr-only">Loading...</span></div></div></div></a></div>';
//                y=y+1;
            }
            document.getElementById("userChats").innerHTML = orderCountNumber

        },
        error:function(response){
            alert("An Error Occured")
            }

});

// },5000);
});

//function cliendInfo(orderIdDp,option_value){
//return $.ajax({
//
//
//                 url:domainName1+'clientInfo',
//
//                 success:function(response){
//
//                           console.log(response)
//
//                },
//                 error:function(response){
//                    alert("An Error Occured")
//                 }
//
//        });
//
//
//}

function myFunction(orderIdDp) {
    console.log("<<<<<<<<",orderIdDp);
    console.log()

    $.ajax({


                 url:domainName1+'/clientInfo',

                 success:function(response){

                           console.log(response)



  let clientStatus=response.clientInfo
     var option_value=statusGet();
//     console.log(orderIdDp,option_value)
//    console.log(cliendInfo(orderIdDp,option_value),'======')
//     let clientStatus=cliendInfo(orderIdDp,option_value)['responseJSON'];
//     console.log(clientStatus)
//     clientStatus=clientStatus.getResponseHeader()
//     console.log(clientStatus)
    // var option_value = document.getElementById("orderDe").value;
    if (clientStatus=='online'){
    var option_value='accept';
    console.log(option_value);
    if (option_value=='paid'){
        console.log('__-__--');

        $( document ).ready(function() {
        $.ajax({

                 type:"GET",
                 url:domainName1+'/order/orderAjaxRight/'+String(orderIdDp)+'/'+String(option_value),

                 success:function(response){

                    console.log(response.orderHeaderDetails[0],'llllllllllllllllllllllllllllllllll');
                    console.log(response.orderHeaderDetails[1])
//                    var productInnerList=response.orderHeaderDetails[0];
                    var productHtml=''
                    for (let b of response.orderHeaderDetails[1]){
                        console.log(b);
                        let productName=b.productName;
                        let productId=b.productId;
                        let productPrice=b.productPrice;
                        let productValues=b.productValues;
                        let productQuantity=b.productQuantity;

                        let productImage='https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/'+String(b.productImage);
                        productHtml=productHtml+'<tr><td class="tableTd1"><img src="'+productImage+'" alt="imge" class="me-2" height="50" width="50">'+productName+'</td><td class="tableTd2">'+String(productQuantity)+'</td><td class="tableTd3">'+String(productValues)+'</td></tr>'
                    }
                    var html=''



                    let productOrderHeaderId=response.orderHeaderDetails[0].orderHeaderId;
                    // let orderId=orderIdDp;
                    let userNumber=response.orderHeaderDetails[0].userNumber;
                    let totalAmount=response.orderHeaderDetails[0].totalPrice;
                    let customerName=response.orderHeaderDetails[0].customerName;
                    let customerAddressline1=response.orderHeaderDetails[0].customerAddressline1;
                    let customerArea=response.orderHeaderDetails[0].customerArea;
                    let customerPincode=response.orderHeaderDetails[0].customerPincode;

                    console.log(userNumber);
                    html =html+'<div class="divInvoiceAdress"><div style="display: flex;justify-content: space-between;margin: auto;line-height: 1.5;font-size: 14px;color: #4a4a4a;"><p><b>Adress:</b> <br><p>'+customerName+'</p><p>'+customerAddressline1+'</p><p>'+customerArea+'</p><p>'+customerPincode+'</p></p><p><b>Order no:</b> <p>'+orderIdDp+'</p></p><p><b>Mobile no:</b> <p>'+userNumber+'</p></p></div></div>'



                    document.getElementById("rightBody").innerHTML=html;

                },
                 error:function(response){
                    alert("An Error Occured")
                 }

        });
});

    }

    else if (option_value=='accept'){
         console.log('sasasasasasas')

         $( document ).ready(function() {
        $.ajax({

                 type:"GET",
                 url:domainName1+'/order/orderAjaxRight/'+String(orderIdDp)+'/'+String(option_value),

                 success:function(response){

                    console.log(response.orderHeaderDetails[0],'llllllllllllllllllllllllllllllllll');
                    console.log(response.orderHeaderDetails[1])
//                    var productInnerList=response.orderHeaderDetails[0];
                    var productHtml=''
                    for (let b of response.orderHeaderDetails[1]){
                        console.log(b);
                        let productName=b.productName;
                        let productId=b.productId;
                        let productPrice=b.productPrice;
                        let productValues=b.productValues;
                        let productQuantity=b.productQuantity;
                        let productImage='https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/'+String(b.productImage);
                        productHtml=productHtml+'<tr><td class="tableTd1"><img src="'+productImage+'" alt="imge" class="me-2" height="50" width="50">'+productName+'</td><td class="tableTd2">'+String(productQuantity)+'</td><td class="tableTd3">'+String(productValues)+'</td></tr>'
                    }
                    var html=''



                    let productOrderHeaderId=response.orderHeaderDetails[0].orderHeaderId;

                    let userNumber=response.orderHeaderDetails[0].userNumber;
                    let totalAmount=response.orderHeaderDetails[0].totalPrice;
                    let customerName=response.orderHeaderDetails[0].customerName;
                    let customerAddressline1=response.orderHeaderDetails[0].customerAddressline1;
                    let customerArea=response.orderHeaderDetails[0].customerArea;
                    let customerPincode=response.orderHeaderDetails[0].customerPincode;


                    html =html+'<div class="leftbodyHeader"><div class="userimage"><img src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png" class="img-cover" class="img-cover"></div><div><h4>'+String(userNumber)+'</h4></div><ul class="userIcons"><li><ion-icon name="scan-circle-outline"></ion-icon></li><li><ion-icon name="chatbox"></ion-icon></li><li><ion-icon name="ellipsis-vertical"></ion-icon></li></ul></div><div class="container"><div class="productHead"><strong class="d-none d-md-block h6 my-2">Product Details<hr class="d-none d-md-block my-2"></strong></div><div class="productData"><table class="table table-stripeds table-bordereds"><thead><tr><th>Product</th><th>Qty</th><th>Price</th></tr></thead><tbody>'+productHtml+'</tbody></table></div><div class="totalPrice"><h6 >Total Price<span> Rs. '+totalAmount+'</span></h6></div><div class="productHead"><hr class="d-none d-md-block my-2"><strong class="d-none d-md-block h6 my-2">User Details<hr class="d-none d-md-block my-2"></strong></div><div class="productData"><address class="address text-end"><p>'+customerName+'</p><p>'+customerAddressline1+'</p><p>'+customerArea+'</p><p>'+customerPincode+'</p><p>'+userNumber+'</p></address></div><hr class="d-none d-md-block my-2"><div><a href="#" class="Delivered" onclick="acceptFunction('+String(productOrderHeaderId)+')">Delivered</a></div><hr class="d-none d-md-block my-2"></div>'


                    document.getElementById("rightBody").innerHTML=html;

                },
                 error:function(response){
                    alert("An Error Occured")
                 }

        });
});
    }

    }else if(clientStatus=='offline'){

        console.log(option_value);
        if (option_value=='paid'){
        console.log('__-__--');

        $( document ).ready(function() {
        $.ajax({

                 type:"GET",
                 url:domainName1+'/order/orderAjaxRight/'+String(orderIdDp)+'/'+String(option_value),

                 success:function(response){

                    console.log(response.orderHeaderDetails[0],'llllllllllllllllllllllllllllllllll');
                    console.log(response.orderHeaderDetails[1])
//                    var productInnerList=response.orderHeaderDetails[0];
                    var productHtml=''
                    let countNum=1
                    let TotalQty=0
                    for (let b of response.orderHeaderDetails[1]){
                        console.log(b);
                        let productName=b.productName;
                        let productId=b.productId;
                        let productPrice=b.productPrice;
                        let productValues=b.productValues;
                        let productQuantity=b.productQuantity;
                        TotalQty=TotalQty+productQuantity;

                        let productImage='https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/'+String(b.productImage);
                        productHtml=productHtml+'<tr class="invoice-items"><td>'+countNum+'</td><td style="text-align: center; padding-right: 0;">'+productName+'</td><td style="text-align: right;">'+String(productQuantity)+'</td><td style="text-align: right;">₹ '+String(productValues)+'</td></tr>'
                        countNum=countNum+1;
                    }
                    var html=''



                    let productOrderHeaderId=response.orderHeaderDetails[0].orderHeaderId;
                    let table_number=response.orderHeaderDetails[0].tablenumber
                    // let orderId=orderIdDp;
                    let userNumber=response.orderHeaderDetails[0].userNumber;
                    let totalAmount=response.orderHeaderDetails[0].totalPrice;
//                    let customerName=response.orderHeaderDetails[0].customerName;
//                    let customerAddressline1=response.orderHeaderDetails[0].customerAddressline1;
//                    let customerArea=response.orderHeaderDetails[0].customerArea;
//                    let customerPincode=response.orderHeaderDetails[0].customerPincode;

                    console.log(userNumber);
                    let productHtmll='<div class="divInvoiceOrder"><table style="width: 100%; table-layout: fixed"><thead><tr><th style="width: 50px; padding-left: 0;">Sn.</th><th style="text-align: center; padding-right: 0;">Item Name</th><th style="text-align: right; padding-right: 0;">QTY</th><th style="text-align: right; padding-right: 0;">Price</th></tr></thead><tbody>'+productHtml+'</tbody></table><table style="width: 100%;background: #fcbd024f;border-radius: 4px;"><thead><tr><th>Total</th><th style="text-align: right; padding-right: 0;">Total Items '+String(TotalQty)+'</th><th>&nbsp;</th><th style="text-align: right;">₹ '+String(totalAmount)+'</th></tr></thead></table><table style="width: 100%;margin-top: 15px;border: 1px dashed #00cd00;border-radius: 3px;"><thead><tr><td>Total Amount In Rs: </td><td style="text-align: right;">₹ '+String(totalAmount)+'</td></tr></thead></table></div>'
                    html =html+'<div class="divInvoiceAdress"><div style="display: flex;justify-content: space-between;margin: auto;line-height: 1.5;font-size: 14px;color: #4a4a4a;"><p><b>TableNUmber:</b> <br><p>'+table_number+'</p></p><p><b>Order no:</b> <p>'+orderIdDp+'</p></p><p><b>Mobile no:</b> <p>'+userNumber+'</p></p></div></div><hr style="border: 1px dashed rgb(131, 131, 131); margin: 25px auto">'+productHtmll+'<button class="btnAcceptOrder" onclick="acceptFunction('+String(productOrderHeaderId)+')">Accept</button>'



                    document.getElementById("rightBody").innerHTML=html;

                },
                 error:function(response){
                    alert("An Error Occured")
                 }

        });
});

    }

        else if (option_value=='accept'){
         console.log('sasasasasasas')

         $( document ).ready(function() {
        $.ajax({
  type:"GET",
                 url:domainName1+'/order/orderAjaxRight/'+String(orderIdDp)+'/'+String(option_value),

                 success:function(response){

                    console.log(response.orderHeaderDetails[0],'llllllllllllllllllllllllllllllllll');
                    console.log(response.orderHeaderDetails[1])
//                    var productInnerList=response.orderHeaderDetails[0];
                    var productHtml=''
                    let countNum=1
                    let TotalQty=0
                    for (let b of response.orderHeaderDetails[1]){
                        console.log(b);
                        let productName=b.productName;
                        let productId=b.productId;
                        let productPrice=b.productPrice;
                        let productValues=b.productValues;
                        let productQuantity=b.productQuantity;
                        TotalQty=TotalQty+productQuantity;

                        let productImage='https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/'+String(b.productImage);
                        productHtml=productHtml+'<tr class="invoice-items"><td>'+countNum+'</td><td style="text-align: center; padding-right: 0;">'+productName+'</td><td style="text-align: right;">'+String(productQuantity)+'</td><td style="text-align: right;">₹ '+String(productValues)+'</td></tr>'
                        countNum=countNum+1;
                    }
                    var html=''



                    let productOrderHeaderId=response.orderHeaderDetails[0].orderHeaderId;
                    let table_number=response.orderHeaderDetails[0].tablenumber
                    // let orderId=orderIdDp;
                    let userNumber=response.orderHeaderDetails[0].userNumber;
                    let totalAmount=response.orderHeaderDetails[0].totalPrice;
//                    let customerName=response.orderHeaderDetails[0].customerName;
//                    let customerAddressline1=response.orderHeaderDetails[0].customerAddressline1;
//                    let customerArea=response.orderHeaderDetails[0].customerArea;
//                    let customerPincode=response.orderHeaderDetails[0].customerPincode;

                    console.log(userNumber);
                    let productHtmll='<div class="divInvoiceOrder"><table style="width: 100%; table-layout: fixed"><thead><tr><th style="width: 50px; padding-left: 0;">Sn.</th><th style="text-align: center; padding-right: 0;">Item Name</th><th style="text-align: right; padding-right: 0;">QTY</th><th style="text-align: right; padding-right: 0;">Price</th></tr></thead><tbody>'+productHtml+'</tbody></table><table style="width: 100%;background: #fcbd024f;border-radius: 4px;"><thead><tr><th>Total</th><th style="text-align: right; padding-right: 0;">Total Items '+String(TotalQty)+'</th><th>&nbsp;</th><th style="text-align: right;">₹ '+String(totalAmount)+'</th></tr></thead></table><table style="width: 100%;margin-top: 15px;border: 1px dashed #00cd00;border-radius: 3px;"><thead><tr><td>Total Amount In Rs: </td><td style="text-align: right;">₹ '+String(totalAmount)+'</td></tr></thead></table></div>'
                    html =html+'<div class="divInvoiceAdress"><div style="display: flex;justify-content: space-between;margin: auto;line-height: 1.5;font-size: 14px;color: #4a4a4a;"><p><b>TableNUmber:</b> <br><p>'+table_number+'</p></p><p><b>Order no:</b> <p>'+orderIdDp+'</p></p><p><b>Mobile no:</b> <p>'+userNumber+'</p></p></div></div><hr style="border: 1px dashed rgb(131, 131, 131); margin: 25px auto">'+productHtmll



                    document.getElementById("rightBody").innerHTML=html;

                },
                 error:function(response){
                    alert("An Error Occured")
                 }
        });
});
    }

    }






                },
                 error:function(response){
                    alert("An Error Occured")
                 }

        });


}


//__________________________________acceptPost____________________________________________





function emty(){
    document.getElementById("rightBody").innerHTML = '';
}



function MyJavaScript(statusByOrder)
{
emty();

//    var option_value = dropdown.options[dropdown.selectedIndex].value;
//    var option_text = dropdown.options[dropdown.selectedIndex].text;

 var option_text=statusByOrder;
            if (option_text=='paid'){

                $( document ).ready(function() {
//                setInterval(function () {
                $.ajax({
                    type:"GET",
                    url:domainName1+"/order/orderAjax",
                    success:function(response){

                        console.log(response.paidUsers);
                        var y=1;
                        var orderCountNumber=''
                        for (let x of response.paidUsers) {
                            let orderCount="Order-"+String(y);
                            let orderNumber=x.customer_number;
                            var timeDp=x.order_date.toString().split('T')[1];
                            var time=x.order_date.toString().split('T')[1];
                            var dateDp=x.order_date.toString().split('T')[0]
                            let time2=time.split(':');
                            let time3=time2[0]+':'+time2[1]
                            let date=new Date();
                            console.log(date);
                            let date1=date.toISOString().slice(0, 19).replace('T', ' ');
                            let date2=date.toString().slice(0, 19).replace('T', ' ');

                            var dateLive=date.toISOString().split('T')[0];
                            var orderHeaderId=x.id;
                            console.log(orderHeaderId,"idddddddddddddd");


                 if(x.order_date.toString().split('T')[0]==date.toISOString().split('T')[0]){

                    if ((Number(time2[0])>12)&&(Number(time2[0])!=24)){
                    let changeTime=Number(time2[0]);
                    let changeTime1=changeTime-12;
                    let time3=String(changeTime1)+':'+time2[1]+' pm'

                    orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                    y=y+1;
                }
                    else if(Number(time2[0])==24){
                    let time3=time2[0]+':'+time2[1]+' am';

                    orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                    y=y+1;

                }
                    else if(Number(time2[0])==12){
                    let time3=time2[0]+':'+time2[1]+' pm';

                    orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                    y=y+1;

                }
                    else{

                    let time3=time2[0]+':'+time2[1]+' am';

                    orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                    y=y+1;
                }


                 }else{
                       let time31=dateDp.split('-');
                       let dayIn=time31[2];
                       let monthIn=time31[1];
                       let yearIn=time31[0];
//                       console.log('hiiiiiiiiiiiiiiiiiiiiii');
                       let time3=dayIn+'-'+monthIn+'-'+yearIn;

                       orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                       y=y+1;
                 }

            }
            document.getElementById("userChats").innerHTML = orderCountNumber

        },
        error:function(response){
            alert("An Error Occured")
            }

});
//                },1000);
                });

            }
            else if (option_text=='accept'){

                 $( document ).ready(function() {
//                setInterval(function () {
                $.ajax({
                    type:"GET",
                    url:domainName1+"/order/acceptAjax",
                    success:function(response){

                        console.log(response.paidUsers);
                        var y=1;
                        var orderCountNumber=''
                        for (let x of response.paidUsers) {
                            let orderCount="Order-"+String(y);
                            let orderNumber=x.customer_number;
                            var timeDp=x.order_date.toString().split('T')[1];
                            var time=x.order_date.toString().split('T')[1];
                            var dateDp=x.order_date.toString().split('T')[0]
                            let time2=time.split(':');
                            let time3=time2[0]+':'+time2[1]
                            let date=new Date();
                            console.log(date);
                            let date1=date.toISOString().slice(0, 19).replace('T', ' ');
                            let date2=date.toString().slice(0, 19).replace('T', ' ');

                            var dateLive=date.toISOString().split('T')[0];
                            var orderHeaderId=x.id;
                            console.log(orderHeaderId,"idddddddddddddd");


                 if(x.order_date.toString().split('T')[0]==date.toISOString().split('T')[0]){

                    if ((Number(time2[0])>12)&&(Number(time2[0])!=24)){
                    let changeTime=Number(time2[0]);
                    let changeTime1=changeTime-12;
                    let time3=String(changeTime1)+':'+time2[1]+' pm'

                    orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me" style="color:green"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                    y=y+1;
                }
                    else if(Number(time2[0])==24){
                    let time3=time2[0]+':'+time2[1]+' am';

                    orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me" style="color:green"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                    y=y+1;

                }
                    else if(Number(time2[0])==12){
                    let time3=time2[0]+':'+time2[1]+' pm';

                    orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me" style="color:green"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                    y=y+1;

                }
                    else{

                    let time3=time2[0]+':'+time2[1]+' am';

                    orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me" style="color:green"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                    y=y+1;
                }


                 }else{
                       let time31=dateDp.split('-');
                       let dayIn=time31[2];
                       let monthIn=time31[1];
                       let yearIn=time31[0];
//                       console.log('hiiiiiiiiiiiiiiiiiiiiii');
                       let time3=dayIn+'-'+monthIn+'-'+yearIn;

                       orderCountNumber=orderCountNumber+'<div class="userblocklistOfSideBarOrderSliderViewOneMain"><a href="#" onclick="myFunction('+String(orderHeaderId)+')" id="order_'+String(orderHeaderId)+'"><div class="senderDetailslistOfSideBarOrderSliderViewOneMain"><div class="sendHeadlistOfSideBarOrderSliderViewOneMain"><h4>'+String(orderCount)+'</h4><p class="senderTimesendHeadlistOfSideBarOrderSliderViewOneMain">'+String(time3)+'</p></div><div class="senderNumbersenderDetailslistOfSideBarOrderSliderViewOneMain"><p>'+String(orderNumber)+'</p><div class="blink_me" style="color:green"><i class="fa-solid fa-check"></i></div></div></div></a></div>';
                       y=y+1;
                 }




            }
            document.getElementById("userChats").innerHTML = orderCountNumber

        },
        error:function(response){
            alert("An Error Occured")
            }

});
//                },1000);
                });

            }

            else if (option_text=='delivered'){
               document.getElementById("userChats").innerHTML=''
            }


}


//var option_value = document.getElementById("orderDe").value;
//console.log(option_value);
//    MyJavaScript(dropdown);


//
//  $.ajax({
//        type:"POST",
//        url:domainName1+'/order/'+'acceptPost',
////        console.log(url);
//        data:[{CSRF: 'kasfsfskjfksjvbksbvkj','a':'12'}],
//        success:function(response){
//            console.log("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj",url,response);
//        },
//        error:function(response){
//            alert("An Error Occured")
//            }
//        });



