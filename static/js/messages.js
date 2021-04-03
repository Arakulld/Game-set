$(".close").on('click', function (e) {
    e.preventDefault();
    if ($(".messages").children().length > 0) {
        $(".messages").children()[$(".messages").children().length - 1].remove();
    }
});