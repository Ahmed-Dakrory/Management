// File for your custom JavaScript


function showLoader(){
    // $('#loading').fadeIn('fast');
    $('#loaderHandler').css({display:'block'});
    // console.log('Showennn');
}

function hideLoader(){
    $('#loaderHandler').css({display:'none'});
    // console.log('hide');
}



function numberWithCommas(x) {

    x = x.toString().replace(/[,]+/g, '');
  
  if(x!=null){
    if(check_float(x)){
      x = parseFloat(x);
      x = x.toFixed(2);
    }else{
      
      x = parseFloat(x);
      x = x.toFixed(0);
    }
    
    
    decimal = (x+"").split(".")[0]
    fl_part = (x+"").split(".")[1]
  
    decimal = decimal.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    if(check_float(x)){
  
      return decimal+fl_part
    }else{
      
      return decimal;
    }
  }else{
    return '';
  }
  }
  