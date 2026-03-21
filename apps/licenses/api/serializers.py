from rest_framework import serializers

class LicenseVerificationSerializer(serializers.Serializer):
    license_key = serializers.CharField(max_length=50, required=True)
    domain = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    ip_address = serializers.IPAddressField(required=False, allow_blank=True, allow_null=True)
    hardware_id = serializers.CharField(max_length=255, required=True)
    device_name = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
