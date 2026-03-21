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
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/qcom-caf/sm8650',
    'hardware/qcom-caf/wlan',
    'hardware/sony',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
    'vendor/sony/sm8650-common',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.qti.hardware.fm@1.0',
        'vendor.qti.hardware.data.cne.internal.api@1.0',
        'vendor.qti.hardware.data.cne.internal.constants@1.0',
        'vendor.qti.hardware.data.cne.internal.server@1.0',
        'vendor.qti.hardware.data.connection@1.0',
        'vendor.qti.hardware.data.connection@1.1',
        'vendor.qti.hardware.data.dynamicdds@1.0',
        'vendor.qti.hardware.data.iwlan@1.0',
        'vendor.qti.hardware.data.qmi@1.0',
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.hardware.dpmservice@1.0',
        'vendor.qti.diaghal@1.0',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.imsrtpservice@3.1',
        'vendor.qti.hardware.qccsyshal@1.0',
        'vendor.qti.hardware.qccsyshal@1.1',
        'vendor.qti.hardware.qccsyshal@1.2',
        'vendor.qti.hardware.qccvndhal@1.0',
        'vendor.qti.hardware.wifidisplaysession@1.0',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/bin/hw/vendor.semc.hardware.secd@1.1-service',
        'vendor/bin/keyprovd',
        'vendor/lib64/librkp.so',
    ): blob_fixup()
    .add_needed(
        'android.hardware.security.rkp-V3-ndk.so'
    ),
    ('vendor/bin/hw/android.hardware.security.keymint-service-spu-qti',
     'vendor/lib64/libspukeymint.so',
     ): blob_fixup()
        .replace_needed('android.hardware.security.sharedsecret-V2-ndk.so', 'android.hardware.security.sharedsecret-V1-ndk.so')
        .replace_needed('android.hardware.security.keymint-V3-ndk.so', 'android.hardware.security.keymint-V2-ndk.so'),
    'vendor/bin/slim_daemon': blob_fixup()
    .add_needed(
        'libc++_shared.so',
    ),
    'vendor/etc/init/android.hardware.security.keymint-service-spu-qti.rc': blob_fixup()
    .regex_replace(
        'on init && property:ro.boot.product.vendor.sku=pineapple', 'on init'
    ),
    'vendor/etc/msm_irqbalance.conf': blob_fixup()
    .regex_replace(
        'IGNORED_IRQ=27,23,38', 'IGNORED_IRQ=27,23,38,115,332'
    ),
    (
        'vendor/bin/hw/vendor.semc.hardware.extlight-service.somc',
        'vendor/lib64/vendor.semc.hardware.extlight-V1-ndk_platform.so',
    ): blob_fixup()
    .replace_needed(
        'android.hardware.light-V1-ndk_platform.so', 'android.hardware.light-V1-ndk.so'
    ),
    (
        'vendor/etc/seccomp_policy/wfdhdcphalservice.policy',
    ): blob_fixup()
    .add_line_if_missing(
        'gettid: 1'
    ),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
    .add_needed(
        'libhidlbase_shim.so',
    )
    .add_needed(
        'libbinder_shim.so',
    ),
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
    .add_needed(
        'libcodec2_shim.so'
    ),
    'vendor/lib64/hw/fingerprint.default.so': blob_fixup()
    .binary_regex_replace(b'bix.fingerprint', b'fingerprint\x00\x00\x00\x00'),
    'vendor/lib64/nfc_nci.nqx.default.hw.so': blob_fixup()
    .add_needed(
        'libbase_shim.so'
    ),
    'system_ext/lib64/libwfdnative.so': blob_fixup()
    .add_needed(
        'libinput_shim.so'
    ),
    'vendor/etc/seccomp_policy/gnss@2.0-qsap-location.policy': blob_fixup()
    .add_line_if_missing('sched_get_priority_min: 1')
    .add_line_if_missing('sched_get_priority_max: 1'),
    (
        'vendor/bin/poweropt-service',
        'vendor/lib64/libaodoptfeature.so',
        'vendor/lib64/libapengine.so',
        'vendor/lib64/libdpps.so',
        'vendor/lib64/liblearningmodule.so',
        'vendor/lib64/liboemcrypto.so',
        'vendor/lib64/libpowercore.so',
        'vendor/lib64/libpsmoptfeature.so',
        'vendor/lib64/libsnapdragoncolor-manager.so',
        'vendor/lib64/libstandbyfeature.so',
        'vendor/lib64/libvideooptfeature.so',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    'system_ext/lib64/vendor.qti.hardware.qccsyshal@1.2-halimpl.so': blob_fixup()
        .replace_needed('libprotobuf-cpp-full.so', 'libprotobuf-cpp-full-21.7.so'),
    (
        'vendor/bin/qcc-vendor',
        'vendor/bin/qms',
        'vendor/bin/xtra-daemon',
        'vendor/lib64/libcne.so',
        'vendor/lib64/libqcc_sdk.so',
        'vendor/lib64/libqms_client.so'
    ): blob_fixup()
        .add_needed('libbinder_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm8650-common',
    'sony',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
