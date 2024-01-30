from rest_framework import serializers
from .models import ConstraintType, Constraint, ConstraintAssociation
from assets.models import Asset
from assets.serializers import AssetSerializer
from controls.models import Control
from controls.serializers import ControlSerializer

class ConstraintTypeSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()

    class Meta:
        model = ConstraintType
        fields = ('pk', 'name')

class ConstraintSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()
    constraint_type = ConstraintTypeSerializer()

    class Meta:
        model = Constraint 
        fields = ('pk', 'name', 'description', 'constraint_type', 'values')
        depth = 1
    
    def update(self, instance, validated_data):
        constraint_type_data = validated_data.pop('constraint_type')

        instance.name = validated_data["name"]
        instance.description = validated_data["description"]
        instance.constraint_type_id = ConstraintType.objects.get(pk=list(constraint_type_data.items())[0][1])
        instance.values = validated_data["values"]

        instance.save()
        # ... plus any other fields you may want to update
        return instance
    
    def create(self, validated_data):
        constraint_type_data = validated_data.pop('constraint_type')
        
        constraint_type = ConstraintType.objects.get(pk=list(constraint_type_data.items())[0][1])
        constraint = Constraint.objects.create(constraint_type=constraint_type, **validated_data)
        
        return constraint
        # ... plus any other fields you may want to update

class ConstraintAssociationSerializer(serializers.ModelSerializer):
    constraint = ConstraintSerializer()
    asset = AssetSerializer(allow_null=True)
    control = ControlSerializer(allow_null=True)

    class Meta:
        model = ConstraintAssociation 
        fields = ('pk', 'name', 'constraint', 'selected_value', 'asset', 'control')
        depth = 1
    
    def update(self, instance, validated_data):
        constraint_data = validated_data.pop('constraint')
        asset_data = validated_data.pop('asset')
        control_data = validated_data.pop('control')

        instance.name = validated_data["name"]
        instance.selected_value = validated_data["selected_value"]
        instance.constraint_type_id = Constraint.objects.get(pk=list(constraint_data.items())[0][1])
        instance.asset_id = Asset.objects.get(pk=list(asset_data.items())[0][1])
        instance.control_id = Control.objects.get(pk=list(control_data.items())[0][1])

        instance.save()
        # ... plus any other fields you may want to update
        return instance
    
    def create(self, validated_data):
        constraint_data = validated_data.pop('constraint')
        asset_data = validated_data.pop('asset')
        control_data = validated_data.pop('control')
        
        constraint = Constraint.objects.get(pk=list(constraint_data.items())[0][1])
        if asset_data is not None:
            asset = Asset.objects.get(pk=list(asset_data.items())[0][1])
        else:
            asset = None
        
        if control_data is not None:
            control = Control.objects.get(pk=list(control_data.items())[0][1])
        else:
            control = None
            
        constraint_association = ConstraintAssociation.objects.create(constraint=constraint, asset=asset, control=control, **validated_data)
        
        return constraint_association
        # ... plus any other fields you may want to update