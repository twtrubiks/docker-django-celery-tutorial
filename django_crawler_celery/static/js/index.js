$('#datatables').DataTable();


$("#start-celery").click(function (e) {
    e.preventDefault();
    $.ajax({
        url: 'task/',
        // url: 'download/',
        type: 'POST',
        dataType: "json",
        contentType: "application/json",
        data: {
            "language": "python"
        }
    }).done(function (msg) {
        $("#check-label").text(msg.data);
        // console.log(msg.data);
    })
});

