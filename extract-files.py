#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixup_vendorcompat,
    lib_fixups,
    lib_fixups_user_type,
    libs_proto_3_9_1,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/motorola/fogos',
    'hardware/qcom-caf/common/libqti-perfd-client',
    'hardware/qcom-caf/sm8350',
    'hardware/qcom-caf/wlan',
    'hardware/motorola',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'libmmosal',
        'vendor.qti.diaghal@1.0',
        'vendor.qti.hardware.fm@1.0',
        'vendor.qti.hardware.qccsyshal@1.0',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
    (
        'vendor.qti.qspmhal@1.0',
    ): lib_fixup_remove,
    libs_proto_3_9_1: lib_fixup_vendorcompat,
}

blob_fixups: blob_fixups_user_type = {
    'system_ext/etc/permissions/moto-telephony.xml': blob_fixup()
        .regex_replace('/system/', '/system_ext/'),
    'system_ext/priv-app/ims/ims.apk': blob_fixup()
        .apktool_patch('ims-patches'),
    (
        'vendor/lib64/libdpps.so',
        'vendor/lib64/libsnapdragoncolor-manager.so',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    (
        'system_ext/lib64/vendor.qti.hardware.qccsyshal@1.2-halimpl.so',
        'system_ext/lib/vendor.qti.hardware.qccsyshal@1.2-halimpl.so',
    ): blob_fixup()
        .replace_needed('libprotobuf-cpp-full.so', 'libprotobuf-cpp-full-21.7.so'),
    'vendor/lib64/libwvhidl.so': blob_fixup()
        .add_needed('libcrypto_shim.so'),
    'vendor/etc/vintf/manifest/vendor.dolby.media.c2@1.0-service.xml': blob_fixup()
        .regex_replace('IComponentStore/default9', 'IComponentStore/default'),
    (
        'vendor/lib64/camera/components/com.mot.node.c2d.so',
        'vendor/lib64/camera/components/com.qti.node.dewarp.so',
        'vendor/lib64/camera/components/com.vidhance.node.ica.so',
        'vendor/lib64/camera/components/com.vidhance.node.processing.so',
    ): blob_fixup()
        .replace_needed('libui.so', 'libui-v34.so'),
    (
        'vendor/lib/libmot_chi_desktop_helper.so',
        'vendor/lib64/libmot_chi_desktop_helper.so',
    ): blob_fixup()
        .add_needed('libgui_shim_vendor.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'fogos',
    'motorola',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_generated_carriersettings=True,
)

module.add_proprietary_file('proprietary-files-fm.txt').add_copy_files_guard(
    'TARGET_HAS_FM', 'true'
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
