from django.db import models


class Dish(models.Model):
    UNDEFINED = 0
    MAIN = 1
    SIDE = 2
    SNACK = 3

    DISH_TYPE = (
        (UNDEFINED, '미정'),
        (MAIN, '주식'),
        (SIDE, '부식'),
        (SNACK, '간식'),
    )

    name = models.CharField(max_length=20, help_text='dish 이름, 타입과 같은 것을 사용해주세요')
    code = models.IntegerField(choices=DISH_TYPE, unique=True)

    class Meta:
        db_table = "food_dish"


class FoodCompany(models.Model):
    code = models.IntegerField(unique=True, null=True)
    name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.code}: {self.name}'

    class Meta:
        db_table = "food_foodcompany"


class FoodBrand(models.Model):
    code = models.IntegerField(unique=True, null=True)
    name = models.CharField(max_length=20, unique=True)
    company = models.ForeignKey(FoodCompany, related_name='brands', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.code}: {self.name}'

    class Meta:
        db_table = "food_foodbrand"


class FoodGroup(models.Model):
    UNDEFINED = 0
    CARBOHYDRATE_GROUP_ONE = 1
    CARBOHYDRATE_GROUP_TWO = 2
    PROTEIN_GROUP_ONE = 3
    PROTEIN_GROUP_TWO = 4
    CARBOHYDRATE_PROTEIN_COMPLEX_GROUP = 5
    FIBER_GROUP = 6
    ETC_GROUP_ONE = 7
    ETC_GROUP_TWO = 8

    GROUP_TYPES = (
        (UNDEFINED, '미정'),
        (CARBOHYDRATE_GROUP_ONE, '탄수화물1군'),
        (CARBOHYDRATE_GROUP_TWO, '탄수화물2군'),
        (PROTEIN_GROUP_ONE, '단백질1군'),
        (PROTEIN_GROUP_TWO, '단백질2군'),
        (CARBOHYDRATE_PROTEIN_COMPLEX_GROUP, '탄단군'),
        (FIBER_GROUP, '식이섬유군'),
        (ETC_GROUP_ONE, '기타1군'),
        (ETC_GROUP_TWO, '기타2군')
    )

    name = models.CharField(max_length=20, help_text='그룹 이름, 타입과 같은 것을 사용해주세요')
    code = models.IntegerField(choices=GROUP_TYPES, unique=True)

    class Meta:
        db_table = "food_foodgroup"


class StorageMethod(models.Model):
    FROZEN = 0  # 냉동 -18 이하
    REFRIGERATED = 1  # 냉장 0 ~ 10
    NORMAL_TEMPERATURE = 2  # 상온 : 15 ~ 25
    ROOM_TEMPERATURE = 3  # 실온 : 1 ~ 35
    STORAGE_METHOD = (
        (FROZEN, '냉동'),
        (REFRIGERATED, '냉장'),
        (NORMAL_TEMPERATURE, '상온'),
        (ROOM_TEMPERATURE, '실온'),

    )

    code = models.IntegerField(choices=STORAGE_METHOD, default=FROZEN)
    name = models.CharField(max_length=5)

    class Meta:
        db_table = "food_storagemethod"


