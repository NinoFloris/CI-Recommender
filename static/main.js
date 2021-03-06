$(document).ready(function() {
    $('.paper-searchbar--submit').on('click', function() {
        var uif = $('#paper-searchbar--settings--independent-features').is(':checked');
        var pagerank = $('#paper-searchbar--settings--pagerank').is(':checked');
        var tfidf = $('#paper-searchbar--settings--tfidf').is(':checked');
        var clustering = $('#paper-searchbar--settings--clustering').is(':checked');
        var recommender = $('#paper-searchbar--settings--recommender').is(':checked');
        var results = $('.paper-searchbar--settings--results').val();
        var type = $('.paper-searchbar--type').val();
        var query = $('.paper-searchbar--input').val();
        $('.searchresults').empty();
        $('.searchresults').append('<img class="searchresults--loading" src="/static/482.png" />');

        $.ajax({
            type: "post",
            url: "http://localhost:5000/recommend",
            data: '{ "uif" : "' + uif + '", "pagerank" : "' + pagerank +'", "tfidf" : "' + tfidf +'", "clustering" : "' + clustering + '", "recommender" : "' + recommender + '", "results" : "' + results + '", "query" : "' + query + '", "type" : "' + type + '" }',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success : function(data) {
                $('.searchresults--loading').hide();
                $.each(data.results, function(i, item) {
                    $('<li class="searchresultsitem"></li>').html('<strong>' + item.title + '</strong></br> Pubmed ID:' + item.pmid + '<br/> Score: ' + item.score + '<br/>').appendTo('.searchresults');
                });
                // alert("results should be displayed");
            },
            error : function(data) {
                alert("error");
            }
        });

        return false;
    });
});