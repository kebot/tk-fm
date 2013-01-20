#
# all the jinja2 template can be compiled to JavaScript.
# Server and Client share the same templates.
#
# <body>
#   <div class="container">
#     {% block container %}
#   </div>
# </body>
#

define 'template', [], ->
  class View
    el: $('body')

    template: 'body'

    render: ->
      $('.container').render()

