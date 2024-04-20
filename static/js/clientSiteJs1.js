
const domainName=location.protocol + "//" + location.host




//const domainName=window.location.hostname;
//const hostVar=location.host;
//const protocolVar=location.protocol;
 console.log(domainName);

// let TableNumber="{{tableNumber}}"
//  console.log(TableNumber)



 function starting(){
    document.getElementById('rightSideBarCustomerVailo').style.visibility="visible";
//     let cart=JSON.parse(localStorage.getItem('productsInCart'));
//     let totalCost=localStorage.getItem('totalCost');
//     let cartNumbers=localStorage.getItem('cartNumbers');
//     console.log(typeof cart,'carttttt')
//    if(Object.keys(cart).length === 0 && totalCost==0 && cartNumbers==0){
//     document.getElementById('rightSideBarCustomerVailo').style.visibility = "hidden";
//     console.log('hihihi')
//    }else{
//     document.getElementById('rightSideBarCustomerVailo').style.visibility="visible";
//    }



 }



function deleteProductCart(deleteId){
    // console.log(deleteId,'deleteId');
    let newCount=0;
    let newPrice=0;
    let productCart=JSON.parse(localStorage.getItem('productsInCart'));
    let productCartCount=Number(localStorage.getItem('cartNumbers'));
    let productPriceCount=Number(localStorage.getItem('totalCost'));
    
    for (const key in productCart) {

        // console.log(`${key}: ${productCart[key]['product_image']}`);
        let productCart1=productCart[key];
        if (key==deleteId){
            console.log(deleteId,'deleteId');
            localStorage.removeItem('productsInCart');
            localStorage.removeItem('cartNumbers');
            localStorage.removeItem('totalCost')
            delete (productCart[deleteId])
            localStorage.setItem('productsInCart',JSON.stringify(productCart));
            document.getElementById('remove'+String(deleteId)).remove();
            document.getElementById('removemobile'+String(deleteId)).remove();

            let cartTok=localStorage.getItem('cart_token');
            let request = new XMLHttpRequest();
            let comb=domainName+"/backProduct/"+String(deleteId)+"/"+cartTok+'/delete/'+String(TableNumber)+'/'
            console.log(comb);
            request.open("GET", comb, true);
            request.send()


  
        }else{
            newCount=newCount+ Number(productCart[key]['product_unit'])
            newPrice=newPrice+ Number(productCart[key]['product_price'])
        }
           
    }

    localStorage.setItem('cartNumbers',newCount);
    localStorage.setItem('totalCost',newPrice);
    document.getElementById('count_iiid').innerHTML=newCount;
    document.getElementById('cart-total').innerHTML=newPrice;
    document.getElementById('cart-total1').innerHTML=newPrice;

    // starting();
}



