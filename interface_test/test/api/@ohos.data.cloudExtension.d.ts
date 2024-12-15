/*
 * Copyright (c) 2023 Huawei Device Co., Ltd.
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
 * @kit ArkData
 */

import type rpc from './@ohos.rpc';
import type cloudData from './@ohos.data.cloudData';
import type relationalStore from './@ohos.data.relationalStore';

/**
 * Provides interfaces to implement extended cloud capabilities.
 *
 * @namespace cloudExtension
 * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
 * @since 11
 */
declare namespace cloudExtension {
  /**
   * Provides interface for managing cloud assets.
   *
   * @extends relationalStore.Asset
   * @interface CloudAsset
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface CloudAsset extends relationalStore.Asset {
    /**
     * Asset ID.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    assetId: string;

    /**
     * Asset hash value.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    hash: string;
  }

  /**
   * Indicates cloud assets in one column.
   *
   * @typedef { Array<CloudAsset> } CloudAssets
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  type CloudAssets = Array<CloudAsset>;

  /**
   * Indicates possible cloud types.
   *
   * @typedef { null | number | string | boolean | Uint8Array | CloudAsset | CloudAssets } CloudType
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  type CloudType = null | number | string | boolean | Uint8Array | CloudAsset | CloudAssets;

  /**
   * Defines cloud information.
   *
   * @interface CloudInfo
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface CloudInfo {
    /**
     * Cloud information. For details, see {@link ServiceInfo}.
     *
     * @type { ServiceInfo }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    cloudInfo: ServiceInfo;

    /**
     * Defines brief application information.
     *
     * @type { Record<string, AppBriefInfo> }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    apps: Record<string, AppBriefInfo>;
  }

  /**
   * Defines cloud service information.
   *
   * @interface ServiceInfo
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface ServiceInfo {
    /**
     * Whether cloud is enabled. The value <b>true</b> means cloud is enabled;
     * the value <b>false</b> means the opposite.
     *
     * @type { boolean }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    enableCloud: boolean;

    /**
     * ID of the cloud account generated by using SHA-256.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    id: string;

    /**
     * Total space (in KB) of the account on the server.
     *
     * @type { number }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    totalSpace: number;

    /**
     * Available space (in KB) of the account on the server.
     *
     * @type { number }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    remainingSpace: number;

    /**
     * Current user of the device.
     *
     * @type { number }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    user: number;
  }

  /**
   * Defines the brief application information.
   *
   * @interface AppBriefInfo
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface AppBriefInfo {
    /**
     * ID of the application.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    appId: string;

    /**
     * Bundle name.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    bundleName: string;

    /**
     * Whether cloud is enabled for the application.
     * The value <b>true</b> means the cloud is enabled; the <b>false</b> means
     * the opposite.
     *
     * @type { boolean }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    cloudSwitch: boolean;

    /**
     * Application instance ID.
     *
     * @type { number }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    instanceId: number;
  }

  /**
   * Enumerates the field types.
   *
   * @enum { number }
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export enum FieldType {
    /**
     * NULL.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    NULL = 0,

    /**
     * Number.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    NUMBER = 1,

    /**
     * Real.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    REAL = 2,

    /**
     * Text.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    TEXT = 3,

    /**
     * Boolean.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    BOOL = 4,

    /**
     * BLOB.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    BLOB = 5,

    /**
     * Asset. For details, see {@link relationalStore.Asset}.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    ASSET = 6,

    /**
     * Assets. For details, see {@link relationalStore.Assets}.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    ASSETS = 7
  }

  /**
   * Defines the fields.
   *
   * @interface Field
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface Field {
    /**
     * Alias of the field on the server.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    alias: string;

    /**
     * Column name.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    colName: string;

    /**
     * Type of the field. For details, see {@link FieldType}.
     *
     * @type { FieldType }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    type: FieldType;

    /**
     * Whether the current column holds the primary key.
     *
     * @type { boolean }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    primary: boolean;

    /**
     * Whether the current column is nullable.
     *
     * @type { boolean }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    nullable: boolean;
  }

  /**
   * Defines a table.
   *
   * @interface Table
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface Table {
    /**
     * Alias of the table on the server.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    alias: string;

    /**
     * Name of the table.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    name: string;

    /**
     * Fields in the table. For details, see {@link Field}.
     *
     * @type { Array<Field> }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    fields: Array<Field>;
  }

  /**
   * Defines a database.
   *
   * @interface Database
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface Database {
    /**
     * Name of the database.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    name: string;

    /**
     * Alias of the database on the server.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    alias: string;

    /**
     * Tables in the database. For details, see {@link Table}.
     *
     * @type { Array<Table> }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    tables: Array<Table>;
  }

  /**
   * Defines the application schema.
   *
   * @interface AppSchema
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface AppSchema {

    /**
     * Bundle name of the application.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    bundleName: string;

    /**
     * Schema version.
     *
     * @type { number }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    version: number;

    /**
     * Databases {@link Database} of the application.
     *
     * @type { Array<Database> }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    databases: Array<Database>;
  }

  /**
   * Defines the data in the cloud.
   *
   * @interface CloudData
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface CloudData {
    /**
     * Next cursor for query.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    nextCursor: string;

    /**
     * Whether the server has more data to query {@link CloudDB.query()}.
     *
     * @type { boolean }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    hasMore: boolean;

    /**
     * Array of data queried, including the data values and extension
     * values {@link ExtensionValue}.
     *
     * @type { Array<Record<string, CloudType>> }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    values: Array<Record<string, CloudType>>;
  }

  /**
   * Defines the subscription information.
   *
   * @interface SubscribeInfo
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface SubscribeInfo {
    /**
     * Subscription expiration time, in milliseconds.
     *
     * @type { number }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    expirationTime: number;

    /**
     * Data to be observed.
     *
     * @type { Record<string, Array<SubscribeId>> }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    subscribe: Record<string, Array<SubscribeId>>;
  }

  /**
   * Defines the subscription ID.
   *
   * @interface SubscribeId
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface SubscribeId {
    /**
     * Alias of the database on the server.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    databaseAlias: string;

    /**
     * Subscription ID generated by {@link CloudService.subscribe()}.
     *
     * @type { string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    id: string;
  }

  /**
   * Enumerates the operations that can be performed on the database.
   *
   * @enum { number }
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export enum Flag {
    /**
     * Insert data.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    INSERT = 0,

    /**
     * Update data.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    UPDATE = 1,

    /**
     * Delete data.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    DELETE = 2
  }

  /**
   * Defines the extension values.
   *
   * @interface ExtensionValue
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface ExtensionValue {
    /**
     * ID generated by {@link CloudDB.insert()}.
     * An ID is generated for each row when data is first inserted to the cloud.
     * The ID must be unique for each table.
     *
     * @type { string }
     * @readonly
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    readonly id: string;

    /**
     * Time when the row data was created.
     *
     * @type { number }
     * @readonly
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    readonly createTime: number;

    /**
     * Time when the row data was last modified.
     *
     * @type { number }
     * @readonly
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    readonly modifyTime: number;

    /**
     * Database operation.
     *
     * @type { Flag }
     * @readonly
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    readonly operation: Flag;
  }

  /**
   * Defines the lock information.
   *
   * @interface LockInfo
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface LockInfo {
    /**
     * Duration for which the cloud database is locked, in seconds.
     *
     * @type { number }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    interval: number;

    /**
     * Lock ID for locking the cloud database.
     *
     * @type { number }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    lockId: number;
  }

  /**
   * Enumerates the error codes.
   *
   * @enum { number }
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export enum ErrorCode {
    /**
     * Successful.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    SUCCESS = 0,

    /**
     * Unknown error.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    UNKNOWN_ERROR = 1,

    /**
     * Network error.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    NETWORK_ERROR = 2,

    /**
     * Cloud is disabled.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    CLOUD_DISABLED = 3,

    /**
     * The cloud database is locked by others.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    LOCKED_BY_OTHERS = 4,

    /**
     * The number of records exceeds the limit.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    RECORD_LIMIT_EXCEEDED = 5,

    /**
     * The cloud has no space for the asset.
     *
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    NO_SPACE_FOR_ASSET = 6
  }

  /**
   * Defines the result.
   *
   * @interface Result
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface Result<T> {
    /**
     * Error code.
     *
     * @type { number }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    code: number;

    /**
     * Error code description.
     *
     * @type { ?string }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    description?: string;

    /**
     * Result value.
     *
     * @type { ?T }
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    value?: T;
  }

  /**
   * Creates a share service stub with the specified instance.
   *
   * @param { ShareCenter } instance - Indicates the <b>ShareCenter</b> instance.
   * @returns { Promise<rpc.RemoteObject> } Returns remote object.
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  function createShareServiceStub(instance: ShareCenter): Promise<rpc.RemoteObject>;

  /**
   * Creates a cloud service stub with the specified instance.
   *
   * @param { CloudService } instance - Indicates the <b>CloudService</b> instance.
   * @returns { Promise<rpc.RemoteObject> } Returns the remote object.
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  function createCloudServiceStub(instance: CloudService): Promise<rpc.RemoteObject>;

  /**
   * Creates a cloud database stub with the specified instance.
   *
   * @param { CloudDB } instance - Indicates the <b>CloudDB</b> instance.
   * @returns { Promise<rpc.RemoteObject> } Returns the remote object.
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  function createCloudDBStub(instance: CloudDB): Promise<rpc.RemoteObject>;

  /**
   * Creates an asset loader stub with the specified instance.
   *
   * @param { AssetLoader } instance - Indicates the <b>AssetLoader</b> instance.
   * @returns { Promise<rpc.RemoteObject> } Returns remote object.
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  function createAssetLoaderStub(instance: AssetLoader): Promise<rpc.RemoteObject>;

  /**
   * Provides interfaces for the operations on the cloud database.
   *
   * @interface CloudDB
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface CloudDB {
    /**
     * Generates the IDs of the rows of data to be inserted to the cloud.
     * The IDs must be unique for each table.
     *
     * @param { number } count - Indicates the number of IDs to generate.
     * @returns { Promise<Result<Array<string>>> } Returns the IDs generated.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    generateId(count: number): Promise<Result<Array<string>>>;

    /**
     * Inserts data to the cloud.
     *
     * @param { string } table - Indicates the table name.
     * @param { Array<Record<string, CloudType>> } values - Indicates the data to insert.
     * @param { Array<Record<string, CloudType>> } extensions - Indicates the extension
     * values {@link ExtensionValue}.
     * @returns { Promise<Array<Result<Record<string, CloudType>>>> } Returns the insert result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    insert(
      table: string,
      values: Array<Record<string, CloudType>>,
      extensions: Array<Record<string, CloudType>>
    ): Promise<Array<Result<Record<string, CloudType>>>>;

    /**
     * Updates data in the cloud.
     *
     * @param { string } table - Indicates the table name.
     * @param { Array<Record<string, CloudType>> } values - Indicates the new data.
     * @param { Array<Record<string, CloudType>> } extensions - Indicates the extension
     * values {@link ExtensionValue}.
     * @returns { Promise<Array<Result<Record<string, CloudType>>>> } Returns the update result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    update(
      table: string,
      values: Array<Record<string, CloudType>>,
      extensions: Array<Record<string, CloudType>>
    ): Promise<Array<Result<Record<string, CloudType>>>>;

    /**
     * Deletes data.
     *
     * @param { string } table - Indicates the table name.
     * @param { Array<Record<string, CloudType>> } extensions - Indicates the extension
     * values {@link ExtensionValue}.
     * @returns { Promise<Array<Result<Record<string, CloudType>>>> } Returns the delete result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    delete(
      table: string,
      extensions: Array<Record<string, CloudType>>
    ): Promise<Array<Result<Record<string, CloudType>>>>;

    /**
     * Queries data.
     *
     * @param { string } table - Indicates the table name.
     * @param { Array<string> } fields - Indicates the columns to query.
     * @param { number } queryCount - Indicates the number of data records
     * to query.
     * @param { string } queryCursor - Indicates the cursor.
     * @returns { Promise<Result<CloudData>> } Returns the query result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    query(table: string, fields: Array<string>, queryCount: number, queryCursor: string): Promise<Result<CloudData>>;

    /**
     * Locks the cloud database.
     * The cloud database will be unlocked when the lock interval has expired.
     * When the cloud database is locked, other devices cannot synchronize data
     * with the cloud.
     *
     * @returns { Promise<Result<LockInfo>> } Returns the locked information.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    lock(): Promise<Result<LockInfo>>;

    /**
     * Uses the heartbeat to extend the lock interval if it is not enough.
     *
     * @param { number } lockId - Indicates the lock ID of the heartbeat.
     * @returns { Promise<Result<LockInfo>> } Returns the time.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    heartbeat(lockId: number): Promise<Result<LockInfo>>;

    /**
     * Unlocks the cloud database.
     *
     * @param { number } lockId - Indicates the lock ID.
     * @returns { Promise<Result<boolean>> } Returns the unlock result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    unlock(lockId: number): Promise<Result<boolean>>;
  }

  /**
   * Provides interfaces for implementing the asset loader.
   *
   * @interface AssetLoader
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface AssetLoader {
    /**
     * Downloads assets.
     *
     * @param { string } table - Indicates the name of the table.
     * @param { string } gid - Indicates the GID.
     * @param { string } prefix - Indicates the prefix information.
     * @param { Array<CloudAsset> } assets - Indicates the assets to download.
     * @returns { Promise<Array<Result<CloudAsset>>> } Returns the asset download result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    download(table: string, gid: string, prefix: string, assets: Array<CloudAsset>): Promise<Array<Result<CloudAsset>>>;

    /**
     * Uploads assets.
     *
     * @param { string } table - Indicates the name of the table.
     * @param { string } gid - Indicates the GID.
     * @param { Array<CloudAsset> } assets - Indicates the assets to upload.
     * @returns { Promise<Array<Result<CloudAsset>>> } Returns the asset upload result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    upload(table: string, gid: string, assets: Array<CloudAsset>): Promise<Array<Result<CloudAsset>>>;
  }

  /**
   * Provides interfaces for implementing ShareCenter.
   *
   * @interface ShareCenter
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface ShareCenter {
    /**
     * Shares data with specific participants.
     *
     * @param { number } userId - Indicates the user ID.
     * @param { string } bundleName - Indicates the bundle name.
     * @param { string } sharingResource - Indicates the sharing resource.
     * @param { Array<cloudData.sharing.Participant> } participants - Indicates the participant.
     * @returns { Promise<Result<Array<Result<cloudData.sharing.Participant>>>> } Returns the sharing result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    share(
      userId: number,
      bundleName: string,
      sharingResource: string,
      participants: Array<cloudData.sharing.Participant>
    ): Promise<Result<Array<Result<cloudData.sharing.Participant>>>>;

    /**
     * UnShares data with specific participants.
     *
     * @param { number } userId - Indicates the user ID.
     * @param { string } bundleName - Indicates the bundle name.
     * @param { string } sharingResource - Indicates the sharing resource.
     * @param { Array<cloudData.sharing.Participant> } participants - Indicates the participant.
     * @returns { Promise<Result<Array<Result<cloudData.sharing.Participant>>>> } Returns the sharing result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    unshare(
      userId: number,
      bundleName: string,
      sharingResource: string,
      participants: Array<cloudData.sharing.Participant>
    ): Promise<Result<Array<Result<cloudData.sharing.Participant>>>>;

    /**
     * Exits the sharing.
     *
     * @param { number } userId - Indicates the user ID.
     * @param { string } bundleName - Indicates the bundle name.
     * @param { string } sharingResource - Indicates the sharing resource.
     * @returns { Promise<Result<void>> } Returns the exit result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    exit(userId: number, bundleName: string, sharingResource: string): Promise<Result<void>>;

    /**
     * Changes privilege of the specific participants.
     *
     * @param { number } userId - Indicates the user ID.
     * @param { string } bundleName - Indicates the bundle name.
     * @param { string } sharingResource - Indicates the sharing resource.
     * @param { Array<cloudData.sharing.Participant> } participants - Indicates the participant.
     * @returns { Promise<Result<Array<Result<cloudData.sharing.Participant>>>> } Returns the changing result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    changePrivilege(
      userId: number,
      bundleName: string,
      sharingResource: string,
      participants: Array<cloudData.sharing.Participant>
    ): Promise<Result<Array<Result<cloudData.sharing.Participant>>>>;

    /**
     * Queries participants of the specific sharing resource.
     *
     * @param { number } userId - Indicates the user ID.
     * @param { string } bundleName - Indicates the bundle name.
     * @param { string } sharingResource - Indicates the sharing resource.
     * @returns { Promise<Result<Array<cloudData.sharing.Participant>>> } Returns the query result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    queryParticipants(
      userId: number,
      bundleName: string,
      sharingResource: string
    ): Promise<Result<Array<cloudData.sharing.Participant>>>;

    /**
     * Queries participants based on the specified invitation code.
     *
     * @param { number } userId - Indicates the user ID.
     * @param { string } bundleName - Indicates the bundle name.
     * @param { string } invitationCode - Indicates the invitation code.
     * @returns { Promise<Result<Array<cloudData.sharing.Participant>>> } Returns the query result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    queryParticipantsByInvitation(
      userId: number,
      bundleName: string,
      invitationCode: string
    ): Promise<Result<Array<cloudData.sharing.Participant>>>;

    /**
     * Confirms invitation.
     *
     * @param { number } userId - Indicates the user ID.
     * @param { string } bundleName - Indicates the bundle name.
     * @param { string } invitationCode - Indicates the invitation code.
     * @param { cloudData.sharing.State } state - Indicates the state.
     * @returns { Promise<Result<string>> } Returns the sharing resource.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    confirmInvitation(
      userId: number,
      bundleName: string,
      invitationCode: string,
      state: cloudData.sharing.State
    ): Promise<Result<string>>;

    /**
     * Changes confirmation.
     *
     * @param { number } userId - Indicates the user ID.
     * @param { string } bundleName - Indicates the bundle name.
     * @param { string } sharingResource - Indicates the sharing resource.
     * @param { cloudData.sharing.State } state - Indicates the state.
     * @returns { Promise<Result<void>> } Returns the change result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    changeConfirmation(
      userId: number,
      bundleName: string,
      sharingResource: string,
      state: cloudData.sharing.State
    ): Promise<Result<void>>;
  }

  /**
   * Provides interfaces for implementing CloudService.
   *
   * @interface CloudService
   * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
   * @systemapi
   * @since 11
   */
  export interface CloudService {
    /**
     * Obtains the service information.
     *
     * @returns { Promise<ServiceInfo> } Returns the service information obtained.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    getServiceInfo(): Promise<ServiceInfo>;

    /**
     * Obtains the brief application information.
     *
     * @returns { Promise<Record<string, AppBriefInfo>> }
     * Returns the key-value pairs corresponding to <b>bundle</b> and
     * <b>AppBriefInfo</b>.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    getAppBriefInfo(): Promise<Record<string, AppBriefInfo>>;

    /**
     * Obtains the application schema information.
     *
     * @param { string } bundleName - Indicates the bundle name of the application.
     * @returns { Promise<Result<AppSchema>> } Returns <b>AppSchema</b>.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    getAppSchema(bundleName: string): Promise<Result<AppSchema>>;

    /**
     * Subscribes to data changes in the cloud.
     * When the cloud server data is changed, the server notifies the device of
     * the data change.
     *
     * @param { Record<string, Array<Database>> } subInfo - Indicates
     * the data to be subscribed to, that is, the key-value pairs corresponding
     * to an array of bundle names and databases.
     * @param { number } expirationTime - Indicates the subscription expiration
     * time.
     * @returns { Promise<Result<SubscribeInfo>> } Returns <b>SubscribeInfo</b>.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    subscribe(
      subInfo: Record<string, Array<Database>>,
      expirationTime: number
    ): Promise<Result<SubscribeInfo>>;

    /**
     * Unsubscribes from the data changes in the cloud.
     *
     * @param { Record<string, Array<string>> } unsubscribeInfo - Indicates
     * the data to be unsubscribe from, that is, the key-value pairs
     *  corresponding to an array of bundle names and databases.
     * @returns { Promise<number> } Returns unsubscribeInfo result.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    unsubscribe(unsubscribeInfo: Record<string, Array<string>>): Promise<number>;

    /**
     * Connects to a database.
     *
     * @param { string } bundleName - Indicates the bundle name of the application.
     * @param { Database } database - Indicates the database to connect.
     * @returns { Promise<rpc.RemoteObject> } Returns connectDB RemoteObject.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    connectDB(bundleName: string, database: Database): Promise<rpc.RemoteObject>;

    /**
     * Connects to an assetLoader.
     *
     * @param { string } bundleName - Indicates the bundle name of the application.
     * @param { Database } database - Indicates the database of bundle.
     * @returns { Promise<rpc.RemoteObject> } Returns connectAssetLoader RemoteObject.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    connectAssetLoader(bundleName: string, database: Database): Promise<rpc.RemoteObject>;

    /**
     * Connects to a share center.
     *
     * @param { number } userId - Indicates the user ID.
     * @param { string } bundleName - Indicates the bundle name.
     * @returns { Promise<rpc.RemoteObject> } Returns shareCenter RemoteObject.
     * @syscap SystemCapability.DistributedDataManager.CloudSync.Server
     * @systemapi
     * @since 11
     */
    connectShareCenter(userId: number, bundleName: string): Promise<rpc.RemoteObject>;
  }
}

export default cloudExtension;