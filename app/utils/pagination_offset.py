import math

class PaginationOffset:
    def __init__(self, page_number=1, page_size=20, order_by="-timestamp"):
        self.page_number = page_number
        self.page_size = page_size
        self.order_by = order_by

    def get_offset(self):
        upper_limit = self.page_number * self.page_size
        lower_limit = upper_limit - self.page_size
        return lower_limit, upper_limit

    def get_serialized_data(self, model, queryset, serializer=None, context=None):
        if serializer:
            serialized_data = serializer.serialize_many(queryset)
        else:
            class DynamicSerializer:
                @staticmethod
                def serialize(instance):
                    return {
                        column.name: getattr(instance, column.name)
                        for column in model.__table__.columns
                    }
            serialized_data = [DynamicSerializer.serialize(obj) for obj in queryset]
        return serialized_data

    def __call__(self, model, queryset, serializer=None, context=None):
        if not queryset:
            print("Empty queryset received.")
            return {
                "results": [],
                "count": 0,
                "total_pages": 0,
                "is_next_page": False,
            }

        lower_limit, upper_limit = self.get_offset()
        print(f"Pagination slice: {lower_limit} to {upper_limit}")

        paginated_queryset = queryset[lower_limit:upper_limit] if lower_limit < len(queryset) else queryset
        print(f"Paginated queryset: {paginated_queryset}")

        total_objects_count = len(queryset)
        total_pages = math.ceil(total_objects_count / self.page_size)
        is_next_page = self.page_number < total_pages

        serialized_data = self.get_serialized_data(model, paginated_queryset, serializer, context)
        print(f"Serialized results: {serialized_data}")

        return {
            "results": serialized_data,
            "count": total_objects_count,
            "total_pages": total_pages,
            "is_next_page": is_next_page,
        }
