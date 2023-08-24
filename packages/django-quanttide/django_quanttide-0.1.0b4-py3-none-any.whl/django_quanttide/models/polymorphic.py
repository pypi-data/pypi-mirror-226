from polymorphic.models import PolymorphicModel as BasePolymorphicModel

from django_quanttide.models import IDField, CreatedAtField, UpdatedAtField


class PolymorphicModel(BasePolymorphicModel):
    """
    多态数据模型

    类型字段映射表（TYPE_FIELD_MAPPINGS）是一个键值对字典，用于将模型名称（即 ContentType 表的 model 值）映射到用户定义的类型值。
    如果需要使用类型字段映射表，请在子类中覆盖 TYPE_FIELD_MAPPINGS 属性。

    示例：

    ```
    class Project(PolymorphicModel):
        pass
    ```
    """
    id = IDField()

    class Meta:
        abstract = True

    @property
    def type(self) -> str:
        """
        类型字段

        默认返回值为模型名称的小写形式，比如`parentmodel`、`childmodel`。

        :return: 类型值
        """
        # 类名转小写，方便和ContentType.model字段对应
        return self.polymorphic_ctype.model
