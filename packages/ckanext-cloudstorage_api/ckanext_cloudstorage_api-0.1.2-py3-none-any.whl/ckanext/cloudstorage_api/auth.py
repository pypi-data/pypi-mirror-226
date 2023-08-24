"""Require authentication on endpoints."""

from ckan.logic import check_access


def get_auth_functions():
    return {
        "cloudstorage_initiate": initiate_multipart,
        "cloudstorage_presign_download": get_presigned_url_download,
        "cloudstorage_presign_upload": get_presigned_upload_url_multipart,
        "cloudstorage_presign_upload_list": get_presigned_upload_url_list_multipart,
        "cloudstorage_list_parts": list_parts,
        "cloudstorage_finish": finish_multipart,
        "cloudstorage_abort": abort_multipart,
        "cloudstorage_check": multipart_check,
        "cloudstorage_clean_multiparts": clean_multipart,
    }


def initiate_multipart(context, data_dict):
    return {"success": check_access("resource_create", context, data_dict)}


def get_presigned_url_download(context, data_dict):
    return {"success": check_access("resource_create", context, data_dict)}


def get_presigned_upload_url_multipart(context, data_dict):
    return {"success": check_access("resource_create", context, data_dict)}


def get_presigned_upload_url_list_multipart(context, data_dict):
    return {"success": check_access("resource_create", context, data_dict)}


def list_parts(context, data_dict):
    return {"success": check_access("resource_create", context, data_dict)}


def finish_multipart(context, data_dict):
    return {"success": check_access("resource_create", context, data_dict)}


def abort_multipart(context, data_dict):
    return {"success": check_access("resource_create", context, data_dict)}


def multipart_check(context, data_dict):
    return {"success": check_access("resource_create", context, data_dict)}


def clean_multipart(context, data_dict):
    return {"success": False}
