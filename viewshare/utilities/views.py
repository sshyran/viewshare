import json
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.http import HttpResponseServerError, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from django.conf import settings
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.views.generic import View, ListView
from django.views.generic.base import RedirectView
from viewshare.apps.exhibit.permissions import PermissionsRegistry


def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context: None
    """
    t = loader.get_template(template_name)
    return HttpResponseServerError(t.render(RequestContext(request)))


class UserHomeView(RedirectView):
    def get_redirect_url(self, **kwargs):
        return reverse('profile_detail',
                       kwargs={'username': self.request.user.username})


class PlainTextResponse(TemplateResponse):
    def __init__(self, *args, **kwargs):
        kwargs['content_type'] = 'text/plain'
        super(PlainTextResponse, self).__init__(*args, **kwargs)


class BaseJSONView(View):

    def get_doc(self):
        """
        This should return a raw string representation of the response document
        """
        return "{}"

    def check_perms(self):
        """
        Returns a boolean value indicating whether or not the request user has
        the appropriate permissions to view this document
        """
        return True

    def cache_control_header(self):
        return "no-cache, must-revalidate"

    def get(self, request, *args, **kwargs):

        if not self.check_perms():
            raise Http404

        response = HttpResponse(self.get_doc())
        response["Content-Type"] = "application/json"
        response["Expires"] = 0
        response["Cache-Control"] = self.cache_control_header()
        return response


class JSONResponse(HttpResponse):

    def __init__(self, data, template=None, **extra_context):
        indent = 2 if settings.DEBUG else None

        if template:
            context = {"json": json.dumps(data, indent=indent)}
            if extra_context:
                context.update(extra_context)
            content = render_to_string(template, context)
            mime = "application/javascript"
        else:
            content = json.dumps(data, indent=indent)
            mime = ("text/javascript" if settings.DEBUG
                    else "application/json")
        super(JSONResponse, self).__init__(content=content, content_type=mime)


class OwnerSlugPermissionMixin:

    _object = None

    def filter_by_perm(self, obj):
        if hasattr(self, "object_perm") and \
           not self.request.user.has_perm(getattr(self, "object_perm"), obj):
                raise Http404
        return obj

    def get_object(self, queryset=None):
        if self._object is None:
            if queryset is None:
                queryset = self.get_queryset()
            obj = get_object_or_404(queryset,
                                    owner__username=self.kwargs.get("owner"),
                                    slug=self.kwargs.get("slug"))
            obj = self.filter_by_perm(obj)
            self._object = obj
        return self._object


class OwnerListView(ListView):
    """
    A base view for filtering based on the 'owner' of a particular object.
    'owner' is expected to be a username that maps to a Django User.
    """
    permission = None
    related = None
    defer = None
    owner_field = 'owner'

    def sort_filter(self):
        return

    def get_queryset(self):
        vars = self.request.GET
        sort = vars.get('sort', None)
        if sort:
            if sort not in self.model._meta.get_all_field_names():
                raise Http404("%s is not a valid sorting field" % sort)

        self.owner = get_object_or_404(User, username=self.kwargs.get("owner"))
        owner_lookup = dict([(self.owner_field, self.owner)])
        list = self.model.objects.filter(**owner_lookup)

        if self.permission:
            f = PermissionsRegistry.get_filter(self.permission,
                                               self.request.user)
            list = list.filter(f)

        if self.related:
            list = list.select_related(*self.related)

        if self.defer:
            list = list.defer(*self.defer)
        if sort:
            dir = vars.get('dir', "desc")
            order_by = (dir == "desc" and "-" or "") + sort
            list = list.order_by(order_by)

        return list

    def get_context_data(self, **kwargs):
        kwargs = super(OwnerListView, self).get_context_data(**kwargs)
        kwargs["owner"] = self.owner
        kwargs["user"] = self.request.user
        p = self.request.GET
        kwargs["sort"] = p.get('sort', None)
        kwargs["dir"] = p.get('dir', "desc")
        return kwargs
