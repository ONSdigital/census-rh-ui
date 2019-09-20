import os
import sys
import gettext
from jinja2.ext import InternationalizationExtension
from jinja2.utils import contextfunction, Markup

# try:
#     BASE_PATH = sys._MEIPASS
# except:
#     BASE_PATH = os.path.abspath('.')

BASE_PATH = os.path.abspath('.')

sys.path.append(os.path.join(BASE_PATH, 'libs'))

localedir = os.path.join(BASE_PATH, 'app', 'translations')
domain = 'messages'

locales = []
for dirpath, dirnames, filenames in os.walk(localedir):
    for dirname in dirnames:
        locales.append(dirname)
    break

all_translations = {}
for locale in locales:
    all_translations[locale] = gettext.translation(domain, localedir, [locale])


def context_locale(context):
    lang = 'en'
    if 'locale' in context and context['locale'] in all_translations:
        lang = context['locale']
    return lang


def gettext(context, msg):
    return all_translations[context_locale(context)].gettext(msg)


def ngettext(context, singular, plural, n):
    return all_translations[context_locale(context)].ngettext(
        singular, plural, n)


class InternationalizationWithContextExtension(InternationalizationExtension):
    def _install_callables(self, gettext, ngettext, newstyle=None):
        if newstyle is not None:
            self.environment.newstyle_gettext = newstyle
        if self.environment.newstyle_gettext:
            gettext = _make_new_gettext(gettext)
            ngettext = _make_new_ngettext(ngettext)
        self.environment.globals.update(gettext=gettext, ngettext=ngettext)


@contextfunction
def _gettext_alias(__context, *args, **kwargs):
    return __context.call(__context.resolve('gettext'), *args, **kwargs)


def _make_new_gettext(func):
    @contextfunction
    def gettext(__context, __string, **variables):
        rv = __context.call(func, __context, __string)
        if __context.eval_ctx.autoescape:
            rv = Markup(rv)
        return rv % variables

    return gettext


def _make_new_ngettext(func):
    @contextfunction
    def ngettext(__context, __singular, __plural, __num, **variables):
        variables.setdefault('num', __num)
        rv = __context.call(func, __context, __singular, __plural, __num)
        if __context.eval_ctx.autoescape:
            rv = Markup(rv)
        return rv % variables

    return ngettext


i18n = InternationalizationWithContextExtension
