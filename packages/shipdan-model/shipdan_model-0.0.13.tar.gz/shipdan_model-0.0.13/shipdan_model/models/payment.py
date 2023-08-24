import datetime

from django.db import models

from shipdan_model.utils.time import KST


class Order(models.Model):
    PG = 1

    ORDER_TYPES = {
        (PG, 'PG')
    }
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders')
    order_type = models.IntegerField(choices=ORDER_TYPES, default=1, help_text="결제 방법")
    merchant_uid = models.CharField(max_length=30, null=True, default=None, blank=True, unique=True)
    imp_uid = models.CharField(max_length=100, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(null=True)
    deadline = models.DateTimeField(default=datetime.datetime(2099, 12, 31, tzinfo=KST), help_text='주문마감시간')

    class Meta:
        db_table = 'payment_order'


class OrderPaymentNoti(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='noti', null=True)
    is_noti = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_orderpaymentnoti'


class IamportCustomerUid(models.Model):
    """
    .. Note::
        -

    """
    user = models.ForeignKey('accounts.User', related_name='customer_uids', on_delete=models.CASCADE)
    customer_uid = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'iamport_customeruid'

    def __str__(self):
        return self.customer_uid


class IamportOrder(models.Model):
    """
    .. Note::
        - Iamport 주문기록을 저장합니다.
        - imp_uid: 주문이 정상적으로 완료된 경우 Iamport 에서 넘겨주는 imp_uid 를 저장합니다.
        - is_canceled: 주문이 취소된 경우 True 아닌 경우 False 입니다.

    """
    UNPAID = 0
    PAID = 1
    CANCELED = -1
    FAILURE = -20

    PAY_STATUS = (
        (UNPAID, '미결제'),
        (PAID, '결제완료'),
        (CANCELED, '결제취소'),
        (FAILURE, '결제실패')
    )

    user = models.ForeignKey('accounts.User', related_name='iamport_orders', on_delete=models.CASCADE)
    customer_uid = models.ForeignKey(IamportCustomerUid, null=True, related_name='orders',
                                     on_delete=models.CASCADE)

    price = models.IntegerField()
    imp_uid = models.CharField(max_length=100, default=None, null=True, unique=True, )
    merchant_uid = models.CharField(max_length=100)

    status = models.IntegerField(choices=PAY_STATUS, default=0)
    status_description = models.TextField(default='', blank=True)
    name = models.TextField(verbose_name='주문명')

    is_canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_iamportorder'


class IamportWebhookLog(models.Model):
    STATUS_READY = 1
    STATUS_PAID = 2
    STATUS_CANCELLED = 3
    STATUS_FAILURE = 4

    STATUS_CHOICES = (
        (STATUS_READY, '가상계좌발급완료'),
        (STATUS_PAID, '결제완료'),
        (STATUS_CANCELLED, '결제취소'),
        (STATUS_FAILURE, '결제실패')
    )

    STATUS_MAP = {
        STATUS_READY: '가상계좌발급완료',
        STATUS_PAID: '결제완료',
        STATUS_CANCELLED: '결제취소',
        STATUS_FAILURE: '결제실패'
    }

    STATUS_TEXT_MAP = {
        'ready': STATUS_READY,
        'paid': STATUS_PAID,
        'cancelled': STATUS_CANCELLED,
        'failed': STATUS_FAILURE,
    }

    iamport_order = models.ForeignKey(IamportOrder, related_name='logs', on_delete=models.CASCADE)
    receipt = models.JSONField(default=dict)
    status = models.IntegerField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment_iamportwebhooklog'


class IamportCancelLog(models.Model):
    iamport_order = models.ForeignKey(IamportOrder, related_name='cancel_log', on_delete=models.CASCADE)
    response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment_iamportcancellog'


class IamportScheduleLog(models.Model):
    """
    .. Note::
        - Iamport 스케쥴 예약시 남는 로그입니다.
    """
    order = models.OneToOneField(IamportOrder, related_name='schedule', on_delete=models.CASCADE)
    schedule_at = models.FloatField(max_length=60)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_iamportschedulelog'