function decremental(decrId){
    // console.log(decrId,'decrId')
    let newCount=0;
    let newPrice=0;
    let productCart=JSON.parse(localStorage.getItem('productsInCart'));
    console.log(productCart,'productttttttsssssssssssssssssss');
    let productCartCount=Number(localStorage.getItem('cartNumbers'));
    let productPriceCount=Number(localStorage.getItem('totalCost'));
    for (const key in productCart) {

        // console.log(`${key}: ${productCart[key]['product_image']}`);
        let productCart1=productCart
        if (key==decrId){
            if (Number(productCart[key]['product_unit'])==1){
                deleteProductCart(decrId);
            }else if (Number(productCart[key]['product_unit'])>1){
                console.log(productCart[key]['product_price'],'decrId');
                let Qty=Number(productCart[key]['product_unit']);
                productCart[key]['product_unit']=Number(productCart[key]['product_unit'])-1;
                let piceOne=Number(productCart[key]['product_price'])/Qty;
                productCart[key]['product_price']=piceOne*Number(productCart[key]['product_unit'])
                console.log(productCart[key]['product_price'],'decrId');
                console.log(productCart)
                localStorage.removeItem('productsInCart');
                localStorage.removeItem('cartNumbers');
                localStorage.removeItem('totalCost')
            // delete (productCart[deleteId])
            // let pendingValue=productCart;
                localStorage.setItem('productsInCart',JSON.stringify(productCart));
                newCount=newCount+ Number(productCart[key]['product_unit'])
                newPrice=newPrice+ Number(productCart[key]['product_price'])
                document.getElementById('countCartWeb'+String(decrId)).innerHTML=Number(productCart[key]['product_unit'])
                document.getElementById('inlineAmountweb'+String(decrId)).innerHTML=Number(productCart[key]['product_price'])
                document.getElementById('countCartMobile'+String(decrId)).innerHTML=Number(productCart[key]['product_unit'])
                document.getElementById('inlineAmountMobile'+String(decrId)).innerHTML=Number(productCart[key]['product_price'])

                let cartTok=localStorage.getItem('cart_token');
                let request = new XMLHttpRequest();
                let comb=domainName+"/backProduct/"+String(decrId)+"/"+cartTok+'/decrement/'+String(TableNumber)+'/'
                console.log(comb);
                request.open("GET", comb, true);
                request.send()


            }
            
  
        }else{
            newCount=newCount+ Number(productCart[key]['product_unit'])
            newPrice=newPrice+ Number(productCart[key]['product_price'])
        }
           
    }

    localStorage.setItem('cartNumbers',newCount);
    localStorage.setItem('totalCost',newPrice);
    document.getElementById('count_iiid').innerHTML=newCount;
    document.getElementById('cart-total').innerHTML=newPrice;
    document.getElementById('cart-total1').innerHTML=newPrice;

}





function incremental(incrId){
    // console.log(incrId,'incrId')
    let newCount=0;
    let newPrice=0;
    let productCart=JSON.parse(localStorage.getItem('productsInCart'));
    console.log(productCart,'productttttttsssssssssssssssssss');
    let productCartCount=Number(localStorage.getItem('cartNumbers'));
    let productPriceCount=Number(localStorage.getItem('totalCost'));
    for (const key in productCart) {

        // console.log(`${key}: ${productCart[key]['product_image']}`);
        let productCart1=productCart
        if (key==incrId){
            if (Number(productCart[key]['product_unit'])>0){
                console.log(productCart[key]['product_price'],'incrId');
                let Qty=Number(productCart[key]['product_unit']);
                productCart[key]['product_unit']=Number(productCart[key]['product_unit'])+1;
                let piceOne=Number(productCart[key]['product_price'])/Qty;
                productCart[key]['product_price']=piceOne*Number(productCart[key]['product_unit'])
                console.log(productCart[key]['product_price'],'incrId');
                console.log(productCart)
                localStorage.removeItem('productsInCart');
                localStorage.removeItem('cartNumbers');
                localStorage.removeItem('totalCost')
            // delete (productCart[deleteId])
            // let pendingValue=productCart;
                localStorage.setItem('productsInCart',JSON.stringify(productCart));
                newCount=newCount+ Number(productCart[key]['product_unit'])
                newPrice=newPrice+ Number(productCart[key]['product_price'])
                document.getElementById('countCartWeb'+String(incrId)).innerHTML=Number(productCart[key]['product_unit'])
                document.getElementById('inlineAmountweb'+String(incrId)).innerHTML=Number(productCart[key]['product_price'])
                document.getElementById('countCartMobile'+String(incrId)).innerHTML=Number(productCart[key]['product_unit'])
                document.getElementById('inlineAmountMobile'+String(incrId)).innerHTML=Number(productCart[key]['product_price'])

                let cartTok=localStorage.getItem('cart_token');
                let request = new XMLHttpRequest();
                let comb=domainName+"/backProduct/"+String(incrId)+"/"+cartTok+'/increment/'+String(TableNumber)+'/'
                console.log(comb);
                request.open("GET", comb, true);
                request.send();


            }
            
  
        }else{
            newCount=newCount+ Number(productCart[key]['product_unit'])
            newPrice=newPrice+ Number(productCart[key]['product_price'])
        }
           
    }

    localStorage.setItem('cartNumbers',newCount);
    localStorage.setItem('totalCost',newPrice);
    document.getElementById('count_iiid').innerHTML=newCount;
    document.getElementById('cart-total').innerHTML=newPrice;
    document.getElementById('cart-total1').innerHTML=newPrice;

}






