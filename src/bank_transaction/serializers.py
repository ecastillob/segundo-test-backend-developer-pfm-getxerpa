from rest_framework import serializers

from .models import Category, Keyword, Merchant, Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "type"]

    def __init__(self, *args, **kwargs):
        edit = kwargs.pop("edit") if "edit" in kwargs else False
        super().__init__(*args, **kwargs)
        if edit:
            self.fields.pop("id")


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ["id", "merchant_name", "merchant_logo"]

    def __init__(self, *args, **kwargs):
        self.category_id = None
        edit = kwargs.pop("edit") if "edit" in kwargs else False
        data = kwargs.get("data", None)
        if data:
            self.category_id = data.get("category", None)
        super().__init__(*args, **kwargs)
        if edit:
            self.fields.pop("id")
            self.fields.pop("merchant_name")

    def validate(self, data):
        if self.category_id:
            if not Category.objects.filter(id=self.category_id).exists():
                raise serializers.ValidationError("No existe la categoría")
            if Merchant.objects.filter(merchant_name=data["merchant_name"], category_id=self.category_id).exists():
                raise serializers.ValidationError(
                    f"Ya existe el mercado {data['merchant_name']} "
                    f"que está asociado la categoría {self.category_id}"
                )
            data["category_id"] = self.category_id
        return data


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        exclude = []


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = []


class TransactionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ["merchant", "category"]


class TransactionBulkSerializer(serializers.Serializer):
    transactions = TransactionSimpleSerializer(many=True)

    def process_category(self, amount: float, category: Category, category_type: str):
        if amount < 0 and category.type == category_type:
            return category.id
        if amount >= 0 and category.type == category_type:
            return category.id
        return None

    def process_1_item(self, validated_data: dict) -> dict:
        category_id = None
        if validated_data.get("amount", None) is None:
            raise serializers.ValidationError("amount is invalid or empty")
        category_type = "expense" if validated_data["amount"] < 0 else "income"
        validated_data.update({"merchant_id": None, "category_id": category_id})
        description = validated_data["description"].lower()
        keyword_queryset = Keyword.objects.filter(keyword__iexact=description)
        if keyword_queryset:
            keyword_instance = keyword_queryset[0]
            validated_data["merchant_id"] = keyword_instance.merchant_id
            category_id = self.process_category(
                amount=validated_data["amount"],
                category=keyword_instance.merchant.category,
                category_type=category_type,
            )
        if not validated_data["merchant_id"]:
            merchant_queryset = Merchant.objects.filter(merchant_name__iexact=description)
            if merchant_queryset:
                merchant = merchant_queryset[0]
                validated_data["merchant_id"] = merchant.id
                category_id = self.process_category(
                    amount=validated_data["amount"],
                    category=merchant.category,
                    category_type=category_type,
                )
        if not category_id:
            category_queryset = Category.objects.filter(name__iexact=description, type=category_type)
            if category_queryset:
                category_id = category_queryset[0].id
        validated_data["category_id"] = category_id
        return validated_data

    def create(self, validated_data):
        category_counter = 0
        merchant_counter = 0
        instances = []
        for item in validated_data["transactions"]:
            new_item = self.process_1_item(item)
            if new_item["category_id"]:
                category_counter += 1
            if new_item["merchant_id"]:
                merchant_counter += 1
            instances.append(Transaction(**new_item))
        saved_instances = Transaction.objects.bulk_create(instances)
        total = len(saved_instances)
        return {
            "categorization_rate": round(100 * category_counter / total, 2),
            "merchant_rate": round(100 * merchant_counter / total, 2),
            "total_transactions": total,
        }


class TransactionResponseSerializer(serializers.Serializer):
    categorization_rate = serializers.FloatField()
    merchant_rate = serializers.FloatField()
    total_transactions = serializers.FloatField()
