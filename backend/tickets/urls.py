from django.urls import path
from .views import TicketCreateView, TicketListView, TicketUpdateView, TicketStatsView
from .views import classify_ticket_view

urlpatterns = [
    path('tickets/', TicketCreateView.as_view()),
    path('tickets/list/', TicketListView.as_view()),
    path('tickets/<int:pk>/', TicketUpdateView.as_view()),
    path('tickets/stats/', TicketStatsView.as_view()),
    path('tickets/classify/', classify_ticket_view),
]
