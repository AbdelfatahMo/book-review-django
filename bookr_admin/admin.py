
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import URLResolver, path
# from django.contrib.auth.models import User

# Register your models here.


class BookrAdmin(admin.AdminSite):
    site_header = "Bookr Administration"
    logout_template = "admin/logout.html"

    def system_health_dashboard(self, request):
        request.current_app = self.name
        context = self.each_context(request)
        return TemplateResponse(request, "admin/admin_profile.html", context)

    def profile_view(self, request):
        # get the name of the current application and set that in the request context
        request.current_app = self.name
        # fetch the template variables, which are required to render the contents,
        # such as site_title, site_header, and more, in the admin templates
        # each_context() method of the AdminSite class,
        # which provides the dictionary of the admin site template variables from the class
        context = self.each_context(request)
        return TemplateResponse(request, "admin/admin_profile.html", context)

    def get_urls(self):
        return [path("admin_profile/",
                     self.admin_view(self.profile_view), name="admin profile"),
                path("dashboard/", 
                     self.admin_view(self.system_health_dashboard), name="dashboard"),
                ] + super().get_urls()


# admin_site=BookrAdmin('bookr_admin')
# admin_site.register(User)
