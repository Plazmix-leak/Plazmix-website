# -*- coding: utf-8 -*-

from flask import Markup, current_app, json
from werkzeug.urls import url_encode

JSONEncoder = json.JSONEncoder

TEMPLATE = u'''
        <!-- start wysiwyg %s field -->
        <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote.min.js"></script>
        <textarea id="wysiwygField_%s" name="%s">%s</textarea>
        <script>
            $(document).ready(function() {
              $('#wysiwygField_%s').summernote();
            });
        </script>
        <!-- end wysiwyg %s field -->
'''


class WysiwygWidget(object):

    def __call__(self, field, error=None, **kwargs):
        return Markup(TEMPLATE % (field.name, field.name, field.name,
                                  field.data if field.data else '', field.name, field.name))
