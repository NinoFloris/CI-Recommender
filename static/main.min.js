$(document).ready(function() {
    $('.paper-searchbar--submit').on('click', function() {
        var type = $('.paper-searchbar--type').val();
        var query = $('.paper-searchbar--input').val();

        $.ajax({
            type: "post",
            url: "http://localhost:5000/recommend",
            data: '{ "query" : "' + query + '", "type" : "' + type + '" }',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success : function(data) {
                alert(data.query + data.type);
            },
            error : function(data) {
                alert("error");
            }
        });

        return false;
    });
});