/**
 * Created by endru on 23.03.15.
 */

function runAction(url){
    $('#PREN_AsyncMsg').html('');
    var d= $.Deferred();
    var options= {
        method: "GET",
        url: url
    };

    return $.ajax(options);
}


function getPicture(){
    runAction('/get_picture').done(function(){
        $('#PREN_AsyncMsg').html('<img src="/images/image.jpg?'+Math.floor(Math.random()*10000)+'" />');
    }).fail(function(err){
        $('#PREN_Error').html(err);
    });
}

function runBalldepot(){
    runAction('/test_balldepot').done(function(data){
        $('#PREN_AsyncMsg').html(data);
    }).fail(function(err){
        $('#PREN_Error').html(err);
    });
}

function runBallbefoerderung(){
    runAction('/test_ballbefoerderung').done(function(data){
        $('#PREN_AsyncMsg').html(data);
    }).fail(function(err){
        $('#PREN_Error').html(err);
    });
}