debug = true;
// @TODO: REMOVE future!
var rovar = {
    messages: {
        'edit': 'Редактировать',
        'travel time': 'Время в пути',
        'add point': '<i class=\"icon plus\"></i> Добавить точку',
        'set coordinates': 'Выберите место на карте (Esc для отмены)',
        'unknown error': 'Неизвестная ошибка.',
        'success message': 'Ваше предложение будет рассмотрено модератором.',
        'error request method': "Неверный тип запроса.",
        'not init client': "Ваш клиент не инициализирован.",
        'required fields': "Поля 'Название', 'Категория', 'Описание', 'Адрес' являются обязательными.",
        'unknown url': "Указанный тип точки не существует.",
        'required image': "Вы не выбрали изображение или оно не верного формата.",
        'invalide url': "Не верный URL для поля 'Cайт'.",
        'feedback email': "Введите email для обратной связи.",
        'description length': "\"Описание\" не должно превышать 256 символов.",
    },
}


var comments = {
    items: [],
    setting: {
        wrapper: "#comments",
        labels: {
            'reply': 'Ответить',
            'say': 'Написать',
            'add_comment': 'Добавить комментарий'
        }
    },
    init: function (entryID, entryTYPE) {
        if (debug) {
            console.log("init function");
        }
        this.load(entryID, entryTYPE);
    },
    load: function (entryID, entryTYPE) {
        if (debug) {
            console.log("load function");
        }
        $(this.setting.wrapper).addClass("active").addClass("dimmer").html("<div class='ui text loader'>Сейчас все появится!:)</div>");
        $("#input_hidden_ENTRYID").val(entryID);
        $("#input_hidden_ENTRYTYPE").val(entryTYPE);
        var request = $.ajax({
                url: "/api/comments",
                method: "GET",
                data: {
                    entry_id: entryID,
                    entry_type: entryTYPE,
//          page: 0,
                    per_page: 100
                },
                dataType: "json"
            })
            .done(function (data) {
                if (data.empty == true) {
                    comments.items = [];
                } else {
                    comments.items = data;
                }
                comments.rePaint();
            })
            .fail(function (jqXHR, textStatus) {
                alert("Request failed: " + textStatus);
                comments.items = [];
                comments.rePaint();
            });
    },
    reBind: function () {
        $(".comments .actions .reply").click(function (e) {
            e.preventDefault();

            //Показать кроме активного
            $(".actions .reply").show();
            $(this).hide();
            var parent_id = $(this).data("commentid");
            $("#input_hidden_PARENTID").val(parent_id);
            $(this).after($("#add-comment-form"));
        });

        $(".comments .comment .author").click(function (e) {
            e.preventDefault();
            var $comment = $(this).closest(".comment");
            var username = $comment.children(".content").children(".author").html()
            var msg = $("#textarea_message").val();
            $("#textarea_message").val("@" + username + " " + msg);
        });

        function repeatdata() {
            console.log($(".repeatdata"));
            $(".repeatdata").each(function (i, val) {
                var timestamp = parseInt($(this).data("timestamp")) * 1000;
                var momentjs = moment(timestamp, "x").startOf('second').fromNow();
                $(this).html(momentjs);
            })
        }

        // Каждые 10 секунд обновлять время на комментариях
        // @TODO при удалении модального окна таймер остается:) так что память может потечь
        setInterval(repeatdata, 10000);
    },
    rePaint: function () {
        if (debug) {
            console.log("rePaint function");
        }
        if (this.items.length > 0) {
            $(".description-ratingcomment span a").html(rovar.messages['comment number'] + this.items.length)
        } else {
            $(".description-ratingcomment span a").html(rovar.messages['comment first'])
        }
        $("#pre-comments-form").after($("#add-comment-form"));
        $("#pre-comments-form").children(".reply").hide();
        $(this.setting.wrapper).removeClass("active").removeClass("dimmer").html("");
        this.drawItems($(this.setting.wrapper), null);
        this.reBind();
        $("#comment_modal").modal('refresh');
    },
    drawItems: function (wrapper, parent) {
        if (debug) {
            console.log("drawItems function");
        }
        console.log(this.items);
        var if_there = false;
        for (var i = 0; i < this.items.length; i++) {
            current = this.items[i];
            if (current.parent_id === parent) {
                if_there = true;
                this.drawItem(wrapper, current);
            }
        }
        ;
        if (parent && !if_there) { // Если вложенных комментов нет удалить враппер
            $(wrapper).remove();
        }
        ;
    },
    drawItem: function (wrapper, item) {
        if (debug) {
            console.log("drawItem function");
        }
        if (debug) {
            console.log("drawItem: ", current.id);
        }

        tpl = " \
	      <div class='comment' id='comment-" + current.id + "'> \
	        <a class='avatar'> \
	          <img class='ui avatar image' src='http://api.adorable.io/avatars/70/" + current.username + "' alt=''> \
	        </a> \
	        <div class='content'> \
	          <a class='author'>" + current.username + "</a> \
	          <div class='metadata'> \
	            <span class='date repeatdata' data-timestamp='" + current.timestamp + "'>" + moment(current.timestamp * 1000, "x").startOf('second').fromNow() + "</span> \
	          </div> \
	          <div class='text'> \
	            " + current.message + " \
	          </div> \
	          <div class='actions'> \
	            <a class='reply' data-commentid='" + current.id + "'> \
	            " + this.setting.labels['reply'] + "</a> \
	          </div> \
	          <div class='comments'></div> \
	        </div> \
	      </div>";

        $(wrapper).append(tpl);
        this.drawItems($("#comment-" + current.id + " > .content > .comments"), current.id);
    },
    add_comment: function (data) {
        if (debug) {
            console.log("add_comment function");
        }
        console.log(data);
        if (data.success) {
            $("#textarea_message").val("");
            $("#input_hidden_PARENTID").val("");
            this.items.push(data.comment);
            this.rePaint();
            this.reBind();
        } else {
            $("#ajax-errors").html($("<p class=\"error alert\">").text(this.__errors[data.error_code] || this.messages['unknown error']));
        }
    },
    show_form: function (parent_id) {
        if (debug) {
            console.log("show_form function");
        }
        this.hide_forms();
        $("#reply-" + parent_id).before("<form class='comment_form'><textarea></textarea><br><a id='add_comment' data-id='" + parent_id + "' href='#'>" + this.setting.labels['add_comment'] + "</a></form>")
    },
    hide_forms: function () {
        if (debug) {
            console.log("hide_forms function");
        }
        $(".comment_form").remove();
        $(".reply_button").show();
    },
    reply_button: function (button) {
        if (debug) {
            console.log("reply_button function");
        }
        this.show_form(button.data('id'))
        button.hide();
    }
};

