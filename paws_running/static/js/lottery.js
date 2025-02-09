// static/js/lottery.js

document.addEventListener('DOMContentLoaded', function() {
    const lotteryForm = document.querySelector('#lottery-form');
    if (lotteryForm) {
        lotteryForm.addEventListener('submit', function(event) {
            event.preventDefault();
            // Handle lottery spin logic here
            alert("You have participated in the lottery!");
            // You can add AJAX request to submit the lottery participation
        });
    }
});
