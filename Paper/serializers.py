from rest_framework import serializers
from Paper.models import Journal, ReviewType, Country, ProductType, Frequency, Category,\
    Publisher, Article, Submit, Order, Author, Status, Requirement, UploadFile, OrderStatusLog


class FrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Frequency
        fields = [
            'id',
            'name',
            'description',
        ]


class ReviewTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewType
        fields = [
            'id',
            'name',
            'json',
        ]


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = [
            'id',
            'name',
            'description',
        ]


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = [
            'id',
            'name',
            'iso',
            'nice_name',
            'num_code',
        ]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
        ]


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = [
            'id',
            'name',
            'name_translate',
            'description',
            'description_translate',
            'logo_url',
            'site_address',
        ]


class JournalSerializer(serializers.ModelSerializer):
    review_type = ReviewTypeSerializer(read_only=True)
    countries = CountrySerializer(many=True, required=False)
    frequency = FrequencySerializer(read_only=True)
    categories = CategorySerializer(many=True, required=False)
    products = ProductTypeSerializer(many=True, required=False)
    publisher = PublisherSerializer(read_only=True, required=False)

    class Meta:
        model = Journal
        fields = [
            'id',
            'name',
            'description',
            'logo_url',
            'issn',
            'eissn',
            'review_type',
            'guide_url',
            'url',
            'start_year',
            'impact_factor',
            'open_access',
            'flag',
            'countries',
            'frequency',
            'categories',
            'products',
            'publisher'
        ]


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = [
            'id',
            'name',
            'description',
        ]


class AuthorSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField(read_only=True)
    email = serializers.EmailField()

    class Meta:
        model = Author
        fields = [
            'first_name',
            'last_name',
            'position',
            'reason',
            'email',
            'appellation',
            'type',
            'country',
        ]


class UploadFileSerializer(serializers.ModelSerializer):
    requirement = serializers.StringRelatedField()

    class Meta:
        model = UploadFile
        fields = [
            'id',
            'requirement',
            'file',
            'name'
        ]


class SubmitSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    contactor = serializers.StringRelatedField(read_only=True)
    article = serializers.StringRelatedField(read_only=True)
    abstract = serializers.CharField(required=True)
    keywords = serializers.CharField(required=True)
    journal = serializers.StringRelatedField(read_only=True)
    authors = AuthorSerializer(source='get_authors',  read_only=True, many=True)
    upload_files = UploadFileSerializer(source='get_upload_files',  read_only=True, many=True)
    status = serializers.StringRelatedField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    def get_message(self, obj):
        try:
            order = obj.set_order()
            return OrderStatusLog.objects.filter(status=obj.status, order=order).first().message

        except Exception as e:
            return ''

    class Meta:
        model = Submit
        fields = [
            'id',
            'user',
            'article',
            'title',
            'abstract',
            'keywords',
            'major',
            'journal',
            'contactor',
            'authors',
            'upload_files',
            'status',
            'message'
        ]


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'id',
        ]


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = [
            'id',
            'name',
        ]


class RequirementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requirement
        fields = [
            'id',
            'name',
        ]

