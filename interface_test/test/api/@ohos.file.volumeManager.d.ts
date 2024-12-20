/*
 * Copyright (C) 2022-2023 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @file
 * @kit CoreFileKit
 */

import { AsyncCallback, Callback } from './@ohos.base';

/**
 * Provides volumemanager statistics APIs
 *
 * @namespace volumeManager
 * @syscap SystemCapability.FileManagement.StorageService.Volume
 * @systemapi
 * @since 9
 */
declare namespace volumeManager {
  /**
   * Get All Volumes
   *
   * @interface Volume
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  export interface Volume {
    /**
     * Volume ID.
     *
     * @type { string }
     * @syscap SystemCapability.FileManagement.StorageService.Volume
     * @systemapi
     * @since 9
     */
    id: string;

    /**
     * Universally unique identifier of volume.
     *
     * @type { string }
     * @syscap SystemCapability.FileManagement.StorageService.Volume
     * @systemapi
     * @since 9
     */
    uuid: string;

    /**
     * The ID of disk that volume belongs to.
     *
     * @type { string }
     * @syscap SystemCapability.FileManagement.StorageService.Volume
     * @systemapi
     * @since 9
     */
    diskId: string;

    /**
     * The label of the volume.
     *
     * @type { string }
     * @syscap SystemCapability.FileManagement.StorageService.Volume
     * @systemapi
     * @since 9
     */
    description: string;

    /**
     * The volume is removable or not.
     *
     * @type { boolean }
     * @syscap SystemCapability.FileManagement.StorageService.Volume
     * @systemapi
     * @since 9
     */
    removable: boolean;

    /**
     * The mount state of the volume.
     *
     * @type { number }
     * @syscap SystemCapability.FileManagement.StorageService.Volume
     * @systemapi
     * @since 9
     */
    state: number;

    /**
     * The mount path of the volume.
     *
     * @type { string }
     * @syscap SystemCapability.FileManagement.StorageService.Volume
     * @systemapi
     * @since 9
     */
    path: string;

