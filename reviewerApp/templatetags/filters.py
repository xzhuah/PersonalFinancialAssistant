from django import template

register = template.Library()


style = {
"food":{"style":"label label-default","icon":"glyphicon glyphicon-glass"},
"necessities":{"style":"label label-default","icon":"glyphicon glyphicon-shopping-cart"},

"transportation":{"style":"label label-primary","icon":"glyphicon glyphicon-plane"},
"entertainment":{"style":"label label-primary","icon":"glyphicon glyphicon-music"},
"education":{"style":"label label-primary","icon":"glyphicon glyphicon-education"},

"investment":{"style":"label label-success","icon":"glyphicon glyphicon-bitcoin"},

"salary":{"style":"label label-danger","icon":"glyphicon glyphicon-usd"},

"medical":{"style":"label label-warning","icon":"glyphicon glyphicon-plus"},

"other":{"style":"label label-info","icon":"glyphicon glyphicon-question-sign"}
}

@register.filter
def get_style(arg):
    global style
    if arg in style:
        return style[arg]["style"]
    else:
        return style["other"]["style"]

@register.filter
def get_icon(arg):
    global style
    if arg in style:
        return style[arg]["icon"]
    else:
        return
        return style["other"]["icon"]
