"""
Serializers for the Vehicles API view.
"""
from rest_framework import serializers
from core.models import Ticket, Vehicle


class CreateTicketSerializer(serializers.ModelSerializer):
    placa_patente = serializers.CharField(write_only=True)
    timestamp = serializers.DateTimeField(write_only=True)
    comentarios = serializers.CharField(source='description', write_only=True)

    class Meta:
        model = Ticket
        fields = ['placa_patente', 'timestamp', 'comentarios']

    def create(self, validated_data):
        placa_patente = validated_data.pop('placa_patente')
        try:
            car = Vehicle.objects.get(license_plate=placa_patente)
        except Vehicle.DoesNotExist:
            raise Vehicle.DoesNotExist(
                "Vehicle with this license plate does not exist.")

        # Assuming the user is a police officer
        police = self.context['request'].user.police_profile
        ticket = Ticket.objects.create(
            car=car,
            police=police,
            description=validated_data['description'],
            date=validated_data['timestamp']
        )
        return ticket
