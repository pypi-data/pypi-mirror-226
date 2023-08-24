# encoding: utf-8
"""
@project: djangoModel->single_push_pipline
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 单挑推送管道
@created_time: 2023/8/23 13:13
"""
from django.db.models import F

from xj_enroll.models import EnrollSubitemRecord
from xj_push.push_pipeline.pipline_base import PipelineBase
from xj_push.services.push_single_service import PushSingleService
from ..utils.custom_tool import force_transform_type, dynamic_load_class, write_to_log


class SinglePushPipeline(PipelineBase):
    notice_title = {
        "publish": "提交订单",
        "enroll": "项目报名",
        "appoint": "选择镖师",
        "pay": "完成支付",
        "upload": "上传标书文件",
        "accept_in_checking": "审核通过标书资料",
        "check_fial_upload": "操作驳回",
        "accept": "操作验收",
        "cancel_publish": "取消订单",
    }

    @staticmethod
    def process(*args, params: dict = None, **kwargs):
        # 获取报名相关的信息
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)
        enroll_id = params.get("enroll_id", None)
        if not enroll_id:
            return None, "报名ID错误"

        # 导入依赖
        Enroll, enroll_import_err = dynamic_load_class(import_path="xj_enroll.models", class_name="Enroll")
        EnrollRecord, record_import_err = dynamic_load_class(import_path="xj_enroll.models", class_name="EnrollRecord")
        if enroll_import_err or record_import_err:
            write_to_log(prefix="站内推送管道异常", content="请安装报名模块")
            return None, None

        print("params >>>>>>>>>>", params, "\n")
        # 获取相关信息
        enroll_info = Enroll.objects.filter(id=enroll_id).values().first()
        thread_id = enroll_info.get("thread_id")
        enroll_user_id = enroll_info.get("user_id")
        add_params = {"thread_id": thread_id, "source_code": "订单动态"}

        # ------------------------- section 管道挂油，管道分流 start ------------------------
        # 发布的订单后通知客户
        if params.get("push_action") == "publish":
            add_params["content"] = add_params["title"] = "订单发布成功"
            add_params["to_user_id"] = enroll_user_id
            data, err = PushSingleService.add(params=add_params)

        # 镖师报名相互通知
        elif params.get("push_action") == "enroll":
            # 提醒客户有人报名
            add_params["content"] = add_params["title"] = "项目报名"
            add_params["to_user_id"] = enroll_user_id
            data, err = PushSingleService.add(params=add_params)
            # 体校镖师报名成功
            record_info = EnrollRecord.objects.filter(id=params.get("record_id")).values().first()
            if record_info:
                add_params["content"] = add_params["title"] = "报名成功"
                add_params["to_user_id"] = record_info.get("user_id")
                data, err = PushSingleService.add(params=add_params)

        # 用户取消订单通知所有的报名用户
        elif params.get("push_action") == "cancel_publish":
            # 通知所有报名的用户
            add_params["content"] = add_params["title"] = "客户取消订单"
            record_infos = list(EnrollRecord.objects.filter(enroll_id=enroll_id).values())
            for i in record_infos:
                if not i.get("user_id"):
                    continue
                add_params["to_user_id"] = i.get("user_id")
                PushSingleService.add(params=add_params)

            # 通知客户取消成功
            add_params["content"] = add_params["title"] = "取消订单成功"
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

        # 指派通知
        elif params.get("push_action") == "appoint":
            # 通知客户指派成功
            add_params["content"] = add_params["title"] = "选择镖师成功"
            add_params["to_user_id"] = enroll_user_id
            data, err = PushSingleService.add(params=add_params)

            # 通知镖师您已被指派
            record_info = EnrollRecord.objects.filter(id=params.get("record_id")).first().values()
            if record_info:
                add_params["content"] = add_params["title"] = "您已被指派"
                add_params["to_user_id"] = record_info.get("user_id")
                data, err = PushSingleService.add(params=add_params)

            # 没有指派的镖师给予提示
            un_appoint_records = list(EnrollRecord.objects.exclude(id=params.get("record_id")).values())
            for i in un_appoint_records:
                add_params["content"] = add_params["title"] = "很遗憾，您没有选中，再接再厉"
                add_params["to_user_id"] = i.get("user_id")
                data, err = PushSingleService.add(params=add_params)

        # 已支付通知客户
        elif params.get("push_action") == "payed":
            add_params["content"] = add_params["title"] = "支付成功"
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

        # 镖师上传
        elif params.get("push_action") == "upload":
            print("执行")
            add_params["content"] = add_params["title"] = "镖书文件已上传"
            # 通知客户
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

            # 通知镖师
            subitem_record = EnrollSubitemRecord.objects.annotate(
                record_user_id=F("enroll_record__user_id")
            ).filter(id=params.get("id")).values("record_user_id", "id").first()
            if subitem_record:
                add_params["to_user_id"] = subitem_record.get("record_user_id")
                PushSingleService.add(params=add_params)

        # 标书初审通过
        elif params.get("push_action") == "check_success":
            add_params["content"] = add_params["title"] = "镖书文件初审成功"
            # 通知客户
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

            # 通知镖师
            bx_worker = EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code=124).values().first()
            if bx_worker:
                add_params["to_user_id"] = bx_worker.get("user_id")
                PushSingleService.add(params=add_params)

        # 标书初审失败
        elif params.get("push_action") == "check_fail":
            add_params["content"] = add_params["title"] = "镖书文件初审失败"
            # 通知客户
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

            # 通知镖师
            bx_worker = EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code=124).values().first()
            if bx_worker:
                add_params["to_user_id"] = bx_worker.get("user_id")
                PushSingleService.add(params=add_params)

        # 标书初审通过
        elif params.get("push_action") == "accept_success":
            add_params["content"] = add_params["title"] = "镖书文件验收成功"
            # 通知客户
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

            # 通知镖师
            bx_worker = EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code=124).values().first()
            if bx_worker:
                add_params["to_user_id"] = bx_worker.get("user_id")
                PushSingleService.add(params=add_params)

        elif params.get("push_action") == "accept_fail":  # 标书初审失败
            add_params["content"] = add_params["title"] = "镖书文件验收失败"
            # 通知客户
            add_params["to_user_id"] = enroll_user_id
            PushSingleService.add(params=add_params)

            # 通知镖师
            bx_worker = EnrollRecord.objects.filter(enroll_id=enroll_id).exclude(enroll_status_code=124).values().first()
            if bx_worker:
                add_params["to_user_id"] = bx_worker.get("user_id")
                PushSingleService.add(params=add_params)

        # ------------------------- section 管道挂油 end  ------------------------
        return None, None