function cartDetails(){
    let productCart=JSON.parse(localStorage.getItem('productsInCart'));
    console.log(productCart,'productttttttsssssssssssssssssss');
    let productList=''
    let productListMobile=''
    for (const key in productCart) {

    console.log(`${key}: ${productCart[key]['product_image']}`);
    let productCart1=productCart[key];
   
       
        productList=productList+`<div class="product" id='remove${productCart[key]['id']}'>
        <div class="product-image">
            <img src="https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/${productCart[key]['product_image']}">
        </div>
        <div class="product-details">
            <div class="product-title text-capitalize">${productCart[key]['product_original_name']}</div>
            <div class="product-price">${productCart[key]['product_price']/productCart[key]['product_unit']}</div>
        </div>
        <div class="product-quantity">
            <div class="counterCart" id="counterCart4">
                <i class="fa-solid fa-minus decrementalCart" id='decrementalCartWeb${productCart[key]['id']}' onclick='decremental(${productCart[key]['id']})'></i>
                <div class="countCart" id="countCartWeb${productCart[key]['id']}">${productCart[key]['product_unit']}</div>
                <i class="fa-solid fa-plus incrementalCart" id='incrementalCartWeb${productCart[key]['id']}' onclick='incremental(${productCart[key]['id']})'></i>
    
            </div>
            <i class="fa-solid fa-trash trashIcon" id='incrementalCartWeb${productCart[key]['id']}' onclick='deleteProductCart(${productCart[key]['id']})'></i>
        </div>
    
        <div class="product-line-price" id='inlineAmountweb${productCart[key]['id']}'>${productCart[key]['product_price']}</div>
    </div>
    `
    


    productListMobile=productListMobile+` <div class="product" id='removemobile${productCart[key]['id']}'>
    <div class="product-image">
        <img src="https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/${productCart[key]['product_image']}">
    </div>
    <div class="product-details">
        <div class="product-title">${productCart[key]['product_original_name']}</div>
        <div class="product-price">${productCart[key]['product_price']/productCart[key]['product_unit']}</div>
    </div>
    <div class="product-quantity">
     
        <div class="counterCart" id="counterCart4">
            <i class="fa-solid fa-minus decrementalCart" onclick='decremental(${productCart[key]['id']})'></i>
            <div class="countCart" id="countCartMobile${productCart[key]['id']}">${productCart[key]['product_unit']}</div>
            <i class="fa-solid fa-plus incrementalCart" onclick='incremental(${productCart[key]['id']})'></i>

        </div>
        <i class="fa-solid fa-trash trashIcon"  onclick='deleteProductCart(${productCart[key]['id']})'></i>
    </div>

    <div class="product-line-price"  id='inlineAmountMobile${productCart[key]['id']}'>${productCart[key]['product_price']}</div>
</div>`
}

    
    let Price=localStorage.getItem('totalCost')
    document.getElementById('cartProductsweb').innerHTML=productList;
    document.getElementById('cartProductsMobile').innerHTML=productListMobile;
    document.getElementById('cart-total').innerHTML=Price;
    document.getElementById('cart-total1').innerHTML=Price;

}




