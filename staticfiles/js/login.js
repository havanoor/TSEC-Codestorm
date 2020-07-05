// var card = document.querySelector('.flip-button');
// card.addEventListener( 'click', function() 
//   card.classList.toggle('flip-karo');
// });



function toggleForm(){
var val=document.getElementById('flip-button')
val.classList.toggle('flip-karo')
console.log(val.classList.toString('flip-karo'))


}


function flip() {
    $('.card').toggleClass('flip-karo');
}
