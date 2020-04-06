from bson import ObjectId
from mongoengine import Q
from mongoengine.queryset.visitor import QCombination
from models.user import User


class UserService:
    @staticmethod
    def get_users(user_ids=[], emails=[], query='', page=None, limit=None, paginate=True, data_objects=False):
        """
        :param page: page number
        :param limit: no of results per page
        :param query: query string
        :param user_ids: List of ad IDs
        :param emails: List of emails
        :param paginate: Boolean, to return paginated results if true
        :param data_objects: Boolean, to return queryset
        :return: Returns users filtered on the requirement in the specified format
        """
        if user_ids:
            users = User.objects.filter(id__in=user_ids, deleted=False)
        else:
            match_case_query = [Q(deleted=False)]
            if emails:
                match_case_query.append(Q(email__in=emails))

            match_query = QCombination(QCombination.AND, match_case_query)
            users = User.objects.filter((Q(name__icontains=query) | Q(email__icontains=query)) &
                                        match_query).order_by('-created_at')

        if data_objects:
            return users    # Returns QuerySet
        if not paginate:
            return {"data": [instance.to_dict() for instance in list(users)]}
        else:
            users = users.paginate(page=page, per_page=limit)
            return {"data": [instance.to_dict() for instance in users.items],
                    "current_page": users.page,
                    "total_pages_for_query": users.pages,
                    "item_per_page": users.per_page,
                    "total_records": users.total,
                    "next_num": users.next_num,
                    "prev_num": users.prev_num,
                    "has_next": users.has_next,
                    "has_prev": users.has_prev}

    @staticmethod
    def validate_id_and_get_instance(user_id):
        """Validates user id and return instance if available."""
        if not ObjectId.is_valid(user_id):
            return {"err": 'Invalid Ad ID.'}
        user = UserService.get_users(user_ids=[user_id], paginate=False, data_objects=True).first()
        if not user:
            return {"err": 'No User exists.'}
        return {"err": None, "instance": user}
