from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Restaurant, Menu, Vote
from .serializers import UserSerializer, RestaurantSerializer, MenuSerializer, VoteSerializer
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        today = timezone.now().date()
        return Menu.objects.filter(menu_date=today)

    @action(detail=False, methods=['get'], url_path='current')
    def get_current_day_menu(self, request):
        today = timezone.now().date()
        menus = Menu.objects.filter(menu_date=today)
        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='results')
    def get_current_day_results(self, request):
        today = timezone.now().date()
        menus = Menu.objects.filter(menu_date=today)
        results = []
        for menu in menus:
            votes = Vote.objects.filter(menu=menu).count()
            results.append({
                'menu': MenuSerializer(menu).data,
                'votes': votes
            })
        return Response(results)

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
