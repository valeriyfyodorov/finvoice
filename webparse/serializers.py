from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Symbol, QuoteIndication

class SymbolSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    # if we need to edit a field that is a nested serializer,
    # we must override to_internal_value method
    def to_internal_value(self, data):
        return get_object_or_404(Symbol, pk=data['id'])

    class Meta:
        model = Symbol
        fields = (
            'id', 'ticket', 'name', 'updated_at'
        )
        datatables_always_serialize = ('id',)



class QuoteIndicationSerializer(serializers.ModelSerializer):
    symbol = SymbolSerializer()
    symbol_ticket = serializers.ReadOnlyField(source='symbol.ticket')
    symbol_name = serializers.ReadOnlyField(source='symbol.name')
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = QuoteIndication
        fields = (
            'id', 'symbol_name', 'symbol_ticket', 'price_open', 'price_close', 'price_low', 'price_high', 
            'price_last', 'price_previous', 'price_average', 'updated_at', 
            'symbol'
        )

