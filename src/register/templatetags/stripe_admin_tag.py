from django import template
register = template.Library()
from django.contrib.admin.templatetags import admin_modify
 
@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_line_row(context):
    context = context or {}
    ctx= admin_modify.submit_row(context)
    if context.get("readonly", None) != None:
        ctx["readonly"] = context.get("readonly")
    else:
    	ctx["readonly"] = False

    return ctx