from django.db import models
from Account.models import TimeStampMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from Paper.helper import publisher_logo_path, journal_resource_path, submit_upload_path


# Create your models here.
class ReviewType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    json = models.JSONField(null=True)
    description = models.TextField(null=True)


class Category(models.Model):
    name = models.CharField(max_length=12, unique=True)
    description = models.CharField(max_length=255)


class Country(models.Model):
    iso = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=80, unique=True)
    nice_name = models.CharField(max_length=80)
    iso3 = models.CharField(max_length=3, null=True)
    num_code = models.IntegerField(null=True)
    phone_code = models.SmallIntegerField(null=True)


class Frequency(models.Model):
    name = models.CharField(max_length=12)
    description = models.CharField(max_length=255)


class ProductType(models.Model):
    name = models.CharField(max_length=12)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Publisher(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True)
    name_translate = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    description_translate = models.TextField(null=True)
    logo_url = models.ImageField(upload_to=publisher_logo_path, null=True)
    site_address = models.URLField(null=True)

    def __str__(self):
        return self.name_translate


class JournalCategory(models.Model):
    journal = models.ForeignKey('Journal', on_delete=models.CASCADE, related_name='journal_category')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_journal')


class JournalCountry(models.Model):
    journal = models.ForeignKey('Journal', on_delete=models.CASCADE, related_name='journal_country')
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='country_journal')


class JournalProductType(models.Model):
    journal = models.ForeignKey('Journal', on_delete=models.CASCADE, related_name='journal_product')
    product = models.ForeignKey('ProductType', on_delete=models.CASCADE, related_name='product_journal')


class Journal(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    logo_url = models.ImageField(null=True, upload_to=journal_resource_path)
    issn = models.CharField(max_length=255, null=True)
    eissn = models.CharField(max_length=255, null=True)
    review_type = models.ForeignKey(ReviewType, on_delete=models.DO_NOTHING, related_name='journal_review_method',  null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.DO_NOTHING, related_name='journal_publisher', null=True)
    frequency = models.ForeignKey(Frequency, on_delete=models.DO_NOTHING, related_name='journal_frequency', null=True)
    guide_url = models.FileField(null=True, upload_to=journal_resource_path)
    url = models.URLField(null=True)
    start_year = models.SmallIntegerField(default=1990)
    impact_factor = models.FloatField(default=0.0)
    open_access = models.IntegerField(null=True)
    flag = models.BooleanField(default=False)
    issues_per_year = models.SmallIntegerField(null=True)
    countries = models.ManyToManyField(
        Country,
        through='JournalCountry',
        through_fields=('journal', 'country'),
        blank=True,
    )

    products = models.ManyToManyField(
        ProductType,
        through='JournalProductType',
        through_fields=('journal', 'product'),
        blank=True,
    )

    categories = models.ManyToManyField(
        Category,
        through='JournalCategory',
        through_fields=('journal', 'category'),
        blank=True,
    )

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")

    def __str__(self):
        return self.name

    def assign_category(self, categories, is_update=True):
        self.categories.clear() if is_update else ''
        for category in categories:
            try:
                category = Category.objects.get(pk=category)
                if not self.categories.filter(pk=category.pk).exists():
                    self.categories.add(category)
            except Category.DoesNotExist:
                pass
        return True

    def assign_product(self, products, is_update=True):
        self.products.clear() if is_update else ''
        for product in products:
            try:
                product = ProductType.objects.get(pk=product)
                if not self.products.filter(pk=product.pk).exists():
                    self.products.add(product)
            except ProductType.DoesNotExist:
                pass
        return True

    def assign_country(self, countries, is_update=True):
        self.countries.clear() if is_update else ''
        for country in countries:
            try:
                country = Country.objects.get(pk=country)
                if not self.countries.filter(pk=country.pk).exists():
                    self.countries.add(country)
            except Country.DoesNotExist:
                pass
        return True


class Status(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)


class Requirement(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    file_type = models.CharField(max_length=192, null=True)


class Order(TimeStampMixin):
    type = models.ForeignKey('Account.BusinessType', on_delete=models.DO_NOTHING, related_name='order_type')
    user = models.ForeignKey('Account.User', on_delete=models.DO_NOTHING, related_name='order_user')
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='order_status', null=True)
    product = GenericForeignKey()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    status_logs = models.ManyToManyField(
        Status,
        through='OrderStatusLog',
        through_fields=('order', 'status'),
        blank=True,
    )


class OrderStatusLog(TimeStampMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)


class Submit(TimeStampMixin):
    order = GenericRelation(Order, related_query_name='order_submit')
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, related_name='submit_article', null=True)
    title = models.CharField(max_length=255, null=True)
    abstract = models.TextField(null=True)
    keywords = models.TextField(null=True)
    upload_files = models.JSONField(null=True)
    major = models.TextField(null=True)
    user = models.ForeignKey('Account.User', on_delete=models.DO_NOTHING, related_name='submit_user')
    journal = models.ForeignKey(Journal, on_delete=models.DO_NOTHING, related_name='submit_journal', null=True)


class UploadFile(TimeStampMixin):
    name = models.CharField(max_length=255)
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name='submit_upload_paper_type')
    submit = models.ForeignKey(Submit, on_delete=models.CASCADE, related_name='submit_uploaded_paper')
    file = models.FileField(upload_to=submit_upload_path)


class Resource(TimeStampMixin):
    order = GenericRelation(Order, related_query_name='order_resource')
    is_download = models.BooleanField(default=True)
    file_lists = models.JSONField(null=True)


class Author(TimeStampMixin):

    class Appellation(models.TextChoices):
        DOCTOR = 'Dr', _('Doctor')
        MR = 'Mr', _('Mr')
        MRS = 'Mrs', _('Mrs')
        MISS = 'Miss', _('Miss')
        PROFESSOR = 'Professor', _('professor')

    class AuthorType(models.TextChoices):
        AUTHOR = 'author', _('Author')
        REVIEWER = 'reviewer', _('Reviewer')

    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    position = models.CharField(max_length=255, null=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True)
    reason = models.CharField(max_length=255, null=True)
    submit = models.ForeignKey(Submit, on_delete=models.DO_NOTHING, related_name='submit_author')
    type = models.CharField(max_length=12, choices=AuthorType.choices, default=AuthorType.AUTHOR, )
    appellation = models.CharField(max_length=12,
                                   choices=Appellation.choices,
                                   default=Appellation.MR,)
