from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수입니다")
        email = self.normalize_email(email).lower()  # 전체 이메일 소문자 변환
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """확장된 사용자 모델"""
    
    class Gender(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"
    
    # 필수 필드
    email = models.EmailField(unique=True, verbose_name="이메일")
    name = models.CharField(max_length=150, blank=True, verbose_name="이름")
    
    # 확장 필드
    username = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="사용자명"
    )
    mobile_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^01[0-9]-\d{3,4}-\d{4}$",
                message="전화번호 형식은 010-1234-5678 이어야 합니다."
            )
        ],
        verbose_name="전화번호"
    )
    address1 = models.CharField(max_length=255, blank=True, verbose_name="주소1")
    address2 = models.CharField(max_length=255, blank=True, verbose_name="주소2")
    birthday = models.DateField(null=True, blank=True, verbose_name="생년월일")
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        blank=True,
        verbose_name="성별"
    )
    
    # 시스템 필드
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"

    def __str__(self):
        return self.email