$( document ).ready(function() {
setInterval(function () {
var cartNumbers1=document.getElementById("count_iiid").innerHTML;
var cartNumbers2=document.getElementById('link_to');

console.log("__________________________________  _____________",cartNumbers1);
console.log("()))())())())",document.getElementById("count_iiid").innerHTML);

let span_number=Number(cartNumbers1);
cartNumbers2.addEventListener('click',aaa())
function aaa(){
    console.log(typeof span_number,span_number);

    if($(window).width() >600){
    if (span_number==0){
//    document.getElementById("link_to").style.pointer-events = none;
        $("#link_to").css("pointer-events", "none");
        console.log("______________________if block")
        var element =document.getElementById("rightSideBarCustomerVailo");
        element.style.display = "none";
        document.getElementById('productListCustomerVailo').style['max-width']='100%';
        
        document.getElementById('item3').style['grid-template-columns']='repeat(3, 1fr)';
        document.getElementById('rightSideBarCustomerVailo ').style['max-width']='0%';
//    document.getElementById("cart_emty").innerHTML ="Our Cart Is empty";

    }else{
        console.log('else blockkkkkkkkkkkkk')
        $("#link_to").css("pointer-events", "auto");
        var element =document.getElementById("rightSideBarCustomerVailo");
        element.style.display = "block";
        document.getElementById('productListCustomerVailo').style['max-width']='70%';
        
        document.getElementById('item3').style['grid-template-columns']='repeat(2, 1fr)';
        document.getElementById('rightSideBarCustomerVailo ').style['max-width']='30%';
        // document.getElementById('productListCustomerVailo').style.width='800px';
    }


}
else if($(window).width() <600){
    if (span_number==0){
        //    document.getElementById("link_to").style.pointer-events = none;
                $("#iconNavOpen").css("pointer-events", "none");
                console.log("______________________if block")
                // document.getElementById('iconNavOpen').style['pointer-events']= 'none';
                // document.querySelector('.iconNavOpen').style['pointer-events']= 'none';    
                // document.querySelector('#cartIcon').style['pointer-events']= 'none';     
                       // var element =document.getElementById("rightSideBarCustomerVailo");
                // element.style.display = "none";
                // document.getElementById('productListCustomerVailo').style['max-width']='100%';
                
                // document.getElementById('item3').style['grid-template-columns']='repeat(3, 1fr)';
                // document.getElementById('rightSideBarCustomerVailo ').style['max-width']='0%';
        //    document.getElementById("cart_emty").innerHTML ="Our Cart Is empty";
        
            }else{
                console.log('else blockkkkkkkkkkkkk')
                $("#iconNavOpen").css("pointer-events", "auto");
                // document.querySelector('.iconNavOpen').style['pointer-events']= 'block';  
                // document.querySelector('#cartIcon').style['pointer-events']= 'block'; 
                // var element =document.getElementById("rightSideBarCustomerVailo");
                // element.style.display = "block";
                // document.getElementById('productListCustomerVailo').style['max-width']='70%';
                
                // document.getElementById('item3').style['grid-template-columns']='repeat(2, 1fr)';
                // document.getElementById('rightSideBarCustomerVailo ').style['max-width']='30%';
                // document.getElementById('productListCustomerVailo').style.width='800px';
            }
        
}
}

}, 100000);
});



console.log('hi');
$('.AddtoCartCustomerVailo').click(function(){

    console.log(this.id,"____id for user");
    // starting();
    // document.getElementById('rightSideBarCustomerVailo').style.visibility="visible";

let url=domainName+'/api/'+String(this.id)+'/';
let a=fetch(url).then(function(response) {
  return response.json();
}).then(function(data) {
 console.log(data.product[0],"____productObject");


    cartNumbers(data.product[0]);
    totalCost(data.product[0]);
    let cartTok=localStorage.getItem('cart_token');
    let product__id=Number(data.product[0].id);
    console.log(product__id,'[[[[[[');


    cartDetails();

     let request = new XMLHttpRequest();
     let comb=domainName+"/backProduct/"+String(product__id)+"/"+cartTok+'/addTwoCart/'+String(TableNumber)+'/'
     console.log(comb);
     request.open("GET", comb, true);
     request.send();



}).catch(function() {
  console.log("Booo");
});
});



