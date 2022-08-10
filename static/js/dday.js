 final_Day = new Date("2022-08-23:23:59:59+0900"); //예시 페이지 후원 마지막 날짜
  
function CalcDday(finalDay) {

        const today = new Date();

        const milliSecond = finalDay - today;
        const day = Math.floor(milliSecond / 1000 / 60 / 60 / 24);
        if (day === 0){
            return "D-day"
        }
        else{
            return day +"일";
        }
}
  
document.getElementById("detail_day").innerHTML = CalcDday(final_Day); 
  