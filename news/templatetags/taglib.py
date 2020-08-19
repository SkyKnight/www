from django.template import Library, Node, TemplateSyntaxError
from django.db.models import get_model
from django.db import connection

register = Library()

class ContentArchives(Node):
    """
    Retrieve an monthly archive listing, based on the a model of your
    decision. Of course you can format the output completely.

    When you use HTML as format please note that you should use single
    quotes ``'`` around the format instead the usual double quote ``"``.

    The format string can take these "variables", used like in Python
    (``%(variable)s``):

        * ``nicedate`` -- SQL-DateFormat string "%M %Y",
          e.g. "August 2007".

        * ``name`` -- The plural verbose name, which was defined in
          the ``Meta`` class by the attribute ``verbose_name_plural``.
          If you use i18n, this will also be translated automaticly.

        * ``year`` -- Year of the archive, four digits.

        * ``month`` -- Month of the archive, two digits.

        * ``count`` -- Number of nodes in the current archive.

    You should really use ``name`` as variable, especially when you use
    this template tag for more than one model. Otherwise, it is
    possible that you have "August 2005" twice as title...

    Syntax::

        {% get_archives `object] `datefield] with `urlformat] %}

    Example::

        {% get_archives weblog.Entry pub_date with '<link rel="archives" 
title="%(name)s %(nicedate)s (%(count)s)" 
href="/weblog/%(year)s/%(month)s/" />' %}

    Example Output::

        <link rel="archives" title="Blog Entries August 2007 (1)" 
href="/weblog/2007/08/" />
        <link rel="archives" title="Blog Entries November 2006 (1)" 
href="/weblog/2006/11/" />
        <link rel="archives" title="Blog Entries July 2006 (1)" 
href="/weblog/2006/07/" />

    *Please Note:* ``%(name)s`` will be translated, in case you use 
I18N.
    """
    def __init__(self, model, field, htmlformat):
        self.field, self.htmlformat = field, htmlformat
        self.model_table = model.replace('.', '_').lower()
        self.model = get_model(*model.split('.'))

    def render(self, context):
        cursor = connection.cursor()
        try:
            from MySQLdb import OperationalError
        except ImportError: pass
        try:
            cursor.execute('SELECT DATE_FORMAT(' + self.field +
                           ', "%M %Y") AS date_title, DATE_FORMAT(' +
                           self.field + ', "%Y") AS year, DATE_FORMAT(' +
                           self.field + ', "%m") AS month,' +
                           'COUNT(*) as num FROM ' + self.model_table +
                           ' GROUP BY date_title ORDER BY year DESC, month DESC')
        except OperationalError:
            raise TemplateSyntaxError('get_archives tag seems to have gotten wrong arguments. '+
                                  'does the table "%s" has a field "%s"?' % (self.model_table, self.field))
        archives = cursor.fetchall()
        html_archive_links = ''
        for archive in archives:
            html_archive_links += self.htmlformat % {'nicedate': archive[0],
                                                     'year': archive[1],
                                                     'month': archive[2],
                                                     'count': archive[3],
                                                     'name': self.model._meta.verbose_name_plural}
        return html_archive_links

def get_archives(parser, token):
    bits = token.split_contents()
    if len(bits) != 5:
        raise TemplateSyntaxError('get_archives tag takes exactly four arguments')
    if bits[3] != 'with':
        raise TemplateSyntaxError('third argument to get_archives tag must be "with"')
    return ContentArchives(bits[1], bits[2], bits[4][1:-1]+"\n\t")
get_archives = register.tag(get_archives)