function cartNumbers(product){
    console.log("___cartFunction inside");
    let productNumbers=localStorage.getItem('cartNumbers');

    productNumbers=parseInt(productNumbers);


    if (productNumbers){
        localStorage.setItem('cartNumbers',productNumbers+1);
        document.querySelector('.count').textContent=productNumbers+1;
    }else{
        localStorage.setItem('cartNumbers',1);
        document.querySelector('.count').textContent=1;
    }

    setItems(product);

};

function setItems(product){
console.log("setItemsFuction inside");
    let cartItems=localStorage.getItem('productsInCart');
    cartItems=JSON.parse(cartItems);
   console.log(cartItems,"________________");
    if (cartItems!=null){
//        console.log('not null');

        if(cartItems[product.id]==undefined){
//             console.log(cartItems[product.id],'pppppppppppp')
              cartItems={
                ...cartItems,
                [product.id]:product
             }
        }else{

             cartItems[product.id].product_unit +=1;
            cartItems[product.id].product_price =product.product_price+cartItems[product.id].product_price;
        }

    }else{
//        console.log('right');
         cartItems={
            [product.id]:product
            }
}
    localStorage.setItem('productsInCart',JSON.stringify(cartItems));
//    console.log('product-______',product)
    }





function totalCost(product){
    console.log("TotalCostFunctiuon");
    let cartCost=localStorage.getItem('totalCost');
//    console.log('1111',cartCost);
//    console.log('222',typeof cartCost);
    if(cartCost !=null){
        cartCost=parseInt(cartCost);
        localStorage.setItem('totalCost',cartCost+product.product_price);
    }else{
        localStorage.setItem('totalCost',product.product_price);
    }

}


function onLoadCartNumber(){
    console.log("onLoadCartNumberFunction");
    let productNumbers=localStorage.getItem('cartNumbers');
    if(productNumbers){
        document.querySelector('.count').textContent=productNumbers;
    }

}



var rand = function() {
    return Math.random().toString(36).substr(2); // remove `0.`
};

var token = function() {
    return rand() + rand(); // to make it longer
};

console.log(token());

function cartToken(){
    let cartTok=localStorage.getItem('cart_token');
    let coTb=localStorage.getItem('tb');


    if (cartTok){
        'hi'
        // let findlink = document.getElementsById("link_to");
        // findlink.href = "https://wa.me/917411722847?text=Menu_"+cartTok;
    }else{
    console.log('nowTocken',cartTok);
        cartTok=localStorage.setItem('cart_token',token());

    }
    if(coTb){
        'hi1'
    }else{
        coTb=localStorage.setItem('tb',TableNumber);
    }
}


function removeAll(){
    console.log("removeFunction");
    let cartTok=localStorage.getItem('cart_token');
    let tokk_n=document.querySelector("#link_to");
    tokk_n.href = "https://wa.me/"+String(ClientNumber)+"?text=Cart ID : "+cartTok;
    let tokk_n1=document.querySelector("#link_to1   ");
    tokk_n1.href = "https://wa.me/"+String(ClientNumber)+"?text=Cart ID : "+cartTok;
    localStorage.removeItem('cart_token');
    localStorage.removeItem('productsInCart');
    localStorage.removeItem('totalCost');
    localStorage.removeItem('cartNumbers');
    localStorage.removeItem('tb');

}





onLoadCartNumber();
cartToken();
cartDetails();






///______________________________________________________
//
//let product=[]
//let url=domainName+'/api/'++'/';
//let a=fetch(url).then(function(response) {
//  return response.json();
//}).then(function(data) {
//  console.log(data.product[0].product_name);
//
//
//}).catch(function() {
//  console.log("Booo");
//});

///_________________________________________________________

//localStorage.setItem('productsInCart',JSON.stringify(data.product[0]));
//    console.log('product',product);
//.addEventListener("click", displayDate);




