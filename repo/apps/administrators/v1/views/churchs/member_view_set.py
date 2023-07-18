from django.utils.decorators import method_decorator

from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action

from common.pagination import JoodaPagination
from common import enums, response, decorators
from common.send import notification

from apps.administrators.v1 import serializers, utils
from apps.accounts.models import Account
from apps.churchs.models import ChurchMember


class ChurchMemberPagination(JoodaPagination):
    default_limit = 10


class ChurchMemberViewSet(mixins.ListModelMixin, GenericViewSet):
    http_method_names = ["get", "patch"]
    pagination_class = ChurchMemberPagination

    @method_decorator(decorators.administrator_authorization())
    def list(self, request):
        administrator = request.administrator
        keyword = request.query_params.get("keyword", None)
        payload = {}
        try:
            church_members = Account.objects.filter(
                church_member__state=enums.ChurchMemberState.SUCCESS,
                church_member__church=administrator.church,
            ).distinct()
            if keyword:
                church_members = church_members.filter(name__icontains=keyword)

            paginated_church_members = self.paginate_queryset(
                church_members.order_by("-created_at")
            )
            paginated_church_members = serializers.ChurchMemberInfoSerializer(
                paginated_church_members, many=True
            ).data
            payload["church_members"] = self.get_paginated_response(
                paginated_church_members
            )

            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.administrator_authorization())
    @action(detail=False, methods=["patch"])
    def kick_out(self, request):
        administrator = request.administrator
        member_list = request.data.getlist("member_list", None)

        try:
            if not member_list:
                return response.JoodaResponse.warning_response(request)

            church_member = ChurchMember.objects.select_related(
                "account", "church"
            ).filter(
                account__id__in=member_list,
                state=enums.ChurchMemberState.SUCCESS,
                church=administrator.church,
            )

            tokens, accounts = utils.get_id_fcmtoken_from_churchmember(church_member)
            sub_title = (
                administrator.church.name
                if administrator.church.name[-2:] == "교회"
                else administrator.church.name + "교회"
            )

            notifications = notification.PushNotification(
                tokens=tokens,
                accounts=accounts,
                title=administrator.church.name,
                sub_title=f"{sub_title}{enums.PushNotificationContent.KICK_OFF}",
                _id=f"",
                _type="",
                domain=enums.PushNotificationDomain.CHURCH,
                church_id=str(administrator.church.id),
            )
            notifications.send_push()
            church_member.update(state=enums.ChurchMemberState.REJECT)

            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    class ChurchConfirmMemberViewSet(
        mixins.ListModelMixin, mixins.UpdateModelMixin, GenericViewSet
    ):
        http_method_names = ["get", "patch"]
        pagination_class = ChurchMemberPagination

        @method_decorator(decorators.administrator_authorization())
        def list(self, request):
            administrator = request.administrator
            keyword = request.query_params.get("keyword", None)
            payload = {}
            try:
                church_members = Account.objects.filter(
                    church_member__state=enums.ChurchMemberState.CONFIRM,
                    church_member__church=administrator.church,
                ).distinct()
                if keyword:
                    church_members = church_members.filter(name__icontains=keyword)

                paginated_church_members = self.paginate_queryset(
                    church_members.order_by("-created_at")
                )
                paginated_church_members = serializers.ChurchMemberInfoSerializer(
                    paginated_church_members, many=True
                ).data
                payload["confirm_members"] = self.get_paginated_response(
                    paginated_church_members
                )

                return response.JoodaResponse.success_response(payload)
            except Exception as e:
                return response.JoodaResponse.error_response(request, error=e)

        @method_decorator(decorators.administrator_authorization())
        def patch(self, request):
            administrator = request.administrator
            member_list = request.data.getlist("member_list", None)
            member_state = request.data.get("member_state", None)

            try:
                if not (member_list and member_state):
                    return response.JoodaResponse.warning_response(request)
                if member_state not in [
                    enums.ChurchMemberState.REJECT,
                    enums.ChurchMemberState.SUCCESS,
                ]:
                    return response.JoodaResponse.warning_response(
                        request, enums.ErrorCode.BAD_PARAMETER_RECEIVED
                    )

                church_member = ChurchMember.objects.filter(
                    account__id__in=member_list,
                    state=enums.ChurchMemberState.CONFIRM,
                    church=administrator.church,
                )

                tokens, accounts = utils.get_id_fcmtoken_from_churchmember(
                    church_member
                )
                church_name = (
                    administrator.church.name
                    if administrator.church.name[-2:] == "교회"
                    else administrator.church.name + "교회"
                )
                patch_comment = (
                    enums.PushNotificationContent.SUCCESS
                    if member_state == enums.ChurchMemberState.SUCCESS
                    else enums.PushNotificationContent.REJECT
                )
                sub_title = church_name + patch_comment
                notifications = notification.PushNotification(
                    tokens=tokens,
                    accounts=accounts,
                    title=administrator.church.name,
                    sub_title=sub_title,
                    _id=f"",
                    _type="",
                    domain=enums.PushNotificationDomain.CHURCH,
                    church_id=str(administrator.church.id),
                )
                notifications.send_push()
                church_member.update(state=member_state)

                return response.JoodaResponse.success_response()
            except Exception as e:
                return response.JoodaResponse.error_response(request, error=e)