    /**
     * The file system type of the volume.
     *
     * @type { string }
     * @syscap SystemCapability.FileManagement.StorageService.Volume
     * @systemapi
     * @since 12
     */
    fsType: string;
  }
  /**
   * Get All Volumes
   *
   * @permission ohos.permission.STORAGE_MANAGER
   * @param { AsyncCallback<Array<Volume>> } callback - callback
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:Mandatory
parameters are left unspecified;
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function getAllVolumes(callback: AsyncCallback<Array<Volume>>): void;

  /**
   * Get All Volumes
   *
   * @permission ohos.permission.STORAGE_MANAGER
   * @returns { Promise<Array<Volume>> } return Promise
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:Mandatory
parameters are left unspecified;
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function getAllVolumes(): Promise<Array<Volume>>;

  /**
   * Mount
   *
   * @permission ohos.permission.MOUNT_UNMOUNT_MANAGER
   * @param { string } volumeId - The id of the volume
   * @param { AsyncCallback<void> } callback - callback
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600002 - Not supported filesystem.
   * @throws { BusinessError } 13600003 - Failed to mount.
   * @throws { BusinessError } 13600005 - Incorrect volume state.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function mount(volumeId: string, callback: AsyncCallback<void>): void;

  /**
   * Mount
   *
   * @permission ohos.permission.MOUNT_UNMOUNT_MANAGER
   * @param { string } volumeId - The id of the volume
   * @returns { Promise<void> } return Promise
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600002 - Not supported filesystem.
   * @throws { BusinessError } 13600003 - Failed to mount.
   * @throws { BusinessError } 13600005 - Incorrect volume state.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function mount(volumeId: string): Promise<void>;

  /**
   * UnMount
   *
   * @permission ohos.permission.MOUNT_UNMOUNT_MANAGER
   * @param { string } volumeId - The id of the volume
   * @param { AsyncCallback<void> } callback - callback
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600002 - Not supported filesystem.
   * @throws { BusinessError } 13600004 - Failed to unmount.
   * @throws { BusinessError } 13600005 - Incorrect volume state.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function unmount(volumeId: string, callback: AsyncCallback<void>): void;

  /**
   * UnMount
   *
   * @permission ohos.permission.MOUNT_UNMOUNT_MANAGER
   * @param { string } volumeId - The id of the volume
   * @returns { Promise<void> } return Promise
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600002 - Not supported filesystem.
   * @throws { BusinessError } 13600004 - Failed to unmount.
   * @throws { BusinessError } 13600005 - Incorrect volume state.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function unmount(volumeId: string): Promise<void>;

  /**
   * Get the volume by uuid.
   *
   * @permission ohos.permission.STORAGE_MANAGER
   * @param { string } uuid - The uuid of volume
   * @param { AsyncCallback<Volume> } callback - callback
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function getVolumeByUuid(uuid: string, callback: AsyncCallback<Volume>): void;

  /**
   * Get the volume by uuid.
   *
   * @permission ohos.permission.STORAGE_MANAGER
   * @param { string } uuid - The uuid of volume
   * @returns { Promise<Volume> } return Promise
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function getVolumeByUuid(uuid: string): Promise<Volume>;

  /**
   * Get the volume by id.
   *
   * @permission ohos.permission.STORAGE_MANAGER
   * @param { string } volumeId - The id of volume
   * @param { AsyncCallback<Volume> } callback - callback
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function getVolumeById(volumeId: string, callback: AsyncCallback<Volume>): void;

  /**
   * Get the volume by id.
   *
   * @permission ohos.permission.STORAGE_MANAGER
   * @param { string } volumeId - The id of volume
   * @returns { Promise<Volume> } return Promise
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function getVolumeById(volumeId: string): Promise<Volume>;

  /**
   * Set the description of volume.
   *
   * @permission ohos.permission.MOUNT_UNMOUNT_MANAGER
   * @param { string } uuid - The uuid of volume
   * @param { string } description - New description of volume
   * @param { AsyncCallback<void> } callback - callback
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600002 - Not supported filesystem.
   * @throws { BusinessError } 13600005 - Incorrect volume state.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function setVolumeDescription(uuid: string, description: string, callback: AsyncCallback<void>): void;

  /**
   * Set the description of volume.
   *
   * @permission ohos.permission.MOUNT_UNMOUNT_MANAGER
   * @param { string } uuid - The uuid of volume
   * @param { string } description - New description of volume
   * @returns { Promise<void> } return Promise
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600002 - Not supported filesystem.
   * @throws { BusinessError } 13600005 - Incorrect volume state.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function setVolumeDescription(uuid: string, description: string): Promise<void>;

  /**
   * Format.
   *
   * @permission ohos.permission.MOUNT_FORMAT_MANAGER
   * @param { string } volumeId - The id of the volume
   * @param { string } fsType - The file system type after formatting
   * @param { AsyncCallback<void> } callback - callback
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600002 - Not supported filesystem.
   * @throws { BusinessError } 13600005 - Incorrect volume state.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function format(volumeId: string, fsType: string, callback: AsyncCallback<void>): void;

  /**
   * Format.
   *
   * @permission ohos.permission.MOUNT_FORMAT_MANAGER
   * @param { string } volumeId - The id of the volume
   * @param { string } fsType - The file system type after formatting
   * @returns { Promise<void> } return Promise
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600002 - Not supported filesystem.
   * @throws { BusinessError } 13600005 - Incorrect volume state.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function format(volumeId: string, fsType: string): Promise<void>;

  /**
   * Partition.
   *
   * @permission ohos.permission.MOUNT_FORMAT_MANAGER
   * @param { string } diskId - The id of the disk
   * @param { number } type - Type of partition such as private partition or public partition
   * @param { AsyncCallback<void> } callback - callback
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function partition(diskId: string, type: number, callback: AsyncCallback<void>): void;

  /**
   * Partition.
   *
   * @permission ohos.permission.MOUNT_FORMAT_MANAGER
   * @param { string } diskId - The id of the disk
   * @param { number } type - Type of partition such as private partition or public partition
   * @returns { Promise<void> } return Promise
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:1.Mandatory
parameters are left unspecified;
   * <br>2.Incorrect parameter types.
   * @throws { BusinessError } 13600001 - IPC error.
   * @throws { BusinessError } 13600008 - No such object.
   * @throws { BusinessError } 13900042 - Unknown error.
   * @syscap SystemCapability.FileManagement.StorageService.Volume
   * @systemapi
   * @since 9
   */
  function partition(diskId: string, type: number): Promise<void>;
}

export default volumeManager;