class Food(models.Model):
    sku = models.CharField(max_length=20, help_text='재고관리코드', null=True, unique=True, default=None)
    name = models.CharField(max_length=50, help_text='제품명')
    dishes = models.ManyToManyField(Dish, related_name='foods')
    brand = models.ForeignKey(FoodBrand, null=True, blank=True, related_name='foods', on_delete=models.SET_NULL)
    group = models.ForeignKey(FoodGroup, blank=True, to_field='code', default=FoodGroup.UNDEFINED, related_name='foods',
                              on_delete=models.SET_DEFAULT)
    storage_method = models.ForeignKey(StorageMethod, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = "food_food"


class FoodProduct(models.Model):
    sku = models.CharField(max_length=20, help_text='재고관리코드', null=True, unique=True)
    food = models.ForeignKey(Food, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    unit_cost = models.IntegerField(null=True, default=None)
    price = models.IntegerField(null=True,
                                help_text='해당 필드는 변경을 해도 의미가 없습니다. 정해진 시간에 origin price와 pricelog를 확인하여 해당 필드가 자동으로 변합니다.')
    origin_price = models.IntegerField(null=True,
                                       help_text='static한 최초의 가격입니다. 해당 필드는 변경되어서는 안됩니다. 가격변화를 PriceLog에 생성해주시면, 정해진 시간에 price가 적용됩니다.')
    link = models.URLField(max_length=400, null=True)
    is_available = models.BooleanField(default=True)
    is_shown = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    barcode = models.CharField(max_length=30, default='', blank=True)

    new_product_until = models.DateTimeField(null=True, blank=True, default=None, help_text='언제까지 신상품이라는 태그를 가질 지')

    # todo: deprecated
    option_string = models.CharField(blank=True, default='', help_text='스크래퍼를 위한 필드', max_length=30)
    checked_at = models.DateTimeField(null=True, blank=True)

    feature_major = models.CharField(blank=True, default='', help_text='상세 정보를 위한 필드', max_length=500)
    feature_sub = models.CharField(blank=True, default='', max_length=1000)

    available_until = models.IntegerField(default=168)
    immediate_sold_out_started_at = models.DateTimeField(null=True, help_text='immediate sold out')
    immediate_sold_out_ended_at = models.DateTimeField(null=True, help_text='immediate sold out')

    @property
    def purchasable(self) -> bool:
        return self.is_approved and self.is_shown and self.is_available

    class Meta:
        db_table = "food_foodproduct"


class FoodProductSKU(models.Model):
    code = models.IntegerField(unique=True)
    food_product = models.OneToOneField(
        FoodProduct, on_delete=models.SET_NULL,
        related_name='sku_relation', null=True, default=None
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "food_foodproductsku"


class ProductExceptDay(models.Model):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6
    DAYS = (
        (MONDAY, '월'),
        (TUESDAY, '화'),
        (WEDNESDAY, '수'),
        (THURSDAY, '목'),
        (FRIDAY, '금'),
        (SATURDAY, '토'),
        (SUNDAY, '일'),
    )

    day = models.IntegerField(choices=DAYS, unique=True)
    products = models.ManyToManyField(FoodProduct, related_name='except_days')

    class Meta:
        db_table = "food_productexceptday"


def product_image_path(instance, filename):
    return 'spark/product/{}_{}/{}'.format(instance.product.food.sku, instance.product.name, filename)


class ProductImage(models.Model):
    product = models.ForeignKey(FoodProduct, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_path)
    code = models.IntegerField(default=100)
    code_index = models.IntegerField(default=0)

    class Meta:
        ordering = ['code', 'code_index']
        db_table = 'food_productimage'



class PriceLog(models.Model):
    BULK_CHANGE = 1
    SHIPDAN_CHANGE = 2
    SELLER_CHANGE = 3

    food_product = models.ForeignKey(FoodProduct, related_name='price_logs', on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(null=True, default=None,
                                help_text='해당 필드는 어드민에서 변경하면 안됩니다. 변경 시, 시스템에 큰 혼란이 오게 됩니다. (사실, log가 사라지는 거지, 문제가 되진 않지만 여튼 변경하거나 삭제하면 안됨!)')
    code = models.IntegerField(null=True)
    content = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "food_pricelog"


class UnitCostLog(models.Model):
    BULK_CHANGE = 1
    SHIPDAN_CHANGE = 2
    SELLER_CHANGE = 3

    food_product = models.ForeignKey(FoodProduct, related_name='unit_cost_logs', on_delete=models.SET_NULL, null=True)
    unit_cost = models.IntegerField(null=True, default=None,
                                    help_text='해당 필드는 어드민에서 변경하면 안됩니다. 변경 시, 시스템에 큰 혼란이 오게 됩니다. (사실, log가 사라지는 거지, 문제가 되진 않지만 여튼 변경하거나 삭제하면 안됨!)')
    code = models.IntegerField(null=True)
    content = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "food_unitcostlog"


class FirstCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "food_firstcategory"


class SecondCategory(models.Model):
    name = models.CharField(max_length=20)
    upper = models.ForeignKey(FirstCategory, on_delete=models.CASCADE, related_name='lowers')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'upper'], name='second category name and upper unique')
        ]
        db_table = 'food_secondcategory'


class ThirdCategory(models.Model):
    name = models.CharField(max_length=20)
    code = models.IntegerField(unique=True, null=True, default=None)
    upper = models.ForeignKey(SecondCategory, on_delete=models.CASCADE, related_name='lowers')
    food = models.ManyToManyField(Food, related_name='categories')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'upper'], name='third category name and upper unique')
        ]
        db_table = 'food_thirdcategory'


class FoodMajorClassification(models.Model):
    name = models.CharField(max_length=30)
    code = models.IntegerField(unique=True, null=True, default=None)

    class Meta:
        db_table = "food_foodmajorclassification"


class FoodSubClassification(models.Model):
    name = models.CharField(max_length=30)
    code = models.IntegerField(unique=True, null=True, default=None)
    upper = models.ForeignKey(FoodMajorClassification, on_delete=models.CASCADE, related_name='lowers')
    foods = models.ManyToManyField(Food, related_name='sub_classifications')

    class Meta:
        db_table = "food_foodsubclassification"


def major_search_category_image_path(instance, filename):
    return 'spark/search_category/{}'.format(filename)


