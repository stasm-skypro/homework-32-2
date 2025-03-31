# View for materials app
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from users.permissions import IsModerator, IsOwner
from .mixins import LessonPermissionMixin
from .models import Course, Lesson
from .paginators import CoursePagination
from .serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
import logging

logger = logging.getLogger(__name__)


# -- ViewSet для создания CRUD-операций с курсами --
class CourseViewSet(viewsets.ModelViewSet):
    """
    Определяет ViewSet для CRUD-операций с курсами.
    """

    queryset = Course.objects.all().order_by("id")

    # -- Serializer
    def get_serializer_class(self):
        """
        Переопределяет сериализатор для логгирования.
        :param self: Объект класса
        :return: Сериализатор списка курсов или сериализатор курса в зависимости от действия
        """
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    # -- Permissions
    def get_permissions(self):
        """
        Настраивает права доступа для владельцев и модераторов.
        :param self: Объект класса
        :return: Список разрешений
        """

        if self.action in ["create", "destroy"]:
            self.permission_classes = [
                IsAuthenticated,
                IsOwner,
            ]  # Только владелец может создавать и удалять
        else:
            self.permission_classes = [
                IsAuthenticated,
                IsOwner | IsModerator,
            ]  # Владелец и модератор могут редактировать и просматривать
        return [permission() for permission in self.permission_classes]

    # -- Pagination
    pagination_class = CoursePagination

    # -- Переопределение метода для использования сериализатора
    def perform_create(self, serializer):
        """
        Сохраняет владельца.
        :param self: Объект класса
        :param serializer: Сериализатор
        :return: None
        """
        serializer.save(owner=self.request.user)

    # -- Переопределение методов CRUD для логгирования
    def create(self, request, *args, **kwargs):
        """
        Переопределяет создание курса для логгирования.
        :param self: Объект класса
        :param request: Запрос
        :param args: Список позиционных документов
        :param kwargs: Список именованных аргументов
        :return: Ответ
        """

        response = super().create(request, *args, **kwargs)
        logger.info(
            "Создан новый курс: %s пользователем %s",
            response.data.get("name"),
            request.user,
        )
        return response

    def list(self, request, *args, **kwargs):
        """
        Переопределяет получение списка курсов для логгирования.
        :param self: Объект класса
        :param request: Запрос
        :param args: Список позиционных документов
        :param kwargs: Список именованных аргументов
        :return: Ответ
        """
        logger.info("Получен запрос на список курсов от %s", request.user)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Переопределяет получение одного курса для логгирования.
        :param self: Объект класса
        :param request: Запрос
        :param args: Список позиционных документов
        :param kwargs: Список именованных аргументов
        :return: Ответ
        """
        course = self.get_object()
        logger.info("Курс %s запрошен пользователем %s", course.name, request.user)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Переопределяет обновление курса для логгирования.
        :param self: Объект класса
        :param request: Запрос
        :param args: Список позиционных документов
        :param kwargs: Список именованных аргументов
        :return: Ответ
        """
        response = super().update(request, *args, **kwargs)
        logger.info(
            "Курс %s обновлён пользователем %s", response.data.get("name"), request.user
        )
        return response

    def destroy(self, request, *args, **kwargs):
        """
        Переопределяет удаление курса для логгирования.
        :param self: Объект класса
        :param request: Запрос
        :param args: Список позиционных документов
        :param kwargs: Список именованных аргументов
        :return: Ответ
        """
        course = self.get_object()
        logger.warning("Курс %s удалён пользователем %s", course.name, request.user)
        return super().destroy(request, *args, **kwargs)


# -- API endpoints для создания CRUD-операций с уроками --
class LessonCreateAPIView(LessonPermissionMixin, generics.CreateAPIView):
    """
    Определяет API endpoint для создания урока.
    """

    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """
        Сохраняет владельца.
        :param self: Объект класса
        :param serializer: Сериализатор урока
        :return: None
        """
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Переопределяет создание урока для логгирования.
        :param self: Объект класса
        :param request: Запрос
        :param args: Список позиционных документов
        :param kwargs: Список именованных аргументов
        :return: Ответ
        """
        response = super().create(request, *args, **kwargs)
        logger.info(
            "Создан новый урок: %s пользователем %s",
            response.data.get("name"),
            request.user,
        )
        return response


class LessonListAPIView(LessonPermissionMixin, generics.ListAPIView):
    """
    Определяет API endpoint для получения списка уроков.
    """

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    pagination_class = CoursePagination

    def list(self, request, *args, **kwargs):
        """
        Переопределяет получение списка уроков для логгирования.
        :param self: Объект класса
        :param request: Запрос
        :param args: Список позиционных документов
        :param kwargs: Список именованных аргументов
        :return: Ответ
        """
        logger.info("Запрос на получение списка уроков от %s", request.user)
        return super().list(request, *args, **kwargs)


class LessonRetrieveAPIView(LessonPermissionMixin, generics.RetrieveAPIView):
    """
    Определяет API endpoint для получения одного урока.
    """

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Переопределяет получение одного урока для логгирования.
        :param self: Объект класса
        :param request: Запрос
        :param args: Список позиционных документов
        :param kwargs: Список именованных аргументов
        :return: Ответ
        """
        lesson = self.get_object()
        logger.info("Урок %s запрошен пользователем %s", lesson.name, request.user)
        return super().retrieve(request, *args, **kwargs)


class LessonUpdateAPIView(LessonPermissionMixin, generics.UpdateAPIView):
    """
    Определяет API endpoint для обновления урока.
    """

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer

    def update(self, request, *args, **kwargs):
        """
        Переопределяет обновление урока для логгирования.
        :param self: Объект класса
        :param request: Запрос
        :param args: Список позиционных документов
        :param kwargs: Список именованных аргументов
        :return: Ответ
        """
        response = super().update(request, *args, **kwargs)
        logger.info(
            "Урок %s обновлён пользователем %s", response.data.get("name"), request.user
        )
        return response


class LessonDestroyAPIView(LessonPermissionMixin, generics.DestroyAPIView):
    """
    Определяет API endpoint для удаления урока.
    """

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Переопределяет удаление урока для логгирования.
        :param self: Объект класса
        :param request: Запрос
        :param args: Список позиционных документов
        :param kwargs: Список именованных аргументов
        :return: Ответ
        """
        lesson = self.get_object()
        logger.warning("Урок %s удалён пользователем %s", lesson.name, request.user)
        return super().destroy(request, *args, **kwargs)
