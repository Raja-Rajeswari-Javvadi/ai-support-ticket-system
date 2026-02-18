from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count, Avg

from .models import Ticket
from .serializers import TicketSerializer
from .gemini_service import classify_ticket
from django.shortcuts import render

# -----------------------------
# CREATE TICKET (WITH AI SUPPORT)
# -----------------------------
class TicketCreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        title = request.data.get("title")
        description = request.data.get("description")
        category = request.data.get("category")
        priority = request.data.get("priority")
        status_value = request.data.get("status", "open")

        # 🔥 AUTO CLASSIFY if category/priority not given
        if not category or not priority:
            category_suggested, priority_suggested = classify_ticket(description)

            if category_suggested:
                category = category_suggested
            if priority_suggested:
                priority = priority_suggested

        serializer = self.get_serializer(data={
            "title": title,
            "description": description,
            "category": category,
            "priority": priority,
            "status": status_value
        })

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# -----------------------------
# LIST + FILTER + SEARCH
# -----------------------------
class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all().order_by('-created_at')

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        priority = self.request.query_params.get('priority')
        status_param = self.request.query_params.get('status')

        if category:
            queryset = queryset.filter(category=category)
        if priority:
            queryset = queryset.filter(priority=priority)
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset


# -----------------------------
# UPDATE TICKET
# -----------------------------
class TicketUpdateView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


# -----------------------------
# STATS ENDPOINT
# -----------------------------
class TicketStatsView(generics.GenericAPIView):

    def get(self, request):
        total_tickets = Ticket.objects.count()
        open_tickets = Ticket.objects.filter(status='open').count()

        avg_tickets_per_day = Ticket.objects.extra(
            {'day': "date(created_at)"}
        ).values('day').annotate(count=Count('id')).aggregate(avg=Avg('count'))['avg']

        priority_breakdown = Ticket.objects.values('priority').annotate(count=Count('id'))
        category_breakdown = Ticket.objects.values('category').annotate(count=Count('id'))

        return Response({
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "avg_tickets_per_day": avg_tickets_per_day,
            "priority_breakdown": {item['priority']: item['count'] for item in priority_breakdown},
            "category_breakdown": {item['category']: item['count'] for item in category_breakdown},
        })


# -----------------------------
# CLASSIFY ONLY ENDPOINT
# -----------------------------
@api_view(['POST'])
def classify_ticket_view(request):
    description = request.data.get("description")

    if not description:
        return Response({"error": "Description is required"}, status=400)

    category, priority = classify_ticket(description)

    return Response({
        "suggested_category": category,
        "suggested_priority": priority
    })
def home(request):
    return render(request, "index.html")