//var entryID = data.id; // currentPoint.id
//var rating_get = $.ajax({
//        url: "/api/ratings",
//        method: "GET",
//        data: {
//            entry_id: entryID,
//            entry_type: "Point" // @TODO научиться принимать разные сущности
//        },
//        dataType: "json"
//    })
//    .done(function (data) {
//        var initialRating = data.initialRating, maxRating = data.maxRating;
//        if (data.is_auth) {
//            $('.ui.rating').rating({
//                initialRating: initialRating,
//                maxRating: maxRating,
//                onRate: function (value) {
//                    var $this = $(this);
//                    //Проверка на инициализацию
//                    //Если ещё не установлен флаг
//                    if ($this.hasClass('initial' + entryID)) {
//
//                        var rating_post = $.ajax({
//                                url: "/api/ratings",
//                                type: "POST",
//                                data: {
//                                    "entry_id": entryID,
//                                    "entry_type": "Point", // @TODO научиться принимать разные сущности
//                                    "value": value
//                                },
//                                dataType: "json"
//                            })
//                            .done(function (data) {
//                                alert("Cпасибо, ваш голос учтён!");
//                            })
//                            .fail(function (jqXHR, textStatus) {
//                                alert("Request failed: " + textStatus);
//                            });
//                    } else {
//                        $this.addClass('initial' + entryID)
//                    }
//                }
//            });
//        } else {
//            $('.ui.rating').rating({
//                initialRating: initialRating,
//                maxRating: maxRating
//            }).rating('disable');
//        }
//    })
//    .fail(function (jqXHR, textStatus) {
//        alert("Request failed: " + textStatus);
//    });

id = $("#obj_id").val();
if (id){
    comments.init(id, $("#obj_type").val()); // @TODO научится принимать тип entry из api
}

$("#add-comment-form").ajaxForm(function (data) {
    comments.add_comment(data);
});
