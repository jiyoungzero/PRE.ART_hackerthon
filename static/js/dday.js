const finalDay1 = "{{post.endday|date:'Y-m-d'}}"
          
function CalcDday(finalDay) {
    var today = new Date();
    finalDay = new Date(finalDay);
    var year = today.getFullYear();
    var month = ('0'+(today.getMonth() +1)).slice(-2);
    var day = ('0'+today.getDate()).slice(-2);
          
    var dateString = year + '-' + month + '-' + day;
    dateString = new Date(dateString);
          
    var dday = Math.ceil(((finalDay.getTime() - dateString.getTime()) / (1000*24*60*60)));
                          
    if (dday === 0){
        return "D-day"
    }
    else{
        return dday;
    }
}
          
document.getElementById("detail_day").innerHTML = CalcDday(finalDay1); 
