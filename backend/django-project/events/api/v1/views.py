# api/v1/events/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ...models import Category, Event
from .serializers import CategorySerializer, EventsSerializer
from .permisions import IsEventOwnerOrCreate,IsCategoryOwnerOrCreate
from ...tasks import send_event_email

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (IsCategoryOwnerOrCreate,)

    def get_queryset(self):
        return Category.objects.filter(creator=self.request.user).select_related("creator")


class EventViewSet(ModelViewSet):
    serializer_class = EventsSerializer
    permission_classes = (IsEventOwnerOrCreate,)

    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user).select_related("creator","category")
    
    def perform_create(self, serializer):
        event = serializer.save(creator=self.request.user)

        if event.send_email:
            result = send_event_email.apply_async(
                args=[event.id],
                eta=event.email_send_time
            )

            event.email_task_id = result.id
            event.save(update_fields=["email_task_id"])