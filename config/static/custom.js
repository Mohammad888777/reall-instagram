function commentFormToggle(parent_id){
    const forms=document.getElementById(parent_id)
    if (forms.classList.contains("d-none")){
        forms.classList.remove("d-none")
    }else{
        $(`#${parent_id}`).on("click",function(){
            $(this).fadeIn(2000)
        })
        forms.classList.add("d-none")
        
    }
}
console.log("HLLOOE")