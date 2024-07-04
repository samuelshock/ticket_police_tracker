"""
Main views for Vehicles APIs.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from vehicles.serializers import CreateTicketSerializer
from core.models import Vehicle
from core.permissions import IsPolice


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
                        'detail': msg
                    },
                    status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
