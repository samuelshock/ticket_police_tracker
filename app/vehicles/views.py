"""
Main views for Vehicles APIs.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from vehicles.serializers import CreateTicketSerializer, ReportTicketSerializer
from core.models import Vehicle, Ticket
from core.permissions import IsPolice


User = get_user_model()


class TicketCreateView(GenericAPIView):
    serializer_class = CreateTicketSerializer
    permission_classes = (IsAuthenticated, IsPolice,)

    def post(self, request, *args, **kwargs):
        serializer = CreateTicketSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {"message": "Ticket created successfully."},
                    status=status.HTTP_201_CREATED)
            except Vehicle.DoesNotExist:
                msg = 'Vehicle with this license plate does not exist.'
                return Response(
                    {
                        'message': msg
                    },
                    status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportTicketView(GenericAPIView):
    """View for user report tickets."""
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email', None)
        if email is None:
            return Response({'message': 'Email parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        tickets = Ticket.objects.filter(car__owner=user)
        serializer = ReportTicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
