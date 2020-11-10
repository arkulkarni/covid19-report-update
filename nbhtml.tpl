{% extends 'full.tpl'%}

{% block input_group %}
    {%- if cell.metadata.get('nbconvert', {}).get('show_code', False) -%}
        ((( super() )))
    {%- endif -%}
{% endblock input_group %}

{% block any_cell %}
    {{ super() }}
{% endblock any_cell %}

