$(document).ready(function() {
    $('.paper-searchbar--submit').on('click', function() {
        var query = $('.paper-searchbar--input').val();

        $.ajax({
            type: "post",
            url: "http://localhost:5000/recommend",
            data: '{ "query" : "' + query + '" }',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success : function(data) {
                alert(data.query);
            },
            error : function(data) {
                alert("error");
            }
        });

        return false;
    });
});