class FoodMajorSearchCategory(models.Model):
    name = models.CharField(max_length=40)
    code = models.IntegerField(unique=True, null=True, default=None)
    order = models.IntegerField(unique=True, null=True, default=None)
    img = models.ImageField(upload_to=major_search_category_image_path, null=True, default=None)
    is_representative = models.BooleanField(default=True)

    class Meta:
        db_table = "food_foodmajorsearchcategory"


class FoodSubSearchCategory(models.Model):
    name = models.CharField(max_length=40)
    code = models.IntegerField(unique=True, null=True, default=None)
    upper = models.ForeignKey(FoodMajorSearchCategory, on_delete=models.CASCADE, related_name='lowers')
    foods = models.ManyToManyField(Food, related_name='sub_search_categories')

    class Meta:
        db_table = "food_foodsubsearchcategory"


class NutrientMeta(models.Model):
    calorie = models.FloatField(help_text='100g 기준 칼로리', null=True, blank=True)
    carbohydrate = models.FloatField(help_text='100g 기준 탄수화물', null=True, blank=True)
    protein = models.FloatField(help_text='100g 기준 단백질', null=True, blank=True)
    fat = models.FloatField(help_text='100g 기준 지방', null=True, blank=True)
    sugar = models.FloatField(help_text='100g 기준 당류', null=True, blank=True)
    sodium = models.FloatField(help_text='100g 기준 나트륨, mg으로 넣어주세요', null=True, blank=True)
    fiber = models.FloatField(help_text='100g 기준 식이섬유', null=True, blank=True)
    saturated_fat = models.FloatField(help_text='100g 기준 포화지방', null=True, blank=True)
    trans_fat = models.FloatField(help_text='100g 기준 트랜스지방', null=True, blank=True)
    cholesterol = models.FloatField(help_text='100g 기준 콜레스테롤', null=True, blank=True)
    proper_gram = models.FloatField(null=True, help_text='한끼 그람 수')

    class Meta:
        abstract = True


class Nutrient(NutrientMeta, models.Model):
    food = models.OneToOneField(Food, on_delete=models.CASCADE, related_name='nutrient')

    class Meta:
        db_table = "food_nutrient"

class UnitMeta(models.Model):
    UNDEFINED = 0
    COUNT = 1
    PIECE = 2
    PER_SERVING = 3
    CAN = 4
    PACK = 5
    PO = 6
    CUP = 7
    AL = 8
    SPOON = 9

    COUNT_UNIT_TYPE = (
        (UNDEFINED, '미정'),
        (COUNT, '개'),
        (PER_SERVING, '인분'),
        (PIECE, '조각'),
        (CAN, '캔'),
        (PACK, '팩'),
        (PO, '포'),
        (CUP, '컵'),
        (AL, '알'),
        (SPOON, '스푼'),
    )

    GRAM = 1
    MILLILITER = 2

    GRAM_UNIT_TYPE = (
        (GRAM, 'g'),
        (MILLILITER, 'ml')
    )

    priority = models.IntegerField(default=1, help_text='낮을 수록 높은 우선 순위')
    total_gram = models.FloatField(help_text='총 그람 수', null=True)
    unit_gram = models.FloatField(help_text='유닛 그람 수', null=True, default=None)
    total_count = models.IntegerField(help_text='총 개수', null=True)
    count_unit = models.IntegerField(choices=COUNT_UNIT_TYPE, help_text='개, 몇인분, 조각 등과 같은 단위', null=True)
    gram_unit = models.IntegerField(choices=GRAM_UNIT_TYPE, default=GRAM, help_text='g, ml')

    class Meta:
        abstract = True


class Unit(UnitMeta, models.Model):
    food_product = models.ForeignKey(FoodProduct, on_delete=models.CASCADE, related_name='units')

    class Meta:
        db_table = "food_unit"


class CookWay(models.Model):
    UNDEFINED = 0
    NO_COOK = 1  # 즉석 섭취식품 및 신선편의식품
    EASY_COOK = 2  # 전자레인지랑 불을 사용해서 손쉽게 데우기 가능(10분이내)
    HARD_COOK = 3  # 전자레인지랑 불을 사용해서 일종의 손질이 들어감(10분초과)
    RAW_COOK = 4  # 원재료

    EAT_WAYS = (
        (UNDEFINED, '미정'),
        (NO_COOK, '즉석섭취식품'),
        (EASY_COOK, '간편조리식품'),
        (HARD_COOK, '간편하지않은조리식품'),
        (RAW_COOK, '원재료'),
    )

    code = models.IntegerField(unique=True)
    foods = models.ManyToManyField(Food, related_name='cook_ways')

    class Meta:
        db_table = "food_cookway"

