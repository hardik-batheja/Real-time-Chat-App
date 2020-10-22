from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls', namespace='chat')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

 
        #if bytes_data:
        # cart = json.loads(self.scope['cookies']['cart'])
        # print(cart)
        
        #print(bytes_data)
        