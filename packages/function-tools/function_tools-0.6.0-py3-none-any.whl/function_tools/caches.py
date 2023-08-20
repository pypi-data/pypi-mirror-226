from collections import (
    Iterable,
    Sequence,
    defaultdict,
    namedtuple,
)
from copy import (
    deepcopy,
)
from datetime import (
    date,
)
from operator import (
    attrgetter,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)

from django.db.models import (
    Model,
    Q,
)

from function_tools.enums import (
    TransferPeriodEnum,
)
from function_tools.strings import (
    DATE_FROM_MORE_OR_EQUAL_DATE_TO_ERROR,
    SEARCHING_KEY_SIZE_LESS_THAN_DEFAULT_SEARCHING_KEY_ERROR,
    SEARCHING_KEY_SIZE_MORE_THAN_DEFAULT_SEARCHING_KEY_ERROR,
)
from function_tools.types import (
    QueryType,
)
from function_tools.utils import (
    date2str,
    deep_getattr,
)
from m3_db_utils.consts import (
    LOOKUP_SEP,
    PK,
)


class BaseCache:
    """
    Кеш-заглушка.
    """

    def __init__(self, *args, **kwargs):
        super().__init__()

        # Кеш подготовлен к работе
        self.__is_prepared = False

    @property
    def is_prepared(self) -> bool:
        """Кеш уже подготовлен."""
        return self.__is_prepared

    @is_prepared.setter
    def is_prepared(self, value: bool):
        """Отметка кеша о готовности."""
        self.__is_prepared = value

    def _before_prepare(self, *args, **kwargs):
        """Действия перед подготовкой кеша."""

    def _prepare(self, *args, **kwargs):
        """Заполнение кеша данными."""

    def _after_prepare(self, *args, **kwargs):
        """Действия после подготовки кеша."""

    def _check_cache_prepared(self):
        """Проверка, был ли подготовлен кеш ранее или нет."""
        if self.is_prepared:
            raise RuntimeError('Cache can not be prepared twice. Please check using method "prepare".')

    def prepare(self, *args, **kwargs):
        """"""
        self._check_cache_prepared()

        self._before_prepare(*args, **kwargs)
        self._prepare(*args, **kwargs)
        self._after_prepare(*args, **kwargs)

        self.is_prepared = True


class EntityCache(BaseCache):
    """Базовый класс кеша объектов сущности.

    Необходимо обратить внимание, что в only_fields нельзя передавать prefetch_related параметры, т.к. возникает ошибка.
    Вместо only_fields необходимо использовать values_fields.
    В приоритете использование only_fields, т.к. для values_fields требуется преобразование результата в виде словаря
    во вложенные объекты.
    """

    FILTER_FUNCTIONS = {
        'range': lambda r: lambda v: r[0] <= v <= r[1],
        'in': lambda r: lambda v: v in r,
        'eq': lambda r: lambda v: v == r,
    }

    def __init__(
        self,
        model: Type[Model],
        *args,
        select_related_fields: Optional[Tuple[str, ...]] = None,
        annotate_fields: Optional[Dict] = None,
        only_fields: Optional[Tuple[str, ...]] = None,
        values_fields: Optional[Tuple[str, ...]] = None,
        additional_filter_params: Optional[Union[Tuple[Union[Q, Dict[str, Any]]], Dict[str, Any]]] = None,
        exclude_params: Optional[Dict[str, Any]] = None,
        distinct: Optional[Union[bool, Tuple[str]]] = True,
        searching_key: Union[str, Tuple[str, ...]] = ('pk', ),
        is_force_fill_cache: bool = True,
        **kwargs,

    ):
        super().__init__(*args, **kwargs)

        self._model = model
        self._select_related_fields = select_related_fields
        self._annotate_fields = annotate_fields
        self._only_fields = only_fields
        self._values_fields = values_fields
        self._actual_entities_queryset = self._prepare_actual_entities_queryset()

        self._searching_key = (
            searching_key
            if (
                isinstance(searching_key, Iterable)
                and not isinstance(searching_key, str)
            )
            else (searching_key, )
        )

        self._additional_filter_params = (
            self._prepare_additional_filter_params(additional_filter_params)
            if additional_filter_params
            else ([], {})
        )
        self._exclude_params = exclude_params

        self._distinct = distinct

        self._is_force_fill_cache = is_force_fill_cache

        self._filters = {}
        self._is_filtered = False

        self._initial_entities = None
        self._filtered_entities = []

        self._initial_entities_hash_table = None

        if self._is_force_fill_cache:
            self.prepare(*args, **kwargs)

    def __repr__(self):
        return (
            f'<{self.__class__.__name__} @model="{self._model.__name__}" @searching_key="{self._searching_key}">'
        )

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        """Обеспечивает итерирование по кешу.

        Например, когда была применена фильтрация filter() можно сразу итерироваться по полученному кешу."""
        entities = self.all()

        for entity in entities:
            yield entity

    def _prepare_additional_filter_params(
        self,
        filter_params: Union[Tuple[Union[Q, Dict[str, Any]]], Dict[str, Any]],
    ) -> Tuple[List[Q], Dict[str, Any]]:
        """Подготовка параметров фильтрации.

        Args:
            filter_params: Параметры фильтрации задаваемые пользователем. Кортеж Q со словарем для именованных
                параметров, например, обозначение вхождения.
        """
        filter_args = []
        filter_kwargs = {}

        if isinstance(filter_params, dict):
            filter_kwargs = filter_params
        else:
            for param in filter_params:
                if isinstance(param, Q):
                    filter_args.append(param)
                elif isinstance(param, dict):
                    filter_kwargs.update(**param)
                else:
                    raise ValueError('Please, check `additional_filter_params`, incorrect value!')

        return filter_args, filter_kwargs

    def _before_prepare(self, *args, **kwargs):
        """
        Точка расширения перед подготовкой кеша
        """
        pass

    def _after_prepare(self, *args, **kwargs):
        """
        Точка расширения после подготовки кеша
        """
        pass

    def _prepare(self, *args, **kwargs):
        """
        Метод подготовки кеша
        """
        self._prepare_entities()
        self._prepare_entities_hash_table()

    def _prepare_entities(self):
        """
        Получение выборки объектов модели по указанными параметрам
        """
        self._initial_entities = self._actual_entities_queryset

        if self._additional_filter_params[0]:
            self._initial_entities = self._initial_entities.filter(*self._additional_filter_params[0])

        if self._additional_filter_params[1]:
            self._initial_entities = self._initial_entities.filter(**self._additional_filter_params[1])

        if self._annotate_fields:
            self._initial_entities = self._initial_entities.annotate(**self._annotate_fields)

        if self._exclude_params:
            self._initial_entities = self._initial_entities.exclude(**self._exclude_params)

        if self._only_fields:
            self._initial_entities = self._initial_entities.only(*self._only_fields)

        if self._values_fields:
            self._initial_entities = self._initial_entities.values(*self._values_fields)

        if self._distinct:
            if isinstance(self._distinct, Iterable):
                self._initial_entities = self._initial_entities.distinct(*self._distinct)
            else:
                self._initial_entities = self._initial_entities.distinct()

        if self._values_fields:
            self._update_values_fields()

            self._convert_values_to_objects()

    def _update_values_fields(self):
        """Обновление полей values_fields.

        Добавление идентификатора и pk в values_fields для корректной работы фильтрации.
        """
        id_field_name = self._model._meta.pk.name

        if (
            PK in self._searching_key
            or PK in self._values_fields
            or id_field_name in self._searching_key
            or id_field_name in self._values_fields
        ):
            additional_fields = []

            if PK not in self._values_fields:
                additional_fields.append(PK)

            if id_field_name not in self._values_fields:
                additional_fields.append(id_field_name)

            self._values_fields += tuple(additional_fields)

    def _build_object_classes(self, field_structure, field_name: str):
        """Формирует классы именованных кортежей для вложенных объектов."""
        if field_structure.get('fields'):
            name = f'{field_name.capitalize()}NamedTuple'

            entity_cls = namedtuple(name, field_structure['fields'].keys())

            field_structure['cls'] = entity_cls

            for field_name, field_value in field_structure['fields'].items():
                if field_value:
                    self._build_object_classes(
                        field_structure=field_value,
                        field_name=field_name,
                    )
        else:
            field_structure['cls'] = None

    def _prepare_field_structure(self) -> Dict[str, Dict[str, Dict]]:
        """Формирование структуры объектов и их полей в виде словаря."""
        field_structure = defaultdict(dict)

        for field in self._values_fields:
            field_items = field.split(LOOKUP_SEP)
            tmp_level = field_structure

            for field_item in field_items:
                if field_item not in tmp_level['fields']:
                    tmp_level['fields'][field_item] = defaultdict(dict)

                tmp_level = tmp_level['fields'][field_item]

        self._build_object_classes(
            field_structure=field_structure,
            field_name=self._model.__class__.__name__,
        )

        return field_structure

    def _build_entity_object(self, entity, field_structure, field_path=()):
        """Формирование объекта сущности из словаря."""
        field_values = {}

        for field_key, field_value in field_structure['fields'].items():
            if field_value:
                value = self._build_entity_object(
                    entity=entity,
                    field_structure=field_value,
                    field_path=(field_path + (field_key, )),
                )
            else:
                tmp_field_key = field_key

                if field_key == PK:
                    tmp_field_key = self._model._meta.pk.name

                tmp_field_key = f'{LOOKUP_SEP}'.join((field_path + (tmp_field_key, )))

                value = entity.get(tmp_field_key)

            field_values[field_key] = value

        entity_object = field_structure['cls'](**field_values)

        return entity_object

    def _convert_values_to_objects(self):
        """Преобразование словарей, полученных при помощи values() в структуру объектов для работы как с обычными QS."""
        field_structure = self._prepare_field_structure()

        tmp_entities = []

        for entity in self._initial_entities:
            entity_object = self._build_entity_object(
                entity=entity,
                field_structure=field_structure,
            )

            tmp_entities.append(entity_object)

        del self._initial_entities

        self._initial_entities = tmp_entities

    def _prepare_entities_hash_table(self):
        """Отвечает за построение хеш таблицы для дальнейшего поиска.

        В качестве ключа можно задавать строку - наименование поля или кортеж наименований полей.

        Если требуется доступ через внешний ключ, то необходимо использовать точку в качестве разделителей. Например,
        searching_key = tuple('account_id', 'supplier.code').
        """
        hash_table = {}

        key_items_count = len(self._searching_key)
        for entity in self._initial_entities:
            temp_hash_item = hash_table

            for index, key_item in enumerate(self._searching_key, start=1):
                key_item_value = deep_getattr(entity, key_item)

                if key_item_value is not None:
                    if index == key_items_count:
                        if key_item_value not in temp_hash_item:
                            temp_hash_item[key_item_value] = entity
                        else:
                            if isinstance(temp_hash_item[key_item_value], set):
                                temp_hash_item[key_item_value].add(
                                    entity
                                )
                            else:
                                temp_hash_item[key_item_value] = {
                                    temp_hash_item[key_item_value], entity
                                }
                    else:
                        if key_item_value not in temp_hash_item:
                            temp_hash_item[key_item_value] = {}

                        temp_hash_item = temp_hash_item[key_item_value]
                else:
                    break

        self._initial_entities_hash_table = hash_table

    def _prepare_actual_entities_queryset(self):
        """Подготовка менеджера с указанием идентификатора учреждения и состояния, если такие имеются у модели."""
        actual_entities_queryset = self._model._base_manager.all()

        if self._select_related_fields:
            actual_entities_queryset = actual_entities_queryset.select_related(
                *self._select_related_fields,
            )

        return actual_entities_queryset

    def _filter_entities(self, entities, filters):
        """Фильтрует сущности на основании применяемых фильтров."""
        self._filtered_entities = []

        if filters:
            for entity in entities:
                if all(
                    func_filter(deep_getattr(entity, attr)) for attr, func_filter in filters.items()
                ):
                    self._filtered_entities.append(entity)
        else:
            self._filtered_entities = entities

    def _check_is_iterable(self, object_):
        """Проверяет, является ли передаваемый объект итерабельным."""
        return (
            isinstance(object_, (Iterable, Sequence))
            and not isinstance(object_, str)
        )

    def clear_filter(self):
        """Сброс примененных фильтров и очистка кеша."""
        self._is_filtered = False
        self._filtered_entities = []
        self._filters = {}

    def all(self) -> Union[QueryType[Model], List[Model]]:
        """Возвращает список объектов либо QuerySet в зависимости от подхода к получению объектов."""
        return self._filtered_entities if self._is_filtered else self._initial_entities

    def first(self):
        """Получение первого элемента из кеша.

        Если ранее была наложена фильтрация, то значение будет получено из отфильтрованной выборки.
        """
        entities = self.all()

        first_entity = entities[0] if entities else None

        return first_entity

    def filter(self, **kwargs):
        """Установка фильтра для выборки данных.

        При повторном применении фильтра, ранее установленные параметры сбрасываются.

        Пример использования:
        some_objects_list = cache.filter(
            id__range=(1,10), elements_id__in=[1,2,3]
        ).values_list('id')
        some_objects_list => [1,5,6]

        some_objects_list = cache.filter(
            id__range=(1,10), elements_id__in=[1,2,3]
        ).values_list('id', 'elements_id')
        some_objects_list => [(1,1), (5,2), (6,3)]
        """
        self.clear_filter()

        for attr, value_filter in kwargs.items():
            lookup_attr = attr.split(LOOKUP_SEP)

            if lookup_attr[-1] in self.FILTER_FUNCTIONS:
                attr = LOOKUP_SEP.join(lookup_attr[:-1])

                lookup_value = self.FILTER_FUNCTIONS.get(lookup_attr[-1])(value_filter)
            else:
                lookup_value = self.FILTER_FUNCTIONS.get('eq')(value_filter)

            attr = attr.replace(LOOKUP_SEP, '.')

            self._filters[attr] = lookup_value

        self._filter_entities(self._initial_entities, self._filters)
        self._is_filtered = True

        return self

    def get_by_key(
        self,
        key: Union[Any, Tuple[Any]],
        strict_mode=True,
    ):
        """Метод получения значения из кеша по ключу поиска.

        В общем случае передаваемый ключ должен совпадать с _searching_key.
        Если отключить строгий режим поиска - strict_mode=False, то можно
        получить промежуточный результат по части ключа следующего с начала.
        """
        key = (
            key if
            self._check_is_iterable(key) else
            (key, )
        )
        key_items_count = len(key)
        searching_key_items_count = len(self._searching_key)

        if key_items_count > searching_key_items_count:
            raise ValueError(
                SEARCHING_KEY_SIZE_MORE_THAN_DEFAULT_SEARCHING_KEY_ERROR
            )
        elif key_items_count < searching_key_items_count and strict_mode:
            raise ValueError(
                SEARCHING_KEY_SIZE_LESS_THAN_DEFAULT_SEARCHING_KEY_ERROR
            )

        result = None
        temp_hash_item = self._initial_entities_hash_table
        for index, key_item in enumerate(key, start=1):
            if key_item not in temp_hash_item:
                if not strict_mode and index != 1:
                    result = temp_hash_item

                break

            temp_hash_item = temp_hash_item[key_item]

            if index == key_items_count:
                result = temp_hash_item

        return result

    def values_list(
        self,
        *args,
        flat: bool = False,
        **kwargs,
    ) -> Optional[List[Tuple]]:
        """Получение списка кортежей состоящих из значений полей объектов согласно заданным параметрам."""
        entities = self.all()

        if flat and len(args) > 1:
            raise RuntimeError('Multiple fields found in flat mode! Please check arguments.')

        fields_getter = attrgetter(*args)

        values_list_ = [fields_getter(entity) for entity in entities]

        if flat:
            values_list_ = list(
                filter(
                    None,
                    values_list_
                )
            )

        return values_list_

    def exists(self) -> bool:
        """Проверка существования отфильтрованных данных."""
        entities = self.all()

        return bool(entities)


class ActualEntityCache(EntityCache):
    """Базовый класс кеша актуальных записей сущности."""

    def __init__(
        self,
        actual_date,
        *args,
        **kwargs,
    ):
        self._actual_date = actual_date

        super().__init__(*args, **kwargs)

    def _prepare_actual_entities_queryset(self) -> Dict[str, date]:
        """Метод получения фильтра актуализации по дате."""
        actual_entities_queryset = super()._prepare_actual_entities_queryset()

        actual_entities_queryset = actual_entities_queryset.filter(
            begin__lte=self._actual_date,
            end__gte=self._actual_date,
        )

        return actual_entities_queryset


class PeriodicalEntityCache(BaseCache):
    """Базовый класс периодического кеша.

    Кеш создается для определенной модели с указанием двух дат, на которые
    должны быть собраны кеши актуальных объектов модели.

    Для примера, может использоваться при переносах остатков на очередной год
    с 31 декабря на 1 января нового года.
    """

    entity_cache_class = EntityCache

    def __init__(
        self,
        date_from: date,
        date_to: date,
        model: Type[Model],
        *args,
        select_related_fields: Optional[Tuple[str, ...]] = None,
        annotate_fields: Optional[Dict] = None,
        only_fields: Optional[Tuple[str, ...]] = None,
        values_fields: Optional[Tuple[str, ...]] = None,
        additional_filter_params: Optional[Union[Tuple[Union[Q, Dict[str, Any]]], Dict[str, Any]]] = None,
        exclude_params: Optional[Dict[str, Any]] = None,
        searching_key: Union[str, Tuple[str, ...]] = ('pk', ),
        is_force_fill_cache: bool = True,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if date_from >= date_to:
            raise ValueError(
                DATE_FROM_MORE_OR_EQUAL_DATE_TO_ERROR
            )

        self._model = model
        self._select_related_fields = select_related_fields
        self._annotate_fields = annotate_fields
        self._only_fields = only_fields
        self._values_fields = values_fields

        self._additional_filter_params = (
            self._prepare_additional_filter_params(additional_filter_params)
            if additional_filter_params
            else ([], {})
        )

        self._exclude_params = exclude_params

        self._is_force_fill_cache = is_force_fill_cache

        self._searching_key = searching_key

        self._date_from = date_from
        self._date_to = date_to

        self._old_entities_cache: Optional[EntityCache] = None
        self._new_entities_cache: Optional[EntityCache] = None

        if self._is_force_fill_cache:
            self.prepare(*args, **kwargs)

    def __repr__(self):
        return (
            f'<{self.__class__.__name__} @model="{self._model.__name__}" '
            f'@date_from="{date2str(self._date_from)}" '
            f'@date_to="{date2str(self._date_to)}" '
            f'@searching_key="{self._searching_key}">'
        )

    def __str__(self):
        return self.__repr__()

    @property
    def old(self):
        """
        Кеш объектов модели актуальных на начальную дату
        """
        return self._old_entities_cache

    @property
    def new(self):
        """
        Кеш объектов модели актуальный на конечную дату
        """
        return self._new_entities_cache

    def _prepare_additional_filter_params(
        self,
        filter_params: Union[Tuple[Union[Q, Dict[str, Any]]], Dict[str, Any]],
    ) -> Tuple[List[Q], Dict[str, Any]]:
        """Подготовка параметров фильтрации.

        Args:
            filter_params: Параметры фильтрации задаваемые пользователем. Кортеж Q со словарем для именованных
                параметров, например, обозначение вхождения.
        """
        filter_args = []
        filter_kwargs = {}

        if isinstance(filter_params, dict):
            filter_kwargs = filter_params
        else:
            for param in filter_params:
                if isinstance(param, Q):
                    filter_args.append(param)
                elif isinstance(param, dict):
                    filter_kwargs.update(**param)
                else:
                    raise ValueError('Please, check `additional_filter_params`, incorrect value!')

        return filter_args, filter_kwargs

    def _get_actuality_filter(
        self,
        period_type: str,
    ) -> Dict[str, date]:
        """
        Метод получения фильтра актуализации по дате.

        При получении счетов или аналитик при переносе остатков необходимо
        учитывать период действия следуя следующей логике:
        -- старые - begin < date_from &&  end >= date_from
        -- новые - begin <= date_to && end > date_to

        :param dict period_type: словарь с параметрами для актуализации по дате
        :return:
        """
        if period_type == TransferPeriodEnum.OLD:
            actuality_filter = {
                'begin__lt': self._date_from,
                'end__gte': self._date_from,
            }
        else:
            actuality_filter = {
                'begin__lte': self._date_to,
                'end__gt': self._date_to,
            }

        return actuality_filter

    def _prepare_entities_cache(
        self,
        additional_filter_params: Tuple[Union[Q, Dict[str, Any]]],
    ):
        """
        Создание кеша объектов модели на указанную дату по указанным параметром
        с ключом поиска для построения хеш-таблицы
        """
        entities_cache = self.entity_cache_class(
            model=self._model,
            select_related_fields=self._select_related_fields,
            annotate_fields=self._annotate_fields,
            only_fields=self._only_fields,
            values_fields=self._values_fields,
            additional_filter_params=additional_filter_params,
            exclude_params=self._exclude_params,
            searching_key=self._searching_key,
            is_force_fill_cache=self._is_force_fill_cache,
        )

        return entities_cache

    def _prepare_periodical_additional_filter_params(
        self,
        period_type: str,
    ) -> Tuple[Union[Q, Dict[str, Any]]]:
        """
        Подготовка словаря с дополнительными параметрами для дальнейшей
        фильтрации объектов при формировании кеша
        """
        additional_filter_params = deepcopy(self._additional_filter_params)

        additional_filter_params[1].update(
            **self._get_actuality_filter(
                period_type=period_type,
            )
        )

        return (*additional_filter_params[0], additional_filter_params[1])

    def _prepare_old_additional_filter_params(self):
        """
        Подготовка дополнительных параметров фильтрации на начальную дату
        """
        return self._prepare_periodical_additional_filter_params(
            period_type=TransferPeriodEnum.OLD,
        )

    def _prepare_new_additional_filter_params(self):
        """
        Подготовка дополнительных параметров фильтрации на конечную дату
        """
        return self._prepare_periodical_additional_filter_params(
            period_type=TransferPeriodEnum.NEW,
        )

    def _prepare_old_entities_cache(self):
        """
        Формирование кеша объектов модели на начальную дату
        """
        additional_filter_params = self._prepare_old_additional_filter_params()

        self._old_entities_cache = self._prepare_entities_cache(
            additional_filter_params=additional_filter_params,
        )

    def _prepare_new_entities_cache(self):
        """
        Формирование кеша объектов модели на конечную дату
        """
        additional_filter_params = self._prepare_new_additional_filter_params()

        self._new_entities_cache = self._prepare_entities_cache(
            additional_filter_params=additional_filter_params,
        )

    def _before_prepare(self, *args, **kwargs):
        """
        Точка расширения перед формированием кеша
        """

    def _prepare(self, *args, **kwargs):
        """
        Формирование кешей на начальную и конечную даты
        """
        self._prepare_old_entities_cache()
        self._prepare_new_entities_cache()

    def _after_prepare(self, *args, **kwargs):
        """
        Точка расширения после формирования кеша
        """


class CacheStorage(BaseCache):
    """
    Хранилище кешей.

    Для выполнения функций, в большинстве случаев, необходимы кеши для
    множества сущностей созданные по особым правилам, но подчиняющиеся общим.
    Для их объединения и применения в функции создаются хранилища, содержащие кеши в виде публичных свойств, с
    которыми в дальнейшем удобно работать
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def prepare(self, *args, **kwargs):
        """
        Подготовка хранилища кешей.

        При подготовке хранилища должна быть произведена подготовка всех кешей для работы с ними.
        """
        super().prepare(*args, **kwargs)

        for attr_value in self.__dict__.values():
            if isinstance(attr_value, BaseCache) and not attr_value.is_prepared:
                attr_value.prepare(*args, **kwargs)


class PatchedGlobalCacheStorage(CacheStorage):
    """
    Хранилище кешей с функциональностью патчинга кеша или хранилища кешей с использованием глобального (внешнего)
    кеша или хранилища кешей. Пригождается в случае использования глобального хелпера, когда есть необходимость
    создания кеша функции на основе кеша ранера.
    """

    def patch_by_global_cache(
        self,
        global_cache: BaseCache,
    ):
        """
        Патчинг кеша или хранилища кеша с использованием внешнего кеша или хранилища кешей.

        Args:
            global_cache: Внешний кеш или хранилище кешей.
        """
        pass
