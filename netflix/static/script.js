$(function () {
    $('#like').on('click', function () {
        var url = $(this).attr('data-url')
        var token = $('[name=csrfmiddlewaretoken]').val()

        $.ajax({
            url: url,

            type: "POST",

            headers: {
                'X_CSRF-Token': token
            },

            success: function (data) {
                console.log('NOICE = NICE')
                $('#like').css('color', 'green')
                $('#likes').load(location.href + ' #likes_count')
                $('#dislikes').load(location.href + ' #dislikes_count')
            },
            error: function (msg) {
                alert('WTF DUDE')
                console.log(msg)
            }
        })
    })
})

$(function () {
    $('#dislike').on('click', function () {
        var url = $(this).attr('data-url')
        var token = $('[name=csrfmiddlewaretoken]').val()

        $.ajax({
            url: url,

            type: "POST",

            headers: {
                'X_CSRF-Token': token
            },

            success: function (data) {
                console.log('NOICE = NICE')
                $('#dilike').css('color', 'red')
                $('#dislikes').load(location.href + ' #dislikes_count')
                $('#likes').load(location.href + ' #likes_count')
            },
            error: function (msg) {
                alert('WTF DUDE')
                console.log(msg)
            }
        })
    })
})