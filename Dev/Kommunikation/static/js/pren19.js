/**
 * Created by endru on 23.03.15.
 */


function initAction() {
    $('#PREN_AsyncMsg').html('');
    $('#PREN_Error_Container').hide();
    waitingDialog.show();
}

function endAction() {
    waitingDialog.hide();
}
function runAction(url) {
    initAction();
    var d = $.Deferred();
    var options = {
        method: "GET",
        url: url
    };
    return $.ajax(options).then(function (data) {
        waitingDialog.hide();
        return data;
    });
}


function getPicture() {
    runAction('/get_picture').done(function () {
        $('#PREN_AsyncMsg').html('<img src="/images/image.jpg?' + Math.floor(Math.random() * 10000) + '" />');
    }).fail(function (err) {
        handleError(err);
    });
}

function testZielerfassung() {
    runAction('/detect').done(function (data) {
        $('#PREN_AsyncMsg').html(data);
    }).fail(function (err) {
        handleError(err);
    });
}

function runBalldepot() {
    runAction('/test_balldepot').done(function (data) {
        $('#PREN_AsyncMsg').html(data);
    }).fail(function (err) {
        handleError(err);
    });
}

function runBallbefoerderung() {
    runAction('/run_ballbefoerderung').done(function (data) {
        $('#PREN_AsyncMsg').html(data);
    }).fail(function (err) {
        handleError(err);
    });
}

function stopBallbefoerderung() {
    runAction('/stop_ballbefoerderung').done(function (data) {
        $('#PREN_AsyncMsg').html(data);
    }).fail(function (err) {
        handleError(err);
    });
}

function setBFSpeed(val) {
    initAction();
    waitingDialog.hide();
    var d = $.Deferred();
    val = val / 100;
    var options = {
        method: "POST",
        url: "/set_bfspeed",
        data: "speed=" + val
    };

    $.ajax(options).done(function (data) {
        $('#PREN_AsyncMsg').html(data);
    }).fail(function (err) {
        handleError(err);
    });
}

function runAusrichtung() {
    runAction('/test_ausrichtung').done(function (data) {
        $('#PREN_AsyncMsg').html(data);
    }).fail(function (err) {
        handleError(err);
    });
}

function testAusrichtungWithDetect(){
    runAction('/test_ausrichtung_detect').done(function (data) {
        $('#PREN_AsyncMsg').html(data);
    }).fail(function (err) {
        handleError(err);
    });

}

function moveSteps(){
    initAction();
    waitingDialog.show();
    var d = $.Deferred();
    val = $('#ar_step_input').val();
    var options = {
        method: "POST",
        url: "/test_ausrichtung_steps",
        data: "steps=" + val
    };

    $.ajax(options).done(function (data) {
        waitingDialog.hide();
        $('#PREN_AsyncMsg').html(data);
    }).fail(function (err) {
        handleError(err);
    });
}

function start() {
    StartTimer();
    runAction('/start').done(function (data) {
        StopTimer();
        $('#PREN_AsyncMsg').html('<img src="/css/feuerwerk.jpg" /><div>' + data + '</div>');
    }).fail(function (err) {
        handleError(err);
        StopTimer();
    });
}

function start_camera(){
    runAction('/start_camera').done(function (data) {
        $('#PREN_AsyncMsg').html(data);
    }).fail(function (err) {
        handleError(err);
    });
}

function stop_camera(){
    runAction('/stop_camera').done(function (data) {
        $('#PREN_AsyncMsg').html(data);
    }).fail(function (err) {
        handleError(err);
    });
}

function shut_down(){
    runAction('/shut_down').done(function (data) {
        $('#PREN_AsyncMsg').html(data);
    }).fail(function (err) {
        handleError(err);
    });
}

function reset_control() {
    runAction('/reset').done(function (data) {
        StopTimer();
        $('#PREN_AsyncMsg').html(data);
    }).fail(function (err) {
        handleError(err);
        StopTimer();
    });
}

function init_control(){
    runAction('/init_control').done(function (data) {
        StopTimer();
        $('#PREN_AsyncMsg').html(data);
    }).fail(function (err) {
        handleError(err);
        StopTimer();
    });
}


function handleError(err) {
    $('#PREN_Error').html(err);
    $('#PREN_Error_Container').show();
    waitingDialog.hide();
}