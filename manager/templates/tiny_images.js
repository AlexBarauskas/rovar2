var tinyMCEImageList = new Array(
        {% for i in images%}
        ["{{i.title}}", "{{i.url}}"]{%if not forloop.last%},{%endif%}
        {% endfor %}